from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import threading
import time
import random
import sys
import paho.mqtt.client as mqtt
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hmac
import cryptography
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# Generate some parameters. These can be reused.
parameters = dh.generate_parameters(generator=2, key_size=512)

# Generate a private key for use in the exchange.
server_private_key = parameters.generate_private_key()

parameters = dh.generate_parameters(generator=2, key_size=512)

# In a real handshake the peer is a remote client. For this
# example we'll generate another local private key though. Note that in
# a DH handshake both peers must agree on a common set of parameters.
peer_private_key = parameters.generate_private_key()
peer_public_key = peer_private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo).hex()
msg = {}
msg["a"] = peer_public_key
jsonstring = json.dumps(msg)
jsona = json.loads(jsonstring)
peer_public_key2 = jsona["a"]

pper = load_pem_public_key(bytes.fromhex(peer_public_key2))

shared_key = server_private_key.exchange(pper)

# And now we can demonstrate that the handshake performed in the
# opposite direction gives the same final value
same_shared_key = peer_private_key.exchange(server_private_key.public_key())

print(shared_key.hex() == same_shared_key.hex())