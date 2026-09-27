from basics import to_numbers, to_letters, egcd, modinv, normalize

def validateA(a: int):
    gcdValue, x, y = egcd(a, 26)
    if gcdValue != 1:
        raise ValueError("Invalid key")

def encrypt(plaintext: str, a: int, b: int) -> str:
    plaintext = normalize(plaintext)
    validateA(a)
    number = to_numbers(plaintext)
    encrypt_nums = []
    for num in number:
        encrypt_num = (a * num + b) % 26
        encrypt_nums.append(encrypt_num)

    return to_letters(encrypt_nums)

def decrypt(ciphertext: str, a: int, b: int) -> str:
    validateA(a)
    a_inv = modinv(a, 26)
    number = to_numbers(ciphertext)
    dencrypt_nums = []

    for num in number:
        dencrypt_num = (a_inv * ( num - b)) % 26
        dencrypt_nums.append(dencrypt_num)
    
    return to_letters(dencrypt_nums)

def valid_keys() -> list[tuple[int, int]]:
    keys = []
    for a in range(26):
        gcd_value, _, _ = egcd(a, 26)
        if gcd_value == 1:
            for b in range(26):
                keys.append((a, b))

    return keys

#print(encrypt("ATTACK", 5, 8))