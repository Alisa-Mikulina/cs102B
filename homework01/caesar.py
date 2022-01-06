import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    upper_index = ord("A")
    lower_index = ord("a")
    for changed_letter in plaintext:
        indexone = ord(changed_letter)
        if changed_letter.isupper():
            local_first = indexone - upper_index
            temporary_shift = local_first + shift
            local_final = temporary_shift % 26
            index = upper_index + local_final
            ciphertext += chr(index)
        elif changed_letter.islower():
            local_first = indexone - lower_index
            temporary_shift = local_first + shift
            local_final = temporary_shift % 26
            index = lower_index + local_final
            ciphertext += chr(index)
        else:
            ciphertext += changed_letter
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    upper_index_start = ord("A")
    lower_index_start = ord("a")
    for changed_letter in ciphertext:
        indexone = ord(changed_letter)
        if changed_letter.isupper():
            local_first = indexone - upper_index_start
            temporary_shift = local_first - shift
            if temporary_shift < 0:
                temporary_shift += 26
            local_final = temporary_shift % 26
            index = upper_index_start + local_final
            plaintext += chr(index)
        elif changed_letter.islower():
            local_first = indexone - lower_index_start
            temporary_shift = local_first - shift
            if temporary_shift < 0:
                temporary_shift += 26
            local_final = temporary_shift % 26
            index = lower_index_start + local_final
            plaintext += chr(index)
        else:
            plaintext += changed_letter
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
