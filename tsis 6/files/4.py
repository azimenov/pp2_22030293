with open('text.txt', 'r') as f:
    counter = 0
    for line in f:
        counter += 1

    print(counter)