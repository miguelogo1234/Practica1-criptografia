from basics import to_letters, to_numbers, normalize

def validateKey(key: str):
    if not key or not key.isalpha():
        raise ValueError("Invalid key")

def encrypt(plaintext: str, key: str) -> str:
    plaintext = normalize(plaintext)
    validateKey(key)
    plain_nums = to_numbers(plaintext)
    key_nums = to_numbers(key)
    encrypt_nums = []
    for i, num in enumerate(plain_nums):
        shift = key_nums[i % len(key_nums)]
        encrypt_num = (num + shift) % 26
        encrypt_nums.append(encrypt_num)

    return to_letters(encrypt_nums)

def decrypt(ciphertext: str, key: str) -> str:
    validateKey(key)
    cipher_num = to_numbers(ciphertext)
    key_nums = to_numbers(key)
    decrypt_nums = []
    for i, num in enumerate(cipher_num):
        shift = key_nums[i % len(key_nums)]
        decrypt_num = (num - shift) % 26
        decrypt_nums.append(decrypt_num)

    return to_letters(decrypt_nums)

def cosets(ciphertext: str, m: int) -> list[str]:
    coset = []
    for i in range(m):
        cos = ciphertext[i::m]
        coset.append(cos)
    return coset

#print(encrypt("MYSECRETMESSAGE", "KEY"))
#print(encrypt("ATTACKATDAWN", "LEMON"))
#print(decrypt("WCQOGPOXKOWQKKC", "KEY"))
#print(decrypt("LXFOPVEFRNHR", "LEMON"))
#print(cosets("ABCDEF", 3))