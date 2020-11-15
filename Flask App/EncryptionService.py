from os import urandom
from Crypto.Cipher import AES
from SessionDao import SessionDao
import math
import base64

class EncryptionService:

    def __init__(self):
        pass

    def encrypt(self, data):
        key = urandom(16)
        iv = urandom(16)
        encrypt_key = AES.new(key, AES.MODE_CBC, iv)
        data_length = len(data)
        next_multiple_of_16 = 16 * math.ceil(data_length/16)
        padded_data = data.rjust(next_multiple_of_16)
        encrypted_data = encrypt_key.encrypt(padded_data.encode('utf-8'))
        print(f"Encrypted Data : {str(encrypted_data)}")
        encrypted_data = base64.b64encode(encrypted_data)
        print(f"B64 Encrypted Data : {str(encrypted_data)}")
        return [key, iv, encrypted_data]

    def decrypt(self, data, key, iv):
        b64_decoded = base64.b64decode(data)
        decrypt_key = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = decrypt_key.decrypt(b64_decoded)
        print(f"Decrypted Data : {str(decrypted_data)[2:len(str(decrypted_data)) - 1].strip()}")
        return str(decrypted_data)[2:len(str(decrypted_data)) - 1].strip()