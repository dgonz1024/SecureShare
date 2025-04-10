from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import base64

def generate_key():
    return get_random_bytes(16)  # AES-128

def encrypt_file(file_path, key):
    cipher = AES.new(key, AES.MODE_EAX)
    with open(file_path, 'rb') as file:
        plaintext = file.read()
    print(f"Plaintext length: {len(plaintext)}")  # Debugging
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    nonce = cipher.nonce

    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as file:
        file.write(nonce + tag + ciphertext)
    
    print(f"Nonce: {nonce}")  # Debugging
    print(f"Tag: {tag}")  # Debugging
    print(f"Ciphertext length: {len(ciphertext)}")  # Debugging

    return encrypted_file_path

def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, 'rb') as file:
        nonce = file.read(16)
        tag = file.read(16)
        ciphertext = file.read()

    print(f"Nonce: {nonce}")  # Debugging
    print(f"Tag: {tag}")  # Debugging
    print(f"Ciphertext length: {len(ciphertext)}")  # Debugging

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError as e:
        print(f"Decryption failed: {e}")  # Debugging
        raise

    # Generate a unique decrypted file path
    decrypted_file_path = encrypted_file_path.replace('.enc', '.dec')
    with open(decrypted_file_path, 'wb') as file:
        file.write(plaintext)
    
    return decrypted_file_path

def encode_key(key):
    return base64.urlsafe_b64encode(key).decode('utf-8')

def decode_key(encoded_key):
    return base64.urlsafe_b64decode(encoded_key)