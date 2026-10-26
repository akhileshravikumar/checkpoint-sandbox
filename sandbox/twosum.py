def twoSum(nums: list[int], target: int) -> list[int]:
    if not nums:
        raise ValueError("Input list 'nums' must not be empty.")
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[j] == target - nums[i]:
                return [i, j]
    return []


print(twoSum([2, 7, 11, 15], 9))  # Output: [0, 1] 