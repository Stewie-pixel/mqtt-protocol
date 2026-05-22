import paho.mqtt.client as mqtt
import time, random, json

BROKER   = 'localhost'
PORT     = 1883
TOPIC    = 'home/livingroom/temperature'
CLIENT_ID = 'sensor-001'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('[Publisher] Connected to broker')
    else:
        print(f'[Publisher] Connection failed, code {rc}')

client = mqtt.Client(client_id=CLIENT_ID)

# Last Will and Testament
client.will_set('home/livingroom/status',
                payload=json.dumps({'status': 'offline', 'sensor': CLIENT_ID}),
                qos=1, retain=True)

client.on_connect = on_connect
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

# Publish retained 'online' status
client.publish('home/livingroom/status',
               json.dumps({'status': 'online', 'sensor': CLIENT_ID}),
               qos=1, retain=True)
try:
    while True:
        reading = {
            'sensor': CLIENT_ID,
            'temperature': round(random.uniform(18.0, 27.0), 2),
            'humidity':    round(random.uniform(40.0, 65.0), 2),
            'timestamp':   time.time()
        }
        client.publish(TOPIC, json.dumps(reading), qos=1)
        print(f'[Publisher] Sent: {reading}')
        time.sleep(2)
except KeyboardInterrupt:
    print('[Publisher] Shutting down...')
    client.disconnect()