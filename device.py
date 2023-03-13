import json
import paho.mqtt.client as mqtt
import codecs
from cryptography.fernet import Fernet

key = b'ppppppppppppppppppppppppppppppppppppppppppp='

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    f = Fernet(key)
    data = json.loads(f.decrypt(msg.payload))
    print(msg.topic+" "+str(data['data']))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

a = client.connect("broker.hivemq.com", 1883, 60)
client.subscribe("/fran192837/device", qos=0)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

