import threading
import time
import random
import sys

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
    print(type(mode))
    if (mode == 1):
        iot = IoTDevice(cypher_mode)
        hilo = threading.Thread(target=iot.input_d)
    elif (mode == 2):
        iot = IoTDevice()
        hilo = threading.Thread(target=iot.output_d)
    elif (mode == 3):
        iot = IoTDevice(cypher_mode, sensor, timer_msg)
        hilo = threading.Thread(target=iot.gen_d)

    hilo.start()



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


