
sfence_help = {}

local function isFile(filename)
    file = io.open(filename);
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
        
        local list_text = "";
        for item_name in pairs(minetest.registered_items) do
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
