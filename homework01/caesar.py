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
    listlower = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
    listupper = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(len(plaintext)):
        changed_letter = plaintext[i]
        if changed_letter.isupper():
            indexone = listupper.find(changed_letter)
            index = indexone + (shift % 26)
            ciphertext += listupper[index]
        elif changed_letter.islower():
            indexone = listlower.find(changed_letter)
            index = indexone + (shift % 26)
            ciphertext += listlower[index]
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
    listlower = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
    listupper = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(len(ciphertext)):
        changed_letter = ciphertext[i]
        if changed_letter.isupper():
            indexone = listupper.find(changed_letter)
            index = indexone - (shift % 26)
            plaintext += listupper[index]
        elif changed_letter.islower():
            indexone = listlower.find(changed_letter)
            index = indexone - (shift % 26)
            plaintext += listlower[index]
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