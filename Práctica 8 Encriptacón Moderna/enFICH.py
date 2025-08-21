import json
import sys
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

if len(sys.argv) != 2:
    print("Usage: python encFICH.py cipher.txt")
    sys.exit(1)

input_filename = sys.argv[1]
try:
    with open(input_filename, 'rb') as file:
        data = file.read()
except FileNotFoundError:
    print(f"Error: File '{input_filename}' not found.")
    sys.exit(1)

key = get_random_bytes(16)  
cipher = AES.new(key, AES.MODE_CBC)

ct_bytes = cipher.encrypt(pad(data, AES.block_size))

iv = b64encode(cipher.iv).decode('utf-8')
ct = b64encode(ct_bytes).decode('utf-8')

result = {
    "iv": iv,
    "ciphertext": ct
}

output_filename = f"{input_filename}.enc.json"
with open(output_filename, 'w') as outfile:
    json.dump(result, outfile)

print(f"Encryption complete. Encrypted file saved as '{output_filename}'.")
print(f"Key (hex): {key.hex()}")
