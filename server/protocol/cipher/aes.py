__author__ = 'Itamar'
import base64
from Crypto.Cipher import AES
from Crypto import Random
# Note: Install PyCrypto ('pip install crypto')
# Also might want to save iv.

BS = 16
def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
def unpad(s): return s[:-ord(s[len(s)-1:])]


class AESCipher:
    def __init__(self, key):
        """
        Initialize the AESCipher class with the given key.
        """
        self.key = key

    def encrypt(self, raw):
        """
        Encrypt the given plaintext string using AES in CBC mode with the given key.

        Args:
            raw (bytes): The plaintext message to encrypt.

        Returns:
            bytes: The encrypted message, represented as a base64-encoded string.
        """
        raw = pad(raw)
        raw = raw.encode()
        iv = Random.new().read(AES.block_size) # Generate a random IV (initialization vector) to use in CBC mode.
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        """
        Decrypt the given ciphertext string using AES in CBC mode with the given key.

        Args:
            enc (bytes): The ciphertext message to decrypt, represented as a base64-encoded string.

        Returns:
            str: The decrypted plaintext message.
        """
        enc = base64.b64decode(enc)
        iv = enc[:16] # The IV is stored in the first 16 bytes of the encrypted message.
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode()