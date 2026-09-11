def twoSum(nums: list[int], target: int) -> list[int]:
    num_set = set(nums)
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_set and complement != num:
            return [i, nums.index(complement)]
    return []


print(twoSum([2, 7, 11, 15], 9))  # Output: [0, 1] 