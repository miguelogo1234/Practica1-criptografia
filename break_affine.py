from affine import decrypt
from break_caesar import chi_squared, ENGLISH_FREQS, SPANISH_FREQS

def break_affine(ciphertext: str, language: str = "en") -> tuple[tuple[int, int], str]:
    if language == "es":
        freq_table = SPANISH_FREQS
    else:
        freq_table = ENGLISH_FREQS

    best_key = (0, 0)
    best_text = ""
    lowest_chi = float("inf")

    valid_a_values = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    for a in valid_a_values:
        for b in range(26):
            decrypted_text = decrypt(ciphertext, a, b)

            current_chi = chi_squared(decrypted_text, freq_table)
            if current_chi < lowest_chi:
                lowest_chi = current_chi
                best_key = (a, b)
                best_text = decrypted_text

    return best_key, best_text