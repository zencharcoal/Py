import argparse

def xor_encrypt(payload, key):
    encrypted_payload = bytearray(payload)
    key_length = len(key)
    for i in range(len(encrypted_payload)):
        encrypted_payload[i] ^= key[i % key_length]
    return encrypted_payload

def xor_decrypt(encrypted_payload, key):
    return xor_encrypt(encrypted_payload, key)  # XOR encryption is symmetric

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="XOR Encryption/Decryption Script")
    parser.add_argument("-i", "--input_file", required=True, help="Input binary file to encrypt/decrypt")
    parser.add_argument("-o", "--output_file", required=True, help="Output binary data file")
    parser.add_argument("-k", "--encryption_key", required=True, help="Encryption key as ASCII string")
    parser.add_argument("-ko", "--key_output_file", required=True, help="Output binary char array key file")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the input file")

    args = parser.parse_args()

    try:
        # Read the input binary file
        with open(args.input_file, "rb") as f:
            input_data = bytearray(f.read())
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        return

    # Read the encryption key
    encryption_key = args.encryption_key.encode('utf-8')

    if args.decrypt:
        # Decrypt the input data
        output_data = xor_decrypt(input_data, encryption_key)
    else:
        # Encrypt the input data
        output_data = xor_encrypt(input_data, encryption_key)

    # Write the output data to the output file
    with open(args.output_file, "wb") as f:
        f.write(output_data)

    if not args.decrypt:
        # Write the encryption key as a binary char array to the key output file
        with open(args.key_output_file, "w") as f:
            f.write("const char encryption_key[] = {")
            for i, byte in enumerate(encryption_key):
                f.write(f"0x{byte:02X}")
                if i != len(encryption_key) - 1:
                    f.write(", ")
            f.write(", 0x00};")  # Ensure null-termination

if __name__ == "__main__":
    main()

