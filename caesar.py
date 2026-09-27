from basics import to_numbers, to_letters, normalize

def encrypt(plaintext: str, k: int) -> str:
    plaintext = normalize(plaintext)
    numbers = to_numbers(plaintext)
    encrypted_nums = []
    for num in numbers:
        encrypted_num = (num + k) % 26
        encrypted_nums.append(encrypted_num)
    return to_letters(encrypted_nums)


def decrypt(chipertext: str, k: int) -> str:
    numbers = to_numbers(chipertext)
    decrypt_numbers = []
    for num in numbers:
        decrypt_num = (num - k) % 26
        decrypt_numbers.append(decrypt_num)
    return to_letters(decrypt_numbers)

#print(encrypt("MYSECRETMESSAGE", 3))
#print(decrypt("PBVHFUHWPHVVDJH", 3))