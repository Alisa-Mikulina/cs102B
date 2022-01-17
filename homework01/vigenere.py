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
    upper_index = ord("A")
    lower_index = ord("a")
    word_len = len(plaintext)
    key_len = len(keyword)
    shift = []
    for i in range(word_len):
        indexone = ord(plaintext[i])
        if plaintext[i].isupper():
            local_first = indexone - upper_index
            temporary_shift = local_first + (ord(keyword[i % key_len]) - upper_index)
            local_final = temporary_shift % 26
            shift.append(upper_index + local_final)
        elif plaintext[i].islower():
            local_first = indexone - lower_index
            temporary_shift = local_first + (ord(keyword[i % key_len]) - lower_index)
            local_final = temporary_shift % 26
            shift.append(lower_index + local_final)
        else:
            shift.append(indexone)

    for i in range(word_len):
        ciphertext += chr(shift[i])

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
    upper_index = ord("A")
    lower_index = ord("a")
    word_len = len(ciphertext)
    key_len = len(keyword)
    shift = []
    for i in range(word_len):
        indexone = ord(ciphertext[i])
        if ciphertext[i].isupper():
            local_first = indexone - upper_index
            temporary_shift = local_first - (ord(keyword[i % key_len]) - upper_index)
            if temporary_shift < 0:
                temporary_shift += 26
            local_final = temporary_shift % 26
            shift.append(upper_index + local_final)
        elif ciphertext[i].islower():
            local_first = indexone - lower_index
            temporary_shift = local_first - (ord(keyword[i % key_len]) - lower_index)
            if temporary_shift < 0:
                temporary_shift += 26
            local_final = temporary_shift % 26
            shift.append(lower_index + local_final)
        else:
            shift.append(indexone)
    for i in range(word_len):
        plaintext += chr(shift[i])

    return plaintext
