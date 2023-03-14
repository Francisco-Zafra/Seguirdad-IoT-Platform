from time import sleep
import paho.mqtt.client as mqtt
import threading
import json
from cryptography.fernet import Fernet

key = b'ppppppppppppppppppppppppppppppppppppppppppp='

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def printit():
  threading.Timer(5.0, printit).start()
  client.publish("/fran14732832/sub", payload="token2", qos=0, retain=False)

client = mqtt.Client()
client.on_connect = on_connect

a = client.connect("broker.hivemq.com", 1883, 60)
printit()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
while 1:
  sleep(1)
    