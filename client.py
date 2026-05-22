import paho.mqtt.client as mqtt
import json

BROKER = 'localhost'
PORT   = 1883

def on_connect(mqttc, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print('[Subscriber] Connected')
        mqttc.subscribe('home/#', qos=1)
        print('[Subscriber] Subscribed to home/#')

def on_message(mqttc, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        payload = msg.payload.decode()
    print(f'[{msg.topic}] QoS={msg.qos}  |  {payload}')

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='dashboard-001')
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()