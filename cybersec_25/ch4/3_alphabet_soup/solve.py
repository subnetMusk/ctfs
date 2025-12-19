def subs_char(text, sub_dict):
    result = ""
    for c in text:
        if c in sub_dict:
            result += sub_dict[c]
        else:
            result += c

    return result

with open("encrypted.txt", "r") as f:
    content = f.read()

print(content)


print("--" * 3)

subs = {
    "K" : "I",
    "Q" : "M",
    "B" : "S",
    "T" : "U",
    "C" : "R",
    "U" : "E",
    "M" : "A",
    "D" : "O",
    "V" : "D",
    "L" : "H",
    "X" : "C",
    "W" : "N",
    "N" : "F",
    "J" : "Y"
}

print(subs_char(content, subs))