# All loops in one file

# for loop - Iterating over a list
numbers = [1, 2, 3, 4]
for num in numbers:
    print(f"For loop: {num}")

# for loop - Using range
for i in range(5):
    print(f"Range loop: {i}")

# while loop
i = 0
while i < 5:
    print(f"While loop: {i}")
    i += 1

# Nested for loops
for i in range(3):
    for j in range(2):
        print(f"Nested for loop: i={i}, j={j}")

# Nested while loops
i = 0
while i < 3:
    j = 0
    while j < 2:
        print(f"Nested while loop: i={i}, j={j}")
        j += 1
    i += 1

# break statement
for i in range(5):
    if i == 3:
        break
    print(f"Break example: {i}")

# continue statement
for i in range(5):
    if i == 3:
        continue
    print(f"Continue example: {i}")
