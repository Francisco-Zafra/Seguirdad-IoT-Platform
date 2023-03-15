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
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_parameters

masterKey = b'master key'
data = None
isData = False
key = None

def deviceOnBoarding(data):

    #Check signature
    h2 = hmac.HMAC(masterKey, hashes.SHA256())
    h2.update(bytes.fromhex(data['public_key']))
    try:
        h2.verify(bytes.fromhex(data['signature']))
        print("Verified")
    except cryptography.exceptions.InvalidSignature:
        print("Failed signature")
        return
    
    #HMAC
    h = hmac.HMAC(masterKey, hashes.SHA256())
    parameters = load_pem_parameters(bytes.fromhex(data["parameters"]))
    server_private_key = parameters.generate_private_key()
    print("Claves generadas...")
    print("Generando firma...")
    h.update(server_private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo))
    signature = h.finalize()
    print("Firma generada...")


    #Create response
    msg = {}
    msg['public_key'] = server_private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo).hex()
    msg['signature'] = signature.hex()
    msg['name'] =  'IoT_Platform'
    msg['deviceName'] = data['name']

    #Subscribe to device topic
    client.subscribe(data["topic"], qos= 0)
    print("Subscribe to:" + str(data['topic']))
    #Almacenar topics aqui
    #Publish response
    info = client.publish('/fran14732832/sub', payload=json.dumps(msg), qos = 0, retain = False)
    print("Mensaje enviado ", info.is_published())

    #Create cypher key
    global key
    peer_key = load_pem_public_key(bytes.fromhex(data['public_key']))

    shared_key = server_private_key.exchange(peer_key)
    key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global data
    print("Mensaje")
    data = json.loads(msg.payload)
    if msg.topic != "/fran14732832/sub" or data['name'] == "IoT_Platform":
        data = None
        print(msg.topic+" "+str(msg.payload))
    else:
        print(msg.topic)

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
