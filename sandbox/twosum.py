def twoSum(nums: list[int], target: int) -> list[int]:
    """
    Finds two numbers in the list `nums` that add up to the `target` value.
    
    Parameters:
    nums (list[int]): A list of integers.
    target (int): The target sum to find.
    
    Returns:
    list[int]: A list containing the indices of the two numbers that add up to the target.
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[j] == target - nums[i]:
                return [i, j]
    return []


print(twoSum([2, 7, 11, 15], 9))  # Output: [0, 1] 