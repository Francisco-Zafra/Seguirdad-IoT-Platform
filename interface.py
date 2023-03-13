import os
import subprocess

cipher_mode = 0
sensor_selected = 0
timer_msg = 0
iot = 0

def sub_menu():
    while True:
        print('\n')
        print('------------------------------------------------')
        print('------------- Selección de cifrado -------------')
        print('------------------------------------------------')
        print('1. AE')
        print('2. AEAD')
        print('3. Cancelar')

        opcion_sub = input('Seleccione el tipo de cifrado a utilizar: ')

        if opcion_sub == '1':
            return 1
            
        elif opcion_sub == '2':
            return 2
        elif opcion_sub == '3':
            clear_screen()
            return 0
        else:
            print('Opción inválida')

def select_sensor():
    while True:
        print('\n')
        print('------------------------------------------------')
        print('---------------- Tipo de Sensor ----------------')
        print('------------------------------------------------')
        print('1. Temperatura')
        print('2. Humedad')
        print('3. Intensidad Luminosa')
        print('4. Cancelar')

        opcion_sub = input('Seleccione el tipo de sensor a crear: ')

        if opcion_sub == '1':
            return 1
        elif opcion_sub == '2':
            return 2
        elif opcion_sub == '3':
            return 3
        elif opcion_sub == '4':
            clear_screen()
            return 0
        else:
            print('Opción inválida')

def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('nt', 'dos', 'ce'):
        os.system('cls')
        
def create_iot_device():
    path_file = os.path.abspath("IoT_device.py")
    comando = f'start cmd /k "python {path_file} {"create_new_decive"} {iot} {cipher_mode} {sensor_selected} {timer_msg}"'
    subprocess.call(comando, shell=True)

def main_interface():
    global cipher_mode
    global sensor_selected 
    global timer_msg
    global iot
    while True:
        cipher_mode, sensor_selected, timer_msg = 0,0,0
        print('------------------------------------------------')
        print('---------- Creación de Dispositos IoT ----------')
        print('------------------------------------------------')
        print('1. Dispositivo IoT con interfaz de entrada')
        print('2. Dispositivo IoT con interfaz de salida')
        print('3. Sensor')
        print('4. Salir')

        opcion = input('Seleccione el tipo de dispositivo a crear: ')

        if opcion == '1':
            iot = 1
            clear_screen()
            cipher_mode = sub_menu()
            if cipher_mode != 0:
                create_iot_device()
                clear_screen()
        elif opcion == '2':
            iot = 2
            clear_screen()
            cipher_mode = sub_menu()
            if cipher_mode != 0:
                create_iot_device()
                clear_screen()
        elif opcion == '3':
            iot = 3
            clear_screen()
            cipher_mode = sub_menu()
            if cipher_mode != 0:
                clear_screen()
                sensor_selected = select_sensor()
                if sensor_selected != 0:
                    while timer_msg == 0:
                        timer_msg = input('Tiempo entre mensajes(seg): ') #no permitir el enter
                        if (timer_msg == ''):
                            timer_msg = 0
                    create_iot_device()
                    clear_screen()
        elif opcion == '4':
            clear_screen()
            break
        else:
            print('Opción inválida')

main_interface()