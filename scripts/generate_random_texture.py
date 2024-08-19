#!/bin/python

import sys
import subprocess
import os.path
import pathlib
import random

from PIL import Image

if (len(sys.argv)<7):
  print("Usage: generate_random_texture.py new_texture.png from_texture.png palette_texture.png palette_layers.png combine_texture.png seed")
  print("")
  print("  palette_layers.png -> use NO, to disable")
  print("  combine_texture.png -> use NO, to disable")
  print("  ignore_border -> value bigger then zero decrease effective are of palette by selected number of pixels from every border")
  exit();


from_file = Image.open(sys.argv[2]).convert("RGBA");
palette_file = Image.open(sys.argv[3]).convert("RGBA");
layers_file = None
if (sys.argv[4]!="NO"):
  layers_file = Image.open(sys.argv[4]).convert("RGBA");
  if (palette_file.width!=layers_file.width):
    print("Size of palette_texture and palette_layers must be equal.")
    exit()
  if (palette_file.height!=layers_file.height):
    print("Size of palette_texture and palette_layers must be equal.")
    exit()
combine_file = None
if (sys.argv[5]!="NO"):
  combine_file = Image.open(sys.argv[5]).convert("RGBA");
  if (from_file.width!=combine_file.width):
    print("Size of from_texture and combine_texture must be equal.")
    exit()
  if (from_file.height!=combine_file.height):
    print("Size of from_texture and combine_texture must be equal.")
    exit()

randGen = random.Random(int(sys.argv[6]))

new_png = Image.new(mode="RGBA",size=(from_file.width,from_file.height),color=(0,0,0,255));
new_data = []

good_layers = {}

for from_y in range(from_file.height):
  for from_x in range(from_file.width):
    from_color = from_file.getpixel((from_x,from_y))
    new_color = [0,0,0,from_color[3]]
    if (new_color[3]>0):
      if layers_file!=None:
        while True:
          layer_key = "{}_{}_{}".format(from_color[0], from_color[1], from_color[2])
          palette_x = randGen.randrange(palette_file.width)
          palette_y = randGen.randrange(palette_file.height)
          layer_color = layers_file.getpixel((palette_x, palette_y))
          if layer_color[3]<255:
            continue
          if layer_key in good_layers:
            if layer_color[0]!=good_layers[layer_key][0]:
              continue
            if layer_color[1]!=good_layers[layer_key][1]:
              continue
            if layer_color[2]!=good_layers[layer_key][2]:
              continue
          else:
            good_layers[layer_key] = layer_color
          break
      else:
        palette_x = randGen.randrange(palette_file.width)
        palette_y = randGen.randrange(palette_file.height)
      palette_color = palette_file.getpixel((palette_x, palette_y))
      for c in range(3):
        new_color[c] = palette_color[c]
    if (combine_file!=None):
      combine_color = combine_file.getpixel((from_x,from_y))
      a1 = combine_color[3]/255.0
      a2 = (new_color[3]/255.0)*(1-a1)
      a0 = a1 + a2
      for c in range(3):
        if a1>0:
          new_color[c] = int((combine_color[c]*a1+new_color[c]*a2)/a0)
      if a1>0:
        new_color[3] = int(a0*255)
    new_data.append(tuple(new_color))

new_png.putdata(new_data)
new_png.save(sys.argv[1])

print("Generated texture has been saved into file: {}".format(sys.argv[1]))

