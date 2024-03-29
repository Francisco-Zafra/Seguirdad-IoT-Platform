import json
import paho.mqtt.client as mqtt
import time
import paho.mqtt.client as mqtt
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hmac
import cryptography
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_parameters
from aesgcm import AEAD, AE

MasterKey = b'master key'
data = None
isData = False
keys = {}
client = None

def deviceOnBoarding(data):
    masterKey = MasterKey
    if data["mode"] == 1:
        masterKey = bytes(str(password), encoding="utf8")

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
    print(data)
    dic = {}
    dic['device_name'] = data['name']
    dic['topic'] = data['topic']
    dic['mode'] = data['mode']
    dic['data'] = []
    if (data['mode'] == 1):
        input_topics.append(dic)
    elif (data['mode'] == 3):
        sensor_topics.append(dic)
    
    print("Subscribe to:" + str(data['topic']))

    #Publish response
    info = client.publish("/IoT_Patform_2156/sub", payload=json.dumps(msg), qos = 0, retain = False)
    print("Mensaje enviado ", info.is_published())

    #Create cypher key
    global key
    peer_key = load_pem_public_key(bytes.fromhex(data['public_key']))

    shared_key = server_private_key.exchange(peer_key)
    keys[data["name"]] = HKDF(
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
    print("Mensaje: ", str(msg.topic))
    data = json.loads(msg.payload)
    if msg.topic != "/IoT_Patform_2156/sub" or data['name'] == "IoT_Platform":
        data = None
        d = json.loads(msg.payload)
        if d["name"] != "IoT_Platform":
            print(msg.topic+" "+str(msg.payload))
            iv = bytes.fromhex(d["iv"])
            tag = bytes.fromhex(d["tag"])
            encrypted_data = bytes.fromhex(d["cypher_text"])
            timestamp = bytes.fromhex(d["associated_timestamp"])
            cypher_mode = d["cypher_mode"]
            if cypher_mode == 1:
                decrypted_data = AE().decrypt(keys[d['name']], iv, encrypted_data, tag)
            elif cypher_mode == 2: 
                decrypted_data = AEAD().decrypt(keys[d['name']], timestamp, iv, encrypted_data, tag)

            print("Dato desencriptado: ", decrypted_data)

            if (d['mode'] == 1):
                device_dict = next((item for item in input_topics if item.get('device_name') == d['name']), None)
                new_msg = {'timestamp': timestamp.decode(), "value": decrypted_data.decode()}
                device_dict['data'].append(new_msg)
            elif (d['mode'] == 3):
                device_dict = next((item for item in sensor_topics if item.get('device_name') == d['name']), None)
                new_value = {'timestamp': timestamp.decode(), "value": decrypted_data.decode()}
                device_dict['data'].append(new_value)
    else:
        print(msg.topic)
        
def platform(cl, st, it, pwd):
    global client, sensor_topics, input_topics, password
    sensor_topics = st
    input_topics = it
    password = pwd
    

    client = cl
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("broker.hivemq.com", 1883, 60)
    client.subscribe("/IoT_Patform_2156/sub", qos=0)

    client.loop_start()

    while 1:
        if data != None:
            deviceOnBoarding(data)
        time.sleep(.1)
