import math
import time

num = int(input())
time_of_delay = int(input())

time.sleep(time_of_delay/1000) 
print(f"{math.sqrt(num)} after {time_of_delay} milliseconds")