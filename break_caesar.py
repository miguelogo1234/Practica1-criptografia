from caesar import decrypt

#SACADO DE WIKIPEDIA
ENGLISH_FREQS = {'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074}

#SACADO DE WIKIPEDIA
SPANISH_FREQS = {'A': 0.1253, 'B': 0.0142, 'C': 0.0468, 'D': 0.0586, 'E': 0.1368,
    'F': 0.0069, 'G': 0.0101, 'H': 0.0070, 'I': 0.0625, 'J': 0.0044,
    'K': 0.0002, 'L': 0.0497, 'M': 0.0315, 'N': 0.0671, 'O': 0.0868,
    'P': 0.0251, 'Q': 0.0088, 'R': 0.0687, 'S': 0.0798, 'T': 0.0463,
    'U': 0.0393, 'V': 0.0090, 'W': 0.0001, 'X': 0.0022, 'Y': 0.0090,
    'Z': 0.0052}

def chi_squared(text: str, table: dict[str, float]) -> float:
    chi_sq = 0
    observed_counts = {}

    if not text:
        return 0

    for char in text:
        if char in table:
            observed_counts[char] = observed_counts.get(char, 0) + 1

    for char, expected_prob in table.items():
        expected_count = expected_prob * len(text)
        observed = observed_counts.get(char, 0)
        if expected_count > 0:
            chi_sq += ((observed - expected_count) ** 2) / expected_count

    return chi_sq / len(text)

def break_caesar(ciphertext: str, language: str = "en") -> tuple[int, str]:
    best_k = 0
    best_plaintext = ""
    lowest_chi_sq = float("inf")

    if language == "es":
        freq_table = SPANISH_FREQS
    else:
        freq_table = ENGLISH_FREQS

    for k in range(26):
        decrypted_text = decrypt(ciphertext, k)
        current_chi_sq = chi_squared(decrypted_text, freq_table)

        if current_chi_sq < lowest_chi_sq:
            lowest_chi_sq = current_chi_sq
            best_k = k
            best_plaintext = decrypted_text

    return best_k, best_plaintext