import os

key_length = 256  # for example, you could adjust this to your needs
xor_key = os.urandom(key_length)
print(xor_key.hex())
