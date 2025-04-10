from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from encryption.aes_utils import generate_key, encrypt_file, decrypt_file
import os

class FileEncryptionTests(TestCase):
    def setUp(self):
        self.test_file_path = 'test_file.txt'
        self.test_file_content = b'This is a test file.'
        with open(self.test_file_path, 'wb') as f:
            f.write(self.test_file_content)
        self.key = generate_key()

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        if os.path.exists(self.test_file_path + '.enc'):
            os.remove(self.test_file_path + '.enc')
        if os.path.exists(self.test_file_path[:-4]):
            os.remove(self.test_file_path[:-4])

    def test_file_encryption(self):
        encrypted_file_path = encrypt_file(self.test_file_path, self.key)
        self.assertTrue(os.path.exists(encrypted_file_path))

    def test_file_decryption(self):
        encrypted_file_path = encrypt_file(self.test_file_path, self.key)
        decrypted_file_path = decrypt_file(encrypted_file_path, self.key)
        
        with open(decrypted_file_path, 'rb') as f:
            decrypted_content = f.read()
        
        self.assertEqual(decrypted_content, self.test_file_content)