import json
import paho.mqtt.client as mqtt
import codecs
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

masterKey = b'master key'
data = None
isData = False

def deviceOnBoarding(data):
    #HMAC
    h = hmac.HMAC(masterKey, hashes.SHA256())
    parameters = dh.generate_parameters(generator=2, key_size=512)
    server_private_key = parameters.generate_private_key()
    print("Claves generadas...")
    print("Generando firma...")
    h.update(server_private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo))
    signature = h.finalize()
    print("Firma generada...")

    h2 = hmac.HMAC(masterKey, hashes.SHA256())
    h2.update(bytes(bytes.fromhex(data['public_key'])))
    try:
        h2.verify(bytes.fromhex(data['signature']))
        print("Verified")
    except cryptography.exceptions.InvalidSignature:
        print("Failed signature")

    #Create response
    msg = {}
    msg['public_key'] = server_private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo).hex()
    msg['signature'] = signature.hex()
    msg['name'] =  'IoT_Platform'

    x = client.subscribe("/fran14732832/temp", qos= 0)
    print("Subscribe to:" + str(data['topic']) + " State: " + str(x))
    info = client.publish('/fran14732832/sub', payload=json.dumps(msg), qos = 0, retain = False)
    print(str(info))
    #info.wait_for_publish()
    print("Mensaje enviado")
    print(info.is_published())
    print(msg)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global data
    print("Mensaje:")
    print(msg.topic+" "+str(msg.payload))
    data = json.loads(msg.payload)
    if msg.topic != "/fran14732832/sub" or data['name'] == "IoT_Platform":
        data = None


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message



a = client.connect("broker.hivemq.com", 1883, 60)
client.subscribe("/fran14732832/sub", qos=0)

client.loop_start()

while 1:
    if data != None:
        deviceOnBoarding(data)
    time.sleep(.1)
