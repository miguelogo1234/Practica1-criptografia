def to_numbers(text: str) -> list[int]: # normalised text -> 0.25
    numbers = []
    for letter in text:
        value = ord(letter)
        final_valuee = value - 65
        numbers.append(final_valuee)
    return numbers

def to_letters(nums: list[int]) -> str: # 0..25 -> text
    result_text = ""
    for num in nums:
        value = num + 65
        letter = chr(value)
        result_text += letter
    return result_text

def egcd(a: int, b: int) -> tuple[int, int, int]:
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1
    while b != 0:
        quotient = a//b
        remiender = a %b

        a = b
        b = remiender
        next_x = x0 - quotient * x1
        x0 = x1
        x1 = next_x
        next_y = y0 - quotient * y1
        y0 = y1
        y1 = next_y
        
    if a < 0:
        a = -a
        x0 = -x0
        y0 = -y0
    return (a, x0, y0)
    

def modinv(a: int, m: int) -> int:
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist. The gcd of {a} and {m} is {gcd}, not 1.")
    inverse = x % m
    return inverse

def xor_bytes(data: bytes, key: bytes) -> bytes: # key repeats cyclically
    result = bytearray()
    for i in range(len(data)):
        xored_byte = data [i] ^ key[i % len(key)]
        result.append(xored_byte)
    return bytes(result)

def normalize(text: str) -> str:
    return "".join(char for char in text.upper() if "A" <= char <= "Z")


text = "HELLOWORLD"
#print(to_numbers(text))
text2 = [7, 4, 11, 11, 14, -33, 22, 14, 17, 11, 3]
#print(to_letters(text2))
#print(egcd(17, 5))
#print(modinv(5, 26))
#print(modinv(7, 26))
#print(modinv(17, 26))
#print(modinv(13, 26))
#print(modinv(2, 26))
#print(xor_bytes(b"HELLO", b"KEYKE").hex())