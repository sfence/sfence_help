
sfence_help = {}

local function isFile(filename)
    local file = io.open(filename);
    if (file==nil) then 
      return false;
    end
    io.close(file);
    return true;
  end


local command_print_all_items = {
    params = "<file>",
    description = "Save list of all registered item names to file <file>",
    privs = nil,
    func = function (name, param)
        -- check param
        if (param==nil) or (param=="") then
          return false, "Use /print_all_items filename";
        end
        -- command body
        local filename = minetest.get_worldpath().."/"..param;
        
        local use_items = {};
        for item_name in pairs(minetest.registered_items) do
          table.insert(use_items, item_name);
        end
        table.sort(use_items);
        local list_text = "";
        for index, item_name in pairs(use_items) do
          list_text = list_text..item_name.."\n";
        end
        
        if isFile(filename) then
          return false, "File \""..filename.."\" already exists!";
        end

        local file = io.open(filename,"w");
        file:write(list_text);
        file:close();
        return true, "List of registered items saved to file \""..filename.."\".";
      end
  };
minetest.register_chatcommand("print_all_items", command_print_all_items)

local command_print_all_recipes = {
    params = "<file>",
    description = "Save list of all registered recipes to file <file>",
    privs = nil,
    func = function (name, param)
        -- check param
        if (param==nil) or (param=="") then
          return false, "Use /print_all_recipes filename";
        end
        -- command body
        local filename = minetest.get_worldpath().."/"..param;
        
        local use_items = {};
        for item_name in pairs(minetest.registered_items) do
          table.insert(use_items, item_name);
        end
        table.sort(use_items);
        local list_text = "";
        for index, item_name in pairs(use_items) do
          local recipes = minetest.get_all_craft_recipes(item_name);
          if (recipes~=nil) then
            for key, recipe in pairs(recipes) do
              list_text = list_text..dump(recipe).."\n";
            end
          end
        end
        
        if isFile(filename) then
          return false, "File \""..filename.."\" already exists!";
        end

        local file = io.open(filename,"w");
        file:write(list_text);
        file:close();
        return true, "List of registered recipes saved to file \""..filename.."\".";
      end
  };
minetest.register_chatcommand("print_all_recipes", command_print_all_recipes)

local command_find_nearby_node = {
    params = "<nodename>",
    description = "Print location of first found node with name <nodename>",
    privs = nil,
    func = function (name, param)
        -- check param
        if (param==nil) or (param=="") then
          return false, "Use /find_nearby_node nodename";
        end
        
        local player = minetest.get_player_by_name(name);
        local find_pos = minetest.find_node_near(player:get_pos(), 128, param);
        if (find_pos==nil) then
          return false, "Node "..param.." not found in radius 128";
        end
        return true, "Node "..param.." found at x="..find_pos.x.." y="..find_pos.y.." z="..find_pos.z;
      end
  };
minetest.register_chatcommand("find_nearby_node", command_find_nearby_node)

local command_print_definition_node = {
    params = "<nodename>",
    description = "Print <nodename> definition like warning to server terminal.",
    privs = nil,
    func = function (name, param)
        -- check param
        if (param==nil) or (param=="") then
          return false, "Use /print_definition_node nodename";
        end
        
        local node_def = minetest.registered_items[param];
        if node_def then
          minetest.log("warning", param..":\n"..dump(node_def));
          return true, "Node definition has been printed into server terminal like warning.";
        else
          return false, "Node "..param.." definition not found.";
        end
      end
  };
minetest.register_chatcommand("print_definition_node", command_print_definition_node)

local command_print_node = {
    params = "<position>",
    description = "Print <positon> node data like warning to server terminal.",
    privs = nil,
    func = function (name, param)
        -- check param
        if (param==nil) or (param=="") then
          return false, "Use /print_node position";
        end
        
        local node_pos = minetest.string_to_pos(param)
        if node_pos==nil then
          return false, "Position "..param.." failed to conversion to pos.";
        end
        local node_data = minetest.get_node(node_pos);
        if node_data then
          local node_meta = minetest.get_meta(node_pos):to_table();
          minetest.log("warning", param..":\n"..dump(node_data));
          minetest.log("warning", param..":\n"..dump(node_meta));
          return true, "Node data has been printed into server terminal like warning.";
        else
          return false, "Node "..param.." data not found.";
        end
      end
  };
minetest.register_chatcommand("print_node", command_print_node)

