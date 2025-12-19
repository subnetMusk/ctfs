def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


def inv_shift_rows(s):
    """
    Esegue l'Inverse ShiftRows assumendo che lo shift avvenga sulle colonne.
    Colonna 0: shift di 0
    Colonna 1: shift di 1
    ...
    """
    num_rows = len(s)
    num_cols = len(s[0])

    # Iteriamo su ogni colonna (indice 'c')
    for c in range(num_cols):
        # 1. Estraiamo la colonna c corrente in una lista
        #    (s[0][c], s[1][c], s[2][c], s[3][c])
        col = [s[r][c] for r in range(num_rows)]

        # 2. Applichiamo lo shift verso il basso
        #    Lo shift dipende dall'indice della colonna (c)
        #    formula: lista[-k:] + lista[:-k] sposta a destra (che qui è "basso")
        shift = c
        shifted_col = col[-shift:] + col[:-shift]

        # 3. Reinseriamo la colonna shiftata nella matrice originale
        for r in range(num_rows):
            s[r][c] = shifted_col[r]
    return s

# learned from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def mix_single_column(a):
    # see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)


def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])


def inv_mix_columns(s):
    # see Sec 4.1.3 in The Design of Rijndael
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v

    mix_columns(s)


state = [
    [108, 106, 71, 86],
    [96, 62, 38, 72],
    [42, 184, 92, 209],
    [94, 79, 8, 54],
]

mat = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

inv_mix_columns(state)
inv_shift_rows(state)
for r in state:
    for c in r:
        print(chr(c), end="")