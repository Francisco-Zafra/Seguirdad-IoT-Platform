import os
import _ctypes
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class AEAD:
    def encrypt(self, key, plaintext, associated_data):
        # Generate a random 96-bit IV.
        iv = os.urandom(12)

        # Construct an AES-GCM Cipher object with the given key and a
        # randomly generated IV.
        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
        ).encryptor()

        # associated_data will be authenticated but not encrypted,
        # it must also be passed in on decryption.
        encryptor.authenticate_additional_data(associated_data)

        # Encrypt the plaintext and get the associated ciphertext.
        # GCM does not require padding.
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        return (iv, ciphertext, encryptor.tag)

    def decrypt(self, key, associated_data, iv, ciphertext, tag):
        # Construct a Cipher object, with the key, iv, and additionally the
        # GCM tag used for authenticating the message.
        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
        ).decryptor()

        # We put associated_data back in or the tag will fail to verify
        # when we finalize the decryptor.
        decryptor.authenticate_additional_data(associated_data)

        # Decryption gets us the authenticated plaintext.
        # If the tag does not match an InvalidTag exception will be raised.
        try:
            plain = decryptor.update(ciphertext) + decryptor.finalize()
        except:
            plain = b"Error!"
        return plain

class AE:
    def encrypt(self, key, plaintext):
        # Generate a random 96-bit IV.
        iv = os.urandom(12)

        # Construct an AES-GCM Cipher object with the given key and a
        # randomly generated IV.
        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
        ).encryptor()

        # Encrypt the plaintext and associated data.
        # GCM does not require padding.
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        return (iv, ciphertext, encryptor.tag)

    def decrypt(self, key, iv, ciphertext, tag):
        # Construct a Cipher object, with the key, iv, and additionally the
        # GCM tag used for authenticating the message.
        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
        ).decryptor()

        # Decryption gets us the plaintext.
        # If the tag does not match an InvalidTag exception will be raised.
        try:
            plain = decryptor.update(ciphertext) + decryptor.finalize()
        except:
            plain = b"Error!"
        return plain


