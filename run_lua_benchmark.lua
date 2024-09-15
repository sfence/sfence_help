
-- standalone performance run

if #arg < 2 then
	print("Use lua performance_run.lua seed runs")
else
	local scriptDir = arg[0]
	scriptDir = scriptDir:match("(.*/)")
	if scriptDir==nil then
		scriptDir = "./"
	end
	sfence_help = {}

	dofile(scriptDir.."lua_benchmark.lua")

	seed = tonumber(arg[1])
	runs = tonumber(arg[2])
	local results = sfence_help.lua_benchmark(seed, runs, print)
	local sum = 0
	for key, value in pairs(results) do
		print(key..": "..value)
		sum = sum + value
	end
	print("Total time: "..sum)
end
