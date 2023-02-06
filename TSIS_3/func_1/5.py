from itertools import permutations
def permut(str1):
    return list(permutations(str1, len(str1)))

print(permut("abba"))