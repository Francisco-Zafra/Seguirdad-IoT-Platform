import threading
import time
import random
import sys
import paho.mqtt.client as mqtt
import json

class IoTDevice:
    def __init__(self, cypher_mode = None, sensor = None, timer_msg = None):
        self.cypher_mode = cypher_mode
        self.sensor = sensor
        self.timer_msg = timer_msg
        self.topic = ''
        self.client = mqtt.Client()
        self.client.connect("broker.hivemq.com", 1883, 60)
        



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
            encrypted_data = '' #encriptar datos
            #self.client.publish(self.topic, payload=encrypted_data, qos=0, retain=False)
            time.sleep(self.timer_msg)

    def on_message(self, client, userdata, msg):
        f = Fernet(key)
        data = json.loads(f.decrypt(msg.payload))
        print(msg.topic+" "+str(data['data']))


def create_new_decive(mode, cypher_mode, sensor, timer_msg):
    if (mode == 1):
        iot = IoTDevice(cypher_mode)
        th = threading.Thread(target=iot.input_d)
    elif (mode == 2):
        iot = IoTDevice()
        th = threading.Thread(target=iot.output_d)
    elif (mode == 3):
        iot = IoTDevice(cypher_mode, sensor, timer_msg)
        th = threading.Thread(target=iot.gen_d)

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


