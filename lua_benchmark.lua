
-- done with Copilot AI

-- Function to measure execution time
local function measurePerformance(func, ...)
	local startTime = os.clock()
	func(...)
	local endTime = os.clock()
	return endTime - startTime
end

local function fibonacci(n)
	if n <= 1 then
		return n
	else
		return fibonacci(n - 1) + fibonacci(n - 2)
	end
end

local function partition(arr, low, high)
	local pivot = arr[high]
	local i = low - 1
	for j = low, high - 1 do
		if arr[j] <= pivot then
			i = i + 1
			arr[i], arr[j] = arr[j], arr[i]
		end
	end
	arr[i + 1], arr[high] = arr[high], arr[i + 1]
	return i + 1
end

local function quicksort(arr, low, high)
	if low < high then
		local pi = partition(arr, low, high)
		quicksort(arr, low, pi - 1)
		quicksort(arr, pi + 1, high)
	end
end

local function matrixMultiply(A, B)
	local C = {}
	for i = 1, #A do
		C[i] = {}
		for j = 1, #B[1] do
			C[i][j] = 0
			for k = 1, #B do
				C[i][j] = C[i][j] + A[i][k] * B[k][j]
			end
		end
	end
	return C
end

-- BINARY TREE

-- Define a node of the binary tree
local Node = {}
Node.__index = Node

function Node:new(value)
	local node = {
		value = value,
		left = nil,
		right = nil
	}
	setmetatable(node, Node)
	return node
end

-- Define the binary tree
local BinaryTree = {}
BinaryTree.__index = BinaryTree

function BinaryTree:new()
	local tree = {
		root = nil
	}
	setmetatable(tree, BinaryTree)
	return tree
end

function BinaryTree:insert(value)
	local newNode = Node:new(value)
	if self.root == nil then
		self.root = newNode
	else
	self:_insertNode(self.root, newNode)
	end
end

function BinaryTree:_insertNode(currentNode, newNode)
	if newNode.value < currentNode.value then
		if currentNode.left == nil then
			currentNode.left = newNode
		else
			self:_insertNode(currentNode.left, newNode)
		end
	else
		if currentNode.right == nil then
			currentNode.right = newNode
		else
			self:_insertNode(currentNode.right, newNode)
		end
	end
end

function BinaryTree:search(value)
	return self:_searchNode(self.root, value)
end

function BinaryTree:_searchNode(currentNode, value)
	if currentNode == nil then
		return false
	end
	if value == currentNode.value then
		return true
	elseif value < currentNode.value then
		return self:_searchNode(currentNode.left, value)
	else
		return self:_searchNode(currentNode.right, value)
	end
end

-- Create a binary tree and measure performance of insertions
function sfence_help.lua_benchmark(seed, runs, log_func)
	math.randomseed(seed)
	log_func("Start Lua benchmark for seed "..seed.." with "..runs.." runs.")
	local results = {}
	log_func("Start fibonacci")
	results["fibonacci"] = measurePerformance(function()
			for i = 1, runs do
				fibonacci(math.random(1, 20))
			end
		end)
	-- quick sort
	log_func("Start quicksort")
	results["quicksort"] = measurePerformance(function()
			for i = 1, runs do
				local array = {}
				for i = 1, 1000 do
					array[i] = math.random(1, 10000)
				end
				quicksort(array, 1, #array)
			end
		end)
	-- multiply matrix
	log_func("Start multiply matrix")
	results["matrixMultiply"] = measurePerformance(function()
			for i = 1, runs do
				local mA = {}
				local mB = {}
				for i = 1, 10 do
					mA[i] = {}
					mB[i] = {}
					for j = 1, 10 do
						mA[i][j] = math.random(1, 10000)
						mB[i][j] = math.random(1, 10000)
					end
				end
				matrixMultiply(mA, mB)
			end
		end)
	-- binary tree
	log_func("Start binary tree")
	local tree = BinaryTree:new()
	results["tree_insert"] = measurePerformance(function()
			for i = 1, runs do
				tree:insert(math.random(1, 10000))
			end
		end)

	-- Measure performance of search operations
	results["tree_search"] = measurePerformance(function()
			for i = 1, runs do
				tree:search(math.random(1, 10000))
			end
		end)
	log_func("End of Lua benchmark")
	return results
end

