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

readyToSend = False

class IoTDevice:
    def __init__(self, cypher_mode = None, sensor = None, timer_msg = None):
        self.cypher_mode = cypher_mode
        self.sensor = sensor
        self.timer_msg = timer_msg
        self.onBoarding_topic = '/fran14732832/sub'
        self.client = mqtt.Client()
        self.client.connect("broker.hivemq.com", 1883, 60)
        self.masterKey = b'master key'
        self.authenticated = False

    def input_d(self):
        while(True):
            msg = input("Digite la información a enviar: ")
            print(msg)
            encrypted_data = '' #encriptar datos
            #self.client.publish(self.topic, payload=encrypted_data, qos=0, retain=False)

    def output_d(self):
        self.client.on_message = self.on_message
        #client.subscribe("/fran192837/device", qos=0) # pasamos el topic como argumento
        while(True):
            print("Esperando mesanje del servidor: ")

    def gen_d(self):
        while(True):
            data = random.randint(1, 100)
            print("Lenyendo dato: ", data)
            print("Enviando datos al servidor.....")
            info=self.client.publish('/fran14732832/temp', payload='{"name": "hola"}', qos=0, retain=False)
            print("Mensaje enviado", info.is_published())
            time.sleep(5)

    def on_message(self, client, userdata, msg):
        f = Fernet(key)
        data = json.loads(f.decrypt(msg.payload))
        print(msg.topic+" "+str(data['data']))

    def onBoardingMessage(self, client, userdata, msg):
        print("Mensaje recibido:")
        print(msg.topic+" "+str(msg.payload))
        data = json.loads(msg.payload)
        if data['name'] == "IoT_Platform":
            h2 = hmac.HMAC(self.masterKey, hashes.SHA256())
            h2.update(bytes(bytes.fromhex(data['public_key'])))
            try:
                h2.verify(bytes.fromhex(data['signature']))
                print("Verified")
                self.authenticated = True
                self.client.loop_stop()
            except cryptography.exceptions.InvalidSignature:
                print("Failed signature")
        print("Mensaje procesado")


    def onBoarding(self, name="iot-device", topic="/fran14732832/sub", cypher_mode=1):
        print("Comenzando On Boarding")
        print("Generando claves...")
        h = hmac.HMAC(self.masterKey, hashes.SHA256())
        parameters = dh.generate_parameters(generator=2, key_size=512)
        server_private_key = parameters.generate_private_key()
        print("Claves generadas...")
        print("Generando firma...")
        h.update(server_private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo))
        signature = h.finalize()
        print("Firma generada...")

        msg = {}
        msg['public_key'] = server_private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo).hex()
        msg['signature'] = signature.hex()
        msg['name'] =  name
        msg['topic'] = '/fran14732832/temp'
        msg['cypher_mode'] = cypher_mode

        self.client.message_callback_add(self.onBoarding_topic, self.onBoardingMessage)
        self.client.subscribe(self.onBoarding_topic, qos= 0)
        print(self.onBoarding_topic)
        info = self.client.publish(self.onBoarding_topic, payload=json.dumps(msg), qos = 0, retain = False)
        print("Mensaje enviado")
        print(info.is_published())
        print(msg)
        self.client.loop_start()
        while not self.authenticated:
            time.sleep(1)
            print(".", end="", flush=True)
        self.client.loop_stop()

        self.gen_d()



def create_new_decive(mode, cypher_mode, sensor, timer_msg):
    if (mode == 1):
        iot = IoTDevice(cypher_mode)
        th = threading.Thread(target=iot.input_d)
    elif (mode == 2):
        iot = IoTDevice()
        th = threading.Thread(target=iot.output_d)
    elif (mode == 3):
        iot = IoTDevice(cypher_mode, sensor, timer_msg)
        #th = threading.Thread(target=iot.gen_d)
        th = threading.Thread(target=iot.onBoarding)

    th.start()



def main():
    if len(sys.argv) > 1:
        nombre_funcion = sys.argv[1]
        if nombre_funcion == 'create_new_decive':
            create_new_decive(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
        else:
            print("Función no encontrada")
    else:
        print("Debe proporcionar el nombre de una función como argumento")

if __name__ == "__main__":
    main()


