from aes_utils import generate_key, encrypt_file, decrypt_file, encode_key, decode_key
import os

# Test file paths
test_file_path = 'test_file.txt'
encrypted_file_path = 'test_file.txt.enc'
decrypted_file_path = 'test_file.txt.dec'

# Step 1: Create a test file
with open(test_file_path, 'w') as file:
    file.write("This is a test file for encryption and decryption.")

# Step 2: Generate a key
key = generate_key()
print(f"Generated Key: {key}")
encoded_key = encode_key(key)
print(f"Encoded Key: {encoded_key}")

# Step 3: Encrypt the file
encrypted_path = encrypt_file(test_file_path, key)
print(f"Encrypted File Path: {encrypted_path}")

# Step 4: Decrypt the file
decoded_key = decode_key(encoded_key)
decrypted_path = decrypt_file(encrypted_path, decoded_key)
print(f"Decrypted File Path: {decrypted_path}")

# Step 5: Verify the decrypted file content
with open(decrypted_path, 'r') as file:
    content = file.read()
    print(f"Decrypted File Content: {content}")

# Cleanup (optional)
os.remove(test_file_path)
os.remove(encrypted_file_path)
os.remove(decrypted_file_path)