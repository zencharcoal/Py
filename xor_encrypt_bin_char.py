# Modified Python script to encrypt a binary payload and output it as a binary char array

import argparse

def xor_encrypt_decrypt(payload, key):
    encrypted_payload = bytearray(payload)
    key_length = len(key)
    for i in range(len(encrypted_payload)):
        encrypted_payload[i] ^= key[i % key_length]
    return encrypted_payload

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="XOR Encryption Script")
    parser.add_argument("-i", "--input_file", required=True, help="Input binary file to encrypt")
    parser.add_argument("-o", "--output_file", required=True, help="Output binary char array file")
    parser.add_argument("-k", "--encryption_key", required=True, help="Encryption key as ASCII string")
    parser.add_argument("-ko", "--key_output_file", required=True, help="Output binary key file")

    args = parser.parse_args()

    # Read the input binary file
    try:
        with open(args.input_file, "rb") as f:
            payload = bytearray(f.read())
    except FileNotFoundError:
        print("Input file not found.")
        return

    # Read the encryption key
    encryption_key = args.encryption_key.encode('utf-8')

    # Encrypt the payload
    encrypted_payload = xor_encrypt_decrypt(payload, encryption_key)

    # Write the encrypted payload as a binary char array
    with open(args.output_file, "wb") as f:
        for byte in encrypted_payload:
            f.write(b'\\x{:02X}'.format(byte))

    # Write the encryption key as a binary key file
    with open(args.key_output_file, "wb") as f:
        f.write(encryption_key)

if __name__ == "__main__":
    main()

