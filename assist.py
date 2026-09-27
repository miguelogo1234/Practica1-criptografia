import collections
from basics import normalize

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

def report(ciphertext: str, language: str = "en") -> str:
    text = normalize(ciphertext)
    if language == "es":
        expected_freqs = sorted(SPANISH_FREQS.items(), key = lambda x: x[1], reverse = True)
    else: 
        expected_freqs = sorted(ENGLISH_FREQS.items(), key = lambda x: x[1], reverse = True)

    output = []
    output.append(f"--- Frequency report ({language.upper()}) ---")
    output.append(f"Total length: {len(text)}\n")
    output.append("1. Letter frequencies:")
    counts = collections.Counter(text)
    ranked_cipher = counts.most_common()
    suggested_mapping = {}

    for i in range(len(ranked_cipher)):
        cipher_char, count = ranked_cipher[i]
        percent = (count/ len(text)) * 100
        expected_char, expected_percent = expected_freqs[i] if i < len(expected_freqs) else ("?", 0)
        suggested_mapping[cipher_char] = expected_char
        output.append(f"  {cipher_char}: {count:3} ({percent:5.1f}%)  -->  Expected: {expected_char} ({expected_percent*100:5.1f}%)")

    output.append("\n2. Repeated trigram")
    trigrams = collections.defaultdict(list)
    for i in range(len(text) - 2):
        triagram = text[i: i + 3]
        trigrams[triagram].append(i)

    repeated_trigrams = {k: v for k, v in trigrams.items() if len(v) > 1}
    for tri, positions in sorted(repeated_trigrams.items(), key=lambda x: len(x[1]), reverse=True):
        output.append(f"  {tri}: {len(positions)} veces en posiciones {positions}")

    output.append("\n3. Top 10 bigrams:")
    bigrams = [text[i:i+2] for i in range(len(text) - 1)]
    top_bigrams = collections.Counter(bigrams).most_common(10)
    for bi, count in top_bigrams:
        output.append(f"  {bi}: {count}")

    output.append("\n4. Double letter:")
    doubles = collections.Counter([text[i:i+2] for i in range(len(text) - 1) if text[i] == text[i+1]])
    for dbl, count in doubles.items():
        output.append(f"  {dbl}: {count}")

    output.append("\n5. Suggested initial mapping:")
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mapping_str = ""
    for char in alphabet:
        if char in suggested_mapping:
             mapping_str += f"{char}->{suggested_mapping[char]} "
    output.append(f"  {mapping_str}")
        
    return "\n".join(output)

cryptogram = """QATNT YSMHQ XJOCY HKATM FSNQI TUTMP TKTIP JIDTT KHIGQ ATCEG
JMHQA FNTYM TQRTY CSNTJ IEXQA TDTXY CIRTY ACIGT PVATI HQHNY
JFKMJ FHNTP"""

#print(report(cryptogram, "en"))