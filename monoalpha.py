from basics import to_letters, to_numbers, normalize

def validateKey(key: str):
    if len(key) != 26 or len(set(key)) != 26 or not all(c.isupper() and "A" <= c <= "Z" for c in key):
        raise ValueError("Invalid key")

def encrypt(plaintext: str, key: str) -> str:
    plaintext = normalize(plaintext)
    validateKey(key)

    numbers = to_numbers(plaintext)
    encrypt_text = ""

    for num in numbers:
        encrypt_text += key[num]

    return encrypt_text

def decrypt(ciphertext: str, key: str) -> str:
    validateKey(key)

    decrypt_nums = []
    for char in ciphertext:
        original_num = key.index(char)
        decrypt_nums.append(original_num)

    return to_letters(decrypt_nums)

def key_from_keyword(keyword: str) -> str:
    key_chars = []
    for char in keyword:
        if char not in key_chars:
            key_chars.append(char)

    for i in range(26):
        alphabet_char = chr(i + 65)
        if alphabet_char not in key_chars:
            key_chars.append(alphabet_char)

    return "".join(key_chars)

#print(encrypt("HELLO", "MNBVCXZASDFGHJKLPOIUYTREWQ"))
#print(decrypt("ACGGK", "MNBVCXZASDFGHJKLPOIUYTREWQ"))
#print(encrypt("BOB", "MNBVCXZASDFGHJKLPOIUYTREWQ"))
#print(decrypt("NKN", "MNBVCXZASDFGHJKLPOIUYTREWQ"))
#print(key_from_keyword("CRYPTO"))