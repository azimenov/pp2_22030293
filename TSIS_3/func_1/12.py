def histo(counts):
    for item in counts:
        for i in range(item):
            print('*', end = '')
        print()

histo([1,2,4])