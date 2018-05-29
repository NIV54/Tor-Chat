import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import os


class AESCipher(object):
    def __init__(self, key):
        """gets a key and encrypts it with sha256"""
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        """gets raw data and preforms base64 over AES encryption"""
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        """gets encrypted data of the above protocol and decrypts it"""
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


class DataLayer(object):
    def __init__(self, next_layer, next_address, content):
        """:param next_layer = tpe DataLayer
        :param next_address = tuple - ip (str), port (int)
        :param content = type string, the message to be sent"""
        self.next_layer = next_layer
        self.next_address = next_address
        self.content = content


