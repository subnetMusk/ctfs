end = False

while not end:
    input1 = int(input("Enter a number: "))
    input2 = int(input("Enter another number: "))

    print("Operations:\n"
          "0) SUM\n"
          "1) SUB\n"
          "2) MUL\n"
          "3) DIV\n"
          "4) END\n"
    )
    op = int(input())

    print("Result: ", end=" ")
    if op == 0:
        print(input1 + input2)
    if op == 1:
        print(input1 - input2)
    if op == 2:
        print(input1 * input2)
    if op == 3:
        if input2 != 0:
            print(input1 / input2)
        else:
            print("Cannot divide by zero")
    if op == 4:
        end = True

    print("\n")