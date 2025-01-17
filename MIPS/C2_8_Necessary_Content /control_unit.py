control_word = {
    "0000": "0001000001001",
    "0001": "0000010001000",
    "0010": "0000000010001",
    "0011": "0001000001011",
    "0100": "0011000000100",
    "0101": "0001000001000",
    "0110": "0011000000010",
    "0111": "0001000001010",
    "1000": "0111000000110",
    "1001": "0011000000011",
    "1010": "1000000000000",
    "1011": "0111000000101",
    "1100": "0001101001000",
    "1101": "0011000000000",
    "1110": "0000000100001",
    "1111": "0011000000001",
}


filepath = "control_words.txt"
with open(filepath, "w") as my_file:
    my_file.write("v2.0 raw\n")
    for key in control_word:
        hex_val = hex(int(control_word[key], 2))[2:].zfill(4)
        my_file.write(hex_val + "\n")
