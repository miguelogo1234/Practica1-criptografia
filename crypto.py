import argparse
import sys

# Importamos todas las funciones de los archivos que ya has creado
from caesar import encrypt as caesar_encrypt, decrypt as caesar_decrypt
from affine import encrypt as affine_encrypt, decrypt as affine_decrypt
from monoalpha import encrypt as mono_encrypt, decrypt as mono_decrypt, key_from_keyword
from vigenere import encrypt as vigenere_encrypt, decrypt as vigenere_decrypt
from break_caesar import break_caesar
from break_affine import break_affine
from break_vigenere import break_vigenere
from assist import report as assist_report

def get_input_text(args) -> str:
    """Reads input text from a file or stdin if --in is absent."""
    if args.in_file:
        try:
            with open(args.in_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            sys.stderr.write(f"Error: Input file '{args.in_file}' not found.\n")
            sys.exit(1)
    else:
        # Read from standard input
        return sys.stdin.read()

def output_text(text: str, args):
    """Writes output text to a file or stdout if --out is absent."""
    if args.out_file:
        try:
            with open(args.out_file, 'w', encoding='utf-8') as f:
                f.write(text)
        except IOError:
            sys.stderr.write(f"Error: Could not write to output file '{args.out_file}'.\n")
            sys.exit(1)
    else:
        # Write to standard output
        sys.stdout.write(text + '\n')

def main():
    parser = argparse.ArgumentParser(description="Unified Cryptography CLI Tool (Substitution and Cryptanalysis)")
    
    # Subparsers for main commands: cipher, break, assist
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- 1. ENCRYPT/DECRYPT COMMANDS (caesar, affine, mono, vigenere) ---
    for cipher in ['caesar', 'affine', 'mono', 'vigenere']:
        cipher_parser = subparsers.add_parser(cipher, help=f"{cipher.capitalize()} cipher operations")
        cipher_subparsers = cipher_parser.add_subparsers(dest="mode", required=True)
        
        for mode in ['encrypt', 'decrypt']:
            mode_parser = cipher_subparsers.add_parser(mode, help=f"{mode.capitalize()} using {cipher.capitalize()}")
            mode_parser.add_argument("--in", dest="in_file", help="Input file")
            mode_parser.add_argument("--out", dest="out_file", help="Output file")
            
            # Key arguments specific to each cipher
            if cipher == 'caesar':
                mode_parser.add_argument("--key", type=int, required=True, help="Numeric key for Caesar")
            elif cipher == 'affine':
                mode_parser.add_argument("-a", type=int, required=True, help="Multiplier 'a' for Affine")
                mode_parser.add_argument("-b", type=int, required=True, help="Shift 'b' for Affine")
            elif cipher == 'mono':
                mode_parser.add_argument("--keyword", required=True, help="Keyword for Monoalphabetic")
            elif cipher == 'vigenere':
                mode_parser.add_argument("--key", required=True, help="Keyword for Vigenere")

    # --- 2. BREAK COMMAND ---
    break_parser = subparsers.add_parser('break', help="Break a cipher")
    break_subparsers = break_parser.add_subparsers(dest="target", required=True)
    
    # break caesar / affine
    for target in ['caesar', 'affine']:
        target_parser = break_subparsers.add_parser(target, help=f"Break {target.capitalize()} cipher")
        target_parser.add_argument("--in", dest="in_file", help="Input ciphertext file")
        target_parser.add_argument("--out", dest="out_file", help="Output plaintext file")
        target_parser.add_argument("--lang", choices=['en', 'es'], default='en', help="Target language (en/es)")
        
    # break vigenere (requires --m)
    vig_break_parser = break_subparsers.add_parser('vigenere', help="Break Vigenere cipher")
    vig_break_parser.add_argument("--m", type=int, required=True, help="Key length")
    vig_break_parser.add_argument("--in", dest="in_file", help="Input ciphertext file")
    vig_break_parser.add_argument("--out", dest="out_file", help="Output plaintext file")
    vig_break_parser.add_argument("--lang", choices=['en', 'es'], default='en', help="Target language (en/es)")

    # --- 3. ASSIST COMMAND ---
    assist_parser = subparsers.add_parser('assist', help="Frequency assistant for monoalphabetic substitution")
    assist_parser.add_argument("--in", dest="in_file", help="Input ciphertext file")
    assist_parser.add_argument("--out", dest="out_file", help="Output report file")
    assist_parser.add_argument("--lang", choices=['en', 'es'], default='en', help="Target language (en/es)")

    try:
        args = parser.parse_args()
        input_text = get_input_text(args)
        
        if args.command in ['caesar', 'affine', 'mono', 'vigenere']:
            if args.command == 'caesar':
                if args.mode == 'encrypt':
                    result = caesar_encrypt(input_text, args.key)
                else:
                    result = caesar_decrypt(input_text, args.key)
                    
            elif args.command == 'affine':
                if args.mode == 'encrypt':
                    result = affine_encrypt(input_text, args.a, args.b)
                else:
                    result = affine_decrypt(input_text, args.a, args.b)

            elif args.command == 'mono':
                full_key = key_from_keyword(args.keyword)
                if args.mode == "encrypt":
                    result = mono_encrypt(input_text, full_key)
                else:
                    result = mono_decrypt(input_text, full_key)
                
            elif args.command == 'vigenere':
                if args.mode == "encrypt":
                    result = vigenere_encrypt(input_text, args.key)
                else:
                    result = vigenere_decrypt(input_text, args.key)
                
            output_text(result, args)

        elif args.command == 'break':
            if args.target == 'caesar':
                best_k, plaintext = break_caesar(input_text, args.lang)
                sys.stdout.write(f"Key found: {best_k}\n")
                output_text(plaintext, args)
                
            elif args.target == 'affine':
                best_key, plaintext = break_affine(input_text, args.lang)
                sys.stdout.write(f"Key found: a={best_key[0]}, b={best_key[1]}\n")
                output_text(plaintext, args)
                
            elif args.target == 'vigenere':
                best_key, plaintext = break_vigenere(input_text, args.m, args.lang)
                sys.stdout.write(f"Key found: {best_key}\n")
                output_text(plaintext, args)

        elif args.command == 'assist':
            report_text = assist_report(input_text, args.lang)
            output_text(report_text, args)

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()