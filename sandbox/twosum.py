def twoSum(nums: list[int], target: int) -> list[int]:
    """
    Finds two numbers in the list `nums` that add up to the `target` value.
    
    Parameters:
    nums (list[int]): A list of integers.
    target (int): The target sum to find.
    
    Returns:
    list[int]: A list containing the indices of the two numbers that add up to the target.
    """
    num_set = set()
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_set:
            return [num_set[complement], i]
        num_set[num] = i
    return []


print(twoSum([2, 7, 11, 15], 9))  # Output: [0, 1] 