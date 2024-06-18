import heapq
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
# 常见的heapq操作
heapq.heapify(nums)
print(nums)
print(heapq.heappop(nums))
print(heapq.heappop(nums))