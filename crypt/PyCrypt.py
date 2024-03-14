from getpass import getpass
import math
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os


def dec(private_key_file, encrypted_file, passphrase):
	with open(private_key_file, "rb") as file:
	    private_key = RSA.import_key(file.read(), passphrase=passphrase)

	cipher_rsa = PKCS1_OAEP.new(private_key)

	# Open encrypted file and read its contents
	with open(encrypted_file, "rb") as file:
	    ciphertext = file.read()

	size = 256 * 2
	blocks = math.ceil(len(ciphertext)/size)
	print(math.ceil(len(ciphertext)/size))

	plaintext = b""
	for i in range(blocks):
	    start = i * size
	    end = start + size
	    block = ciphertext[start:end]
	    plaintext += cipher_rsa.decrypt(block)

	return plaintext

def dec_from_varrable(private_key_file, encrypted_data, passphrase):
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    import math

    private_key = RSA.import_key(open(private_key_file).read(), passphrase=passphrase)
    cipher_rsa = PKCS1_OAEP.new(private_key)

    size = 256 * 2
    blocks = math.ceil(len(encrypted_data) / size)

    plaintext = b""
    for i in range(blocks):
        start = i * size
        end = start + size
        block = encrypted_data[start:end]
        plaintext += cipher_rsa.decrypt(block)

    return plaintext

def enc(public_key_file, plaintext, input_file):
	# Load public key from file
	with open(public_key_file, "rb") as file:
	    public_key = RSA.import_key(file.read())

	# Generate a cipher object using the public key
	cipher_rsa = PKCS1_OAEP.new(public_key)

	blocks = math.ceil(len(plaintext)/256)
	print(math.ceil(len(plaintext)/256))

	encrypted_file = input_file
	with open(encrypted_file, "wb") as file:
	    for i in range(blocks):
	        start = i * 256
	        end = start + 256
	        block = plaintext[start:end]
	        encrypted_block = cipher_rsa.encrypt(block)
	        file.write(encrypted_block)

def enc_to_varriable(public_key_file, plaintext):
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    import math

    # Load public key from file
    with open(public_key_file, "rb") as file:
        public_key = RSA.import_key(file.read())

    # Generate a cipher object using the public key
    cipher_rsa = PKCS1_OAEP.new(public_key)

    blocks = math.ceil(len(plaintext) / 256)

    encrypted_data = b""
    for i in range(blocks):
        start = i * 256
        end = start + 256
        block = plaintext[start:end]
        encrypted_block = cipher_rsa.encrypt(block)
        encrypted_data += encrypted_block

    return encrypted_data

def aes_enc(data, key):
    iv = get_random_bytes(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    
    # Padding the data to make its length a multiple of 16
    padded_data = pad(data.encode(), AES.block_size)
    
    encrypted_data = encryptor.encrypt(padded_data)
    
    # Return the IV and encrypted data
    return iv + encrypted_data

def aes_dec(data, key):
    iv = data[:16]  # Get the initialization vector from the data
    
    decryptor = AES.new(key, AES.MODE_CBC, iv)

    decrypted_data = decryptor.decrypt(data[16:])
    decrypted_data = unpad(decrypted_data, AES.block_size)

    return decrypted_data.decode('utf-8')