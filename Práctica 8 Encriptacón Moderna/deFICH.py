import json
import sys
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

if len(sys.argv) != 2:
    print("Usage: python decFICH.py <encrypted_file>")
    sys.exit(1)

input_filename = sys.argv[1]
try:
    with open(input_filename, 'r') as file:
        encrypted_data = json.load(file)
except FileNotFoundError:
    print(f"Error: File '{input_filename}' not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: File '{input_filename}' is not a valid JSON file.")
    sys.exit(1)

key_input = input("Enter the key (hex): ")
try:
    key = bytes.fromhex(key_input)
except ValueError:
    print("Invalid key. Please enter a valid hexadecimal key.")
    sys.exit(1)

try:
    iv = b64decode(encrypted_data['iv'])
    ct = b64decode(encrypted_data['ciphertext'])
except KeyError:
    print("Error: JSON file missing required fields ('iv' or 'ciphertext').")
    sys.exit(1)


try:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ct), AES.block_size)
    print("Decryption successful. Decrypted content:")
    print(plaintext.decode('utf-8'))
except (ValueError, KeyError):
    print("Error: Decryption failed. Check the key and input file.")
