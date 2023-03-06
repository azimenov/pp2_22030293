with open('text.txt', 'r') as fr:
    with open('text_copy.txt', 'w') as fw:
        for line in fr:
            fw.write(line)
