import threading
import time
import random

class IoTDevice:
    def __init__(self, cypher_mode = None, sensor = None, timer_msg = None):
        self.cypher_mode = cypher_mode
        self.sensor = sensor
        self.timer_msg = timer_msg


    def input_d(self):
        while(True):
            msg = input("Digite la información a enviar: ")
            print(msg)

    def output_d(self):
        while(True):
            print("Esperando mesanje del servidor: ")

    def gen_d(self):
        while(True):
            data = random.randint(1, 100)
            print("Lenyendo dato: ", data)
            print("Enviando datos al servidor.....")
            time.sleep(self.timer_msg)


def create_new_decive(mode, cypher_mode, sensor, timer_msg):
    if (mode == 1):
        iot = IoTDevice(cypher_mode)
        hilo = threading.Thread(target=iot.output_d)
    elif (mode == 2):
        iot = IoTDevice()
        hilo = threading.Thread(target=iot.input_d)
    elif (mode == 3):
        iot = IoTDevice(cypher_mode, sensor, timer_msg)
        hilo = threading.Thread(target=iot.gen_d)

    hilo.start()

#create_new_decive(3,1,1,10)

def prueba():
    print("Print del segundo script")
