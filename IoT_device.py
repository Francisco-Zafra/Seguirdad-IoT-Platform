import threading
import time
import datetime 
import random
import sys
import paho.mqtt.client as mqtt
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hmac
import cryptography
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, ParameterFormat
from cryptography.hazmat.primitives.serialization import load_pem_public_key

readyToSend = False
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from aesgcm import AEAD, AE

class IoTDevice:
    def __init__(self, mode, cypher_mode = None, sensor = None, timer_msg = None, name=None, topic=None):
        self.mode = mode
        self.cypher_mode = cypher_mode
        self.sensor = sensor
        self.timer_msg = timer_msg
        self.onBoarding_topic = "/IoT_Patform_2156/sub"
        self.client = mqtt.Client()
        self.client.connect("broker.hivemq.com", 1883, 60)
        self.masterKey = b'master key'
        self.authenticated = False
        self.name = name
        self.topic = topic
        self.key = None
        self.peer_key = None

    def print_information(self):
        print(self.cypher_mode, self.sensor, self.timer_msg, self.name, self.topic)

    def input_d(self):
        while(True):
            msg = {}
            msg_plaintext = input("Digite la información a enviar: ")
            timestamp= datetime.datetime.timestamp(datetime.datetime.now())
            timestamp = datetime.datetime.fromtimestamp(timestamp)
            timestamp = timestamp.strftime("%d-%m-%Y %H:%M:%S")
            associated_data = bytes(timestamp, encoding="utf8")
            if self.cypher_mode == 1:
                iv, encrypted_data, tag = AE().encrypt(self.key, bytes(msg_plaintext, encoding='utf8'))
            elif self.cypher_mode == 2: 
                iv, encrypted_data, tag = AEAD().encrypt(self.key, bytes(msg_plaintext, encoding='utf8'), associated_data)
            msg['cypher_text'] = encrypted_data.hex()
            msg['associated_timestamp'] = associated_data.hex()
            msg['iv'] = iv.hex()
            msg['tag'] = tag.hex()
            msg['cypher_mode'] = self.cypher_mode
            msg['name'] =  self.name
            msg['mode'] = self.mode
            msg_json = json.dumps(msg)
            self.client.publish(self.topic, payload=msg_json, qos=0, retain=False)

    def output_d(self):
        self.client.on_message = self.on_message
        while(True):
            print("Esperando mesanje del servidor: ")


    def gen_d(self):
        while(True):
            msg = {}
            plaintext = str(random.randint(1, 100))
            print("Lenyendo dato: ", plaintext)
            timestamp= datetime.datetime.timestamp(datetime.datetime.now())
            timestamp = datetime.datetime.fromtimestamp(timestamp)
            timestamp = timestamp.strftime("%d-%m-%Y %H:%M:%S")
            associated_data = bytes(timestamp, encoding="utf8")
            if self.cypher_mode == 1:
                print("AE")
                iv, encrypted_data, tag = AE().encrypt(self.key, bytes(plaintext,encoding="utf8"))
            elif self.cypher_mode == 2:
                print("AEAD")
                iv, encrypted_data, tag = AEAD().encrypt(self.key, bytes(plaintext,encoding="utf8"), associated_data)
            msg['cypher_text'] = encrypted_data.hex()
            msg['associated_timestamp'] = associated_data.hex()
            msg['iv'] = iv.hex()
            msg['tag'] = tag.hex()
            msg['cypher_mode'] = self.cypher_mode
            msg['name'] =  self.name
            msg['mode'] = self.mode
            print("Enviando datos al servidor.....")
            info=self.client.publish(self.topic, payload=json.dumps(msg), qos=0, retain=False)
            print("Mensaje enviado", info.is_published())
            time.sleep(self.timer_msg)

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    #Callback for onboarding messages
    def onBoardingMessage(self, client, userdata, msg):
        print("Mensaje recibido:")
        print(msg.topic)
        #Get data
        data = json.loads(msg.payload)
        #Si el mensaje es para mi
        if data['name'] == "IoT_Platform" and data['deviceName'] == self.name:
            h2 = hmac.HMAC(self.masterKey, hashes.SHA256())
            h2.update(bytes.fromhex(data['public_key']))
            try:
                h2.verify(bytes.fromhex(data['signature']))
                print("Verified")
                self.authenticated = True
                self.client.loop_stop()
                self.peer_key = bytes.fromhex(data['public_key'])
                print("Mensaje procesado")
            except cryptography.exceptions.InvalidSignature:
                print("Failed signature")
        


    def onBoarding(self):
        if self.mode == 1:
            self.masterKey = bytes(input("Inbtroduce la clave"),encoding="utf8")
            
        print("Comenzando On Boarding")
        print("Generando claves...")
        # Generar frima HMAC
        h = hmac.HMAC(self.masterKey, hashes.SHA256())
        parameters = dh.generate_parameters(generator=2, key_size=512)
        server_private_key = parameters.generate_private_key()
        print("Claves generadas...")
        print("Generando firma...")
        h.update(server_private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo))
        signature = h.finalize()
        print("Firma generada...")

        # Construir mensaje
        msg = {}
        msg['public_key'] = server_private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo).hex()
        msg['signature'] = signature.hex()
        msg['name'] =  self.name
        msg['topic'] = self.topic
        msg['mode'] = self.mode
        msg['cypher_mode'] = self.cypher_mode
        msg['parameters'] = parameters.parameter_bytes(encoding=Encoding.PEM, format=ParameterFormat.PKCS3).hex()

        #Set callback for onboarding topic
        self.client.message_callback_add(self.onBoarding_topic, self.onBoardingMessage)
        #Subscribe to onboarding topic
        self.client.subscribe(self.onBoarding_topic, qos= 0)
        print(self.onBoarding_topic)
        # Publish message
        info = self.client.publish(self.onBoarding_topic, payload=json.dumps(msg), qos = 0, retain = False)
        print("Mensaje enviado", info.is_published())
        self.client.loop_start()
        #Wait for message
        while not self.authenticated:
            time.sleep(1)
            print(".", end="", flush=True)
        self.client.loop_stop()

        #Create cypher key
        peer_key = load_pem_public_key(self.peer_key)
        shared_key = server_private_key.exchange(peer_key)

        self.key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)

        #Start working
        
        if (self.mode == 1):
            self.input_d()
        elif (self.mode == 2):
            self.output_d()
        elif (self.mode == 3):
            self.gen_d()



def create_new_decive(mode, cypher_mode, sensor, timer_msg, name, topic):
    iot = IoTDevice(mode, cypher_mode, sensor, timer_msg, name, topic)
    iot.print_information()
    th = threading.Thread(target=iot.onBoarding)
    th.start()



def main():
    if len(sys.argv) > 1:
        nombre_funcion = sys.argv[1]
        if nombre_funcion == 'create_new_decive':
            create_new_decive(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), str(sys.argv[6]), str(sys.argv[7]))
        else:
            print("Función no encontrada")
    else:
        print("Debe proporcionar el nombre de una función como argumento")

if __name__ == "__main__":
    main()


