
def palindrome(str1):
    str2 = str1[::-1]
    return str2 == str1

str1 = str(input())

print(palindrome(str1))


