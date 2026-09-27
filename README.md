# Cryptography: Substitution Ciphers and Cryptanalysis

## 1. How to run everything
To run the unified command-line interface (crypto.py), use the following verbatim commands:
*    Encrypt/Decrypt: `python crypto.py caesar encrypt --key 3 --in message.txt`
*    Break ciphers: `python crypto.py break vigenere --m 5 --in cipher.txt`
*    Frequency assistant: `python crypto.py assist --in cipher.txt`

To run the automated test suite (covering round-trip correctness, known check values, key validation, edge cases, and breaker reliability):
    `python -m unittest tests/test_ciphers.py`

## 2. Key space size for each of the four ciphers
* **Caesar cipher:** The key space size is 26, as the key is a single integer $k$ in the range of 0 to 25. In practice, there are 25 useful keys, since $k=0$ leaves the text unaltered.
* **Affine cipher:** The key space consists of 312 valid keys. The key requires two values, $a$ and $b$. The multiplier $a$ must be coprime to 26, leaving 12 possible values (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25). The shift $b$ can be any number from 0 to 25 (26 options). Multiplying these choices (12 * 26) yields 312.
* **Vigenère cipher:** The key space depends on the key length $m$. Since each position can be any of the 26 letters, the total number of possible combinations is $26^m$.
* **Monoalphabetic cipher:** The key space is a full permutation of the 26-letter alphabet, which equals $26! \approx 4.03 \times 10^{26}$ possible keys.

## 3. C1 Measurement Table
```
CASE 1: English text vs English table
  Length  20:  95.00% exit
  Length  30:  98.50% exit
  Length  40:  99.50% exit
  Length  60: 100.00% exit
  Length 100: 100.00% exit
CASE 2: Spanish text vs Spanish table
  Length  20:  94.00% exit
  Length  30:  91.50% exit
  Length  40:  94.50% exit
  Length  60:  93.50% exit
  Length 100:  97.00% exit
CASE 3: Spanish text vs English table
  Length  20:  90.00% exit
  Length  30:  96.00% exit
  Length  40: 100.00% exit
  Length  60: 100.00% exit
  Length 100: 100.00% exit
```
The experiments demonstrate that the attack becomes reliable (nearing 100% success) starting at a ciphertext length of about 30 characters. Counterintuitively, crossing languages (e.g., breaking a Spanish text using English expected frequencies) still maintains a near 100% success rate. This occurs because both languages share a very similar structural statistical "fingerprint": high peaks in the same vowels (A, E, O) and deep valleys for rare consonants (K, W, Z). The Chi-squared test is robust enough to align this statistical topography despite exact percentage differences.

## 4. C2 Comparison with C1
```
Case 1: English text vs English table
  Length  20:  69.00% exit
  Length  30:  85.00% exit
  Length  40:  95.50% exit
  Length  60:  99.50% exit
  Length 100: 100.00% exit
Case 2: Spanish text vs Spanish table
  Length  20:  78.50% exit
  Length  30:  91.00% exit
  Length  40:  90.00% exit
  Length  60:  95.50% exit
  Length 100:  96.00% exit
```

While the Caesar cipher requires a very short text length (~30 characters) to reach a 100% success rate, the Affine algorithm requires at least 40 to 60 characters to stabilize. This discrepancy is due to the difference in key space size. Since Affine evaluates 312 combinations compared to Caesar's 26, there is a much higher probability that, in short texts, an incorrect key will produce a random statistical coincidence (a false positive with a low Chi-squared value). A longer text is essential for true language frequencies to override these mathematical anomalies.
## 5. C3 Table and what governs the result
```
--- Key length (m): 3 ---
  Length  60:  82.00% exit
  Length 120: 100.00% exit
  Length 200: 100.00% exit
  Length 300: 100.00% exit

--- Key length (m): 5 ---
  Length  60:  27.00% exit
  Length 120:  75.00% exit
  Length 200:  99.00% exit
  Length 300: 100.00% exit

--- Key length (m): 7 ---
  Length  60:   0.00% exit
  Length 120:  38.00% exit
  Length 200:  89.00% exit
  Length 300: 100.00% exit
```

What truly governs whether the attack works is not the total length of the ciphertext, but rather the individual length of the subtexts or cosets ($L/m$). A Vigenère ciphertext is essentially $m$ interleaved Caesar ciphers. By increasing the key length $m$, the total text is split into a larger number of columns, leaving fewer characters per subtext and effectively "starving" the statistics. For example, a 120-character text divided by a key of 3 ($m=3$) leaves 40 letters per subtext (enough for Caesar to hit 100%), but divided by a key of 7 ($m=7$) leaves only ~17 characters per subtext, causing the Chi-squared test to fail drastically. Therefore, a longer key makes Vigenère stronger because it demands a proportionally longer intercepted text to maintain statistical vulnerability.

## 6. C4 Findings

The automated suggested mapping produced by rank alignment gets only 2 letters completely right: the encrypted T mapping to E (both rank 1), and the encrypted Q mapping to T (both rank 2). At least 19 suggestions out of the 22 distinct letters are completely wrong.

The single most useful line in the whole report for a human solver is the repeated trigram section: QAT: 3 times at positions [0, 44, 73]. In the English language, a trigram repeating this frequently in such a short text (110 characters) almost invariably corresponds to the word "THE". This single line provides a perfect foothold, instantly revealing three of the most common letters in the language and allowing the rest of the words to be deduced via context.

## 7. Vulnerability vs AES-128
The key space size is an upper bound for security, not a guarantee. Although $26!$ is a massive number (larger than an 88-bit key), a monoalphabetic cipher is trivial to break because it leaks the underlying structure of the original language. Since each letter is consistently substituted by the exact same character, the language's original frequency distributions, double letters, and trigram patterns are transferred intact to the ciphertext. Rank alignment alone does not solve the cipher because short texts never perfectly mimic the exact percentage distribution of a full language; natural variance causes mid-frequency letters to swap positions abruptly. Just as artificially aligning spaces (e.g., grouping by five) fails to solve a cipher because it merely hides word lengths to mislead the analyst, forcing a rigid 1-to-1 mathematical rank pairing corrupts the analysis. What actually solves the cipher is the combined statistical analysis of frequencies and structural patterns (like trigrams and double letters). Modern ciphers like AES-128 completely destroy this initial statistical structure, rendering frequency analysis useless.

## 8. Limitations
All implementations, cryptographic algorithms, and statistical breakers passed the automated test suite successfully, including edge cases. Proactive mathematical defenses, such as validateA using the Extended Euclidean Algorithm (egcd) to block non-coprime multipliers in real-time, work as intended. Text normalization properly sanitizes all inputs. There are no known limitations or hidden failures.
