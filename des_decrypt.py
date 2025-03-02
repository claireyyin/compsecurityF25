# DES Decryption Program
# Claire Yin
# Tables
# Initial Permutation Table
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]
#Permutations 1, 56 bits
PC1 = [
        57, 49,	41,	33,	25,	17,	9,
        1,	58,	50,	42,	34,	26,	18,
        10,	2,	59, 51,	43,	35,	27,
        19,	11,	3,	60,	52,	44,	36,
        63,	55,	47,	39,	31,	23,	15,
        7,	62,	54,	46,	38,	30,	22,
        14,	6,	61,	53,	45,	37,	29,
        21,	13,	5,	28,	20,	12,	4]
# Permutation 2, 48 bits
PC2 = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32]
# Number of bit shifts for roundkey generation
shifts =       [1,
               1,
               2,
               2,
               2,
               2,
               2,
               2,
               1,
               2,
               2,
               2,
               2,
               2,
               2,
               1]

# S boxes Tables
s_tables = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

# E Bit-selection table
E_table = [
    32, 1, 2, 3, 4, 5, 4, 5,
    6, 7, 8, 9, 8, 9, 10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 1
]

# P permutation
P_table = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]
# Final Permutation
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

# Permute input based on table
def permutation(key, table, bits):
    if bits != len(table):
        return print("Incorrect bit size")
    p = []
    for i in range (0, bits):
        p.append(key[table[i] - 1])
    return p

# Function to shift bits
def shift_left(block, n_shift):
    return block[n_shift:] + block[:n_shift]

# 16 rounds to generate subkeys
def generate_subkeys(L, R, shifts):
    rks = []
    for i in range(16): # 16 rounds
        print("Round: ", i+1)
        L = shift_left(L, shifts[i])
        R = shift_left(R, shifts[i])
        print("L: ", "".join(L))
        print("R: ", "".join(R))
        round_key = permutation(L + R, PC2, 48)
        print(f"Round key {i+1}: ", "".join(round_key))
        rks.append(round_key)
    return rks

# XOR function for two binary strings
def xor(a, b):
    c = []
    for i in range(len(a)):
        if a[i] == b[i]:
            c.append('0')
        else:
            c.append('1')
    return c

# f function
def f_function(R, round_key):
    expand_R = permutation(R, E_table, 48)
    xor_R = xor(expand_R, round_key) # Ki XOR E(Ri)
    s_box_output = s_box(xor_R, s_tables) # apply 8 s boxes
    output = permutation(s_box_output, P_table, 32)
    print("f_function output: ", "".join(output))
    return output

# Apply 8 s_boxes
def s_box(R_K, s_tables):
    output = []
    for i in range(8):
        chunk = R_K[i * 6:(i + 1) * 6]  # Input every 6 bits
        # convert to binary to int
        row = int(chunk[0] + chunk[5], 2) # first and last digit
        col = int("".join(chunk[1:5]), 2) # middle digits
        s_val = s_tables[i][row][col]  # Get S-Box value
        output.extend(f"{s_val:04b}")  # Convert back to binary 4-bits
    return output

# Decrypt the message
def des_decrypt(ciphertext, round_keys):
    ciphertext = permutation(ciphertext, initial_perm, 64)
    L= ciphertext[:32]
    R= ciphertext[32:]
    # iterate 16 times and decrypt
    for i in range(16):
        print("Iteration: ", i+1)
        prev_R = R
        R = xor(L, f_function(R, round_keys[i]))
        L = prev_R
    decrypted_bin = permutation(R+L, final_perm, 64)
    return decrypted_bin

# Convert binary to text
def binary_to_text(binary_str):
    # Check if binary string length is a multiple of 8
    if len(binary_str) % 8 != 0:
        raise ValueError("Binary string length must be a multiple of 8")
    # Split the binary string into 8-bits and convert each to a character
    text = ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))
    return text

# Deciphered DES enciphered message
ciphertext_bin = "1100101011101101101000100110010101011111101101110011100001110011"
key_bin = "0100110001001111010101100100010101000011010100110100111001000100"

PC1_key = permutation(key_bin, PC1, 56)
# Split in half
C_0=PC1_key[:28] # left
D_0=PC1_key[28:] # right
print("Initial C0: ", "".join(C_0))
print("Initial D0: ", "".join(D_0))
subkeys = generate_subkeys(C_0, D_0, shifts) # generate roundkeys
subkeys.reverse()  # Reverse roundkeys for decryption

deciphered = des_decrypt(ciphertext_bin, subkeys)
d= "".join(deciphered)
print("Binary deciphered: ", d)
print("Deciphered message: ", binary_to_text(d))
