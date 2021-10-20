def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    line = []
    list_lower = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
    list_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    counter = 0
    shift = 0
    end_counter = len(keyword) - 1

    for char in plaintext:
        line.append(char)

    for i in range(len(line)):
        if not line[i].isnumeric():
            if line[i].isupper():
                shift = list_upper.index(keyword[counter].upper())
                line[i] = list_upper[list_upper.index(line[i]) + shift]
                if counter == end_counter:
                    counter = 0
                else:
                    counter += 1
            if line[i].islower():
                shift = list_lower.index(keyword[counter].lower())
                line[i] = list_lower[list_lower.index(line[i]) + shift]
                if counter == end_counter:
                    counter = 0
                else:
                    counter += 1

    for elem in line:
        ciphertext += elem
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    line = []
    list_lower = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
    list_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    counter = 0
    shift = 0
    end_counter = len(keyword) - 1

    for cha in ciphertext:
        line.append(cha)

    for i in range(len(line)):
        if not line[i].isnumeric():
            if line[i].isupper():
                shift = list_upper.index(keyword[counter].upper())
                line[i] = list_upper[list_upper.index(line[i]) - shift]
                if counter == end_counter:
                    counter = 0
                else:
                    counter += 1
            if line[i].islower():
                shift = list_lower.index(keyword[counter].lower())
                line[i] = list_lower[list_lower.index(line[i]) + shift]
                if counter == end_counter:
                    counter = 0
                else:
                    counter += 1

    plaintext = ""
    for elem in line:
        plaintext += elem

    return plaintext
