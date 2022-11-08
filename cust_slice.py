def cust_slice(it_obj, start, stop, step=1):

    for num in range(2, 8):
        print(num)


nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]


output = cust_slice(nums, 2, 10)

print(f"My Slice: {output}")
print(f"Py's Slice: {nums[2:-2:]}")

# print(output)
# Output
[3, 4, 5, 6, 7]

## Example 2
# print(cust_slice(nums, stop=4))


# Output
[1, 2, 3, 4]

## Example
# print(cust_slice(nums, step=-1))

# Output
[9, 8, 7, 6, 5, 4, 3, 2, 1]
