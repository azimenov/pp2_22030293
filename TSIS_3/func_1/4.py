def isPrime(check_num):
    a = int(check_num)
    if a > 1:
        for j in range(2, int(a/2)+1):
            if (a % j) == 0:
                return False
        return True
    else:
        return True

def filter_prime(my_list):
    result = []
    for iter in my_list:
        if isPrime (iter):
            result.append((iter))
    return result
            

my_list = input().split(' ')
print((filter_prime(my_list)))
