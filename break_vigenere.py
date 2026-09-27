from break_caesar import break_caesar
from vigenere import decrypt, cosets

def break_vigenere(ciphertext: str, m: int, language: str = "en") -> tuple[str, str]:
    text_cosets = cosets(ciphertext, m)
    key_letters = []
    for coset in text_cosets:
        best_k, _ =  break_caesar(coset, language)
        key_letters.append(chr(best_k + 65))

    key = "".join(key_letters)
    plaintext = decrypt(ciphertext, key)

    return key, plaintext