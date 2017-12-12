import time
import paho.mqtt.client as mqtt
import os
import json

DEBUG = True
Run = True

def log(message, force = False):
    if not DEBUG and not force:
        return
    print time.strftime("%H:%M:%S"), message

#mqtt
class MqttDelegate(object):
    def __init__(self, client):
        self.client = client

    def on_connect(self, client, userdata, flags, rc):
        log('MQTT connected.', True)
        nodes = os.getenv('CLIENT_NODES', 'node1,node2').split(",")
        log(nodes)
        for node in nodes:
            node = node.upper()
            log(node)
            line1 = os.getenv(node + '_LINE1', 'First line')
            log(line1)
            line2 = os.getenv(node + '_LINE2', 'Another line')
            log(line2)
            line3 = os.getenv(node + '_LINE3', '1337 yen')
            log(line3)
            client.publish('/display/' + node.lower(), json.dumps([node, line1, line2, line3]), 1, True)

mqttc = mqtt.Client('isaax-broker')
delegate = MqttDelegate(mqttc)
mqttc.on_connect = delegate.on_connect

try:
    log('Connecting to mqtt server...', True)
    mqttc.connect('localhost', port=1883, keepalive=60)
    mqttc.loop_start()
except:
    log('MQTT connection failed!', True)

log('Connected!', True)
while Run:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        log("keyboard interrupt, stopping threads")
        mqttc.loop_stop()
        break

mqttc.loop_stop()