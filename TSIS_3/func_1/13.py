import random
print("Hello! What is your name?")
name = input()

number = random.randint(1,20)
counter = 0
print(f"Well, {name}, I am thinking of a number between 1 and 20. \nTake a guess.")

while(True):
    a = int(input())
    counter += 1
    if a > number:
        print("Your guess is too high. \nTake a guess.")
    elif a < number:
        print("Your guess is too low. \nTake a guess.")
    elif a == number:
        print(f"Good job, {name}! You guessed my number in {counter} guesses!")
        break
