#!/bin/python

import sys
import subprocess
import os.path
import pathlib

import lupa

if (len(sys.argv)<3):
  print("Usage: generate_game_bash_script.py mods_file script_file")
  exit();

mods_file = open(sys.argv[1], "r");
mods_names = mods_file.read();
mods_file.close();

lua = lupa.LuaRuntime(unpack_returned_tuples=True)
mods_names = dict(lua.eval(mods_names))

game_repo = None
mod_repos = dict()
no_repos = dict()

for mod_name in mods_names.keys():
  result = subprocess.run(["git", "-C", mods_names[mod_name], "rev-parse", "--show-superproject-working-tree", "--show-toplevel"], capture_output=True)
  if result.returncode==0:
    repo_path = result.stdout[:-1].decode("utf-8").splitlines()
    repo_path = repo_path[0]
    game_conf = "{}/game.conf".format(repo_path)
    if os.path.exists(game_conf):
      if game_repo:
        if game_repo!=repo_path:
          raise Exception("More then one minetest subgame detected. \"{}\" and \"{}\"".format(game_repo, repo_path))
      else:
        game_repo = repo_path
    else:
      if not repo_path in mod_repos:
       mod_repos[repo_path] = []
      mod_repos[repo_path].append(mod_name)
  else:
    no_repos[mod_name] = mods_names[mod_name]

def repo_update_path_to_script(repo_path, name):
  script = ""
  try:
    result = subprocess.run(["git", "-C", repo_path, "branch", "--show-current"], capture_output=True)
    if result.returncode!=0:
      print("git rev-parse failed for {}".format(repo_path))
      raise Exception(result.stderr)
    checkout_to = result.stdout[:-1].decode("utf-8")
    need_merge = True
    if checkout_to=="":
      result = subprocess.run(["git", "-C", repo_path, "rev-parse", "HEAD"], capture_output=True)
      if result.returncode!=0:
        print("git rev-parse failed for {}".format(repo_path))
        raise Exception(result.stderr)
      checkout_to = result.stdout[:-1].decode("utf-8")
      need_merge = False
    
    result = subprocess.run(["git", "-C", repo_path, "remote", "get-url", "origin"], capture_output=True)
    if result.returncode!=0:
      print("git remote get-url failed for {}".format(repo_path))
      raise Exception(result.stderr)
    url = result.stdout[:-1].decode("utf-8")
    url = url.replace("git@github.com:", "https://github.com/")
    url = url.replace("git@gitlab.com:", "https://gitlab.com/")
    
    result = subprocess.run(["git", "-C", repo_path, "submodule"], capture_output=True)
    have_submodules = False
    if result.returncode==0:
      if (len(result.stdout.decode("utf-8"))>0):
        have_submodules = True
    
    script = "{}if [ ! -d \"$repodir\" ]; then\n".format(script)
    script = "{}  git clone {} \"$repodir\"\n".format(script, url)
    script = "{}else\n".format(script)
    script = "{}  git -C $repodir fetch origin\n".format(script)
    script = "{}fi\n".format(script)
    script = "{}git -C $repodir checkout {}\n".format(script, checkout_to)
    if need_merge:
      script = "{}git -C $repodir merge {} origin/{}\n".format(script, checkout_to, checkout_to)
    if have_submodules:
      script = "{}git -C $repodir submodule init\n".format(script)
      script = "{}git -C $repodir submodule update\n".format(script)
      
    script = "{}\n".format(script)
  
  except Exception as e:
    print(e)
    script = "{}# Error in bash generation.\n\n".format(script)
  return script

def repo_check_commit(repo_path, name):
  script = ""
  try:
    result = subprocess.run(["git", "-C", repo_path, "rev-parse", "HEAD"], capture_output=True)
    if result.returncode!=0:
      print("git rev-parse failed for {}".format(repo_path))
      raise Exception(result.stderr)
    commit = result.stdout[:-1].decode("utf-8")
    
    script = "{}if [ $(git -C $repodir rev-parse HEAD) != {} ]; then\n".format(script, commit)
    script = "{}  echo \"{} is checkouted in unexpected commit.\"\n".format(script, name)
    script = "{}fi\n".format(script)
      
    script = "{}\n".format(script)
  
  except Exception as e:
    print(e)
    script = "{}# Error in bash generation.\n\n".format(script)
  return script

script = "#!/bin/bash\n\n"

script = "{}if [ $# -le 2 ]; then\n".format(script)
script = "{}  echo \"Usage:\"\n".format(script)
script = "{}  echo \"  {} game_id game_dir mods_dir\"\n".format(script, sys.argv[2])
script = "{}  exit\n".format(script)
script = "{}fi\n".format(script)
script = "{}\n".format(script)
script = "{}gameid=$1\n".format(script)
script = "{}gamedir=$2\n".format(script)
script = "{}modsdir=$3\n".format(script)
script = "{}echo \"Game will be cloned into $gamedir\"\n".format(script)
script = "{}\n".format(script)

script = "{}# game\n".format(script)
script = "{}echo \"Getting game\"\n".format(script)
if game_repo:
  script = "{}# {}\n".format(script, game_repo)
  script = "{}repodir=$gamedir/$gameid\n".format(script)
  script = "{}{}".format(script, repo_update_path_to_script(game_repo, "game"))
else:
  raise Exception("No game repository has been detected. \"{}\"".format(game_repo))

script = "{}\n".format(script)

for repo_path in mod_repos.keys():
  mods = mod_repos[repo_path]
  script = "{}# mods {}\n".format(script, ", ".join(mods))
  script = "{}echo \"Getting mods {}\"\n".format(script, ", ".join(mods))
  script = "{}# {}\n".format(script, repo_path)
  mod_name = mods[0]
  if (len(mods)>0):
    mod_name = pathlib.PurePath(repo_path)
    mod_name = mod_name.parts[-1]
  script = "{}repodir=$modsdir/{}\n".format(script, mod_name)
  script = "{}{}".format(script, repo_update_path_to_script(repo_path, mod_name))
    

for mod_name in no_repos.keys():
  mod_path = no_repos[mod_name]
  conf_path = "{}/mod.conf".format(mod_path)
  release = False
  author = None
  if os.path.exists(conf_path):
    conf = open(conf_path, "r")
    lines = conf.readlines()
    conf.close()
    for line in lines:
      if line.startswith("release = "):
        release = True
      if line.startswith("author = "):
        author = line[9:-1]
  script = "{}# mod {}\n".format(script, mod_name)
  script = "{}echo \"Getting mod {}\"\n".format(script, mod_name)
  if release and author:
    script = "{}moddir=$modsdir/{}\n".format(script, mod_name)
    script = "{}wget -O \"$modsdir/{}.zip\" https://content.minetest.net/packages/{}/{}/download/\n".format(script, mod_name, author, mod_name)
    script = "{}if [ -f \"$modsdir/{}.zip\" ]; then\n".format(script, mod_name)
    script = "{}  rm -fr \"$moddir\"\n".format(script)
    script = "{}  unzip -d \"$modsdir\" \"$modsdir/{}.zip\"\n".format(script, mod_name)
    script = "{}  rm \"$modsdir/{}.zip\"\n".format(script, mod_name)
    script = "{}fi\n".format(script)
    
  else:
    script = "{}# place insert code for mod {} here\n\n".format(script, mod_name, mod_name)
  print("WARNING: Mod {} in directory \"{}\" is not maintained by GIT. It have to be added manualy to script.".format(mod_name, mods_names[mod_name]))

script = "{}# game commit check\n".format(script)
script = "{}repodir=$gamedir/$gameid\n".format(script)
script = "{}{}".format(script, repo_check_commit(game_repo, "game"))

for repo_path in mod_repos.keys():
  mods = mod_repos[repo_path]
  script = "{}# mods {} commit check\n".format(script, ", ".join(mods))
  mod_name = mods[0]
  if (len(mods)>0):
    mod_name = pathlib.PurePath(repo_path)
    mod_name = mod_name.parts[-1]
  script = "{}repodir=$modsdir/{}\n".format(script, mod_name)
  script = "{}{}".format(script, repo_check_commit(repo_path, mod_name))

output_file = open(sys.argv[2], "w");
output_file.write(script);
output_file.close();

