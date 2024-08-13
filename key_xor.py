import os

def generate_xor_key(length=16):
    return os.urandom(length)

if __name__ == "__main__":
    key = generate_xor_key()
    print("Random XOR Key:", ' '.join(['0x{:02X}'.format(b) for b in key]))

