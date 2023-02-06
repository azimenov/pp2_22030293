class printer:
    name = ""
    def getString(self):
        printer.name = input()
    def PrintString(self):
        return (printer.name).upper()


p1 = printer()
p1.getString()
print(p1.PrintString())

