num_of_lower = 0
num_of_upper = 0

s = input()

for words in s:
    if s.isupper():
        num_of_upper += 1
    if s.islower():
        num_of_lower += 1


print(num_of_lower)
print(num_of_upper)