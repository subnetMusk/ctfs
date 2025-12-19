def shift(s, pos):
    return "".join(chr(ord(c) + pos) for c in s)

string = input("Enter a string: ")

print("Original: ", string, " // Shifted: ", shift(string, 2))


