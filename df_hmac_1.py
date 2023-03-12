from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hmac
import cryptography

masterKey = b'master key'

#HMAC Autentication
h = hmac.HMAC(masterKey, hashes.SHA256())

# Generate some parameters. These can be reused.
parameters = dh.generate_parameters(generator=2, key_size=2048)

# Generate a private key for use in the exchange y la comparto por mqtt con el HMAC
server_private_key = parameters.generate_private_key()
#HMAC the public key
h.update(server_private_key.public_key())
signature = h.finalize()

#Leo de mqtt la public key y la firma
peer_public_key = None
peer_signature = None
h = hmac.HMAC(masterKey, hashes.SHA256())
h.update(peer_public_key)
try:
    h.verify(peer_signature)
except cryptography.exceptions.InvalidSignature:
    print("Failed signature")

shared_key = server_private_key.exchange(peer_public_key)

# Perform key derivation.
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(shared_key)

print(derived_key)