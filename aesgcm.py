import os

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class AEAD:
    def encrypt(key, plaintext, associated_data):
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

    def decrypt(key, associated_data, iv, ciphertext, tag):
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
    def encrypt(key, plaintext):
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

    def decrypt(key, iv, ciphertext, tag):
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


if __name__ == "__main__":
    algo = "AEAD" # "AEAD" or "AE"
    key = AESGCM.generate_key(bit_length=128)
    plaintext = b'a secret message!'
    associated_data = b"authenticated but not encrypted payload" # in case of AEAD
    decrypted_text = b""
    #for AE, plain text = plain text + associated data???

    if algo == "AEAD":
        iv, ciphertext, tag = AEAD.encrypt(key, plaintext, associated_data)
        decrypted_text = AEAD.decrypt(key, associated_data, iv, ciphertext, tag)
    elif algo == "AE":
        iv, ciphertext, tag = AE.encrypt(key, plaintext)
        decrypted_text = AE.decrypt(key, iv, ciphertext, tag)
    print("iv: {}, Cipher text: {}, Tag: {}".format(iv,ciphertext,tag))
    print("Decrypted text: {}".format(decrypted_text.decode()))