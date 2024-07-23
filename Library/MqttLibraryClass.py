import paho.mqtt.client as mqtt
from controllers.device_to_server import EnergyController
from Library.DotDictLibrary import DotDictLibrary
import json
import asyncio

class MqttLibraryClass:
    def __init__(self, broker_address, broker_port):
        self.client = mqtt.Client()
        self.broker_address = broker_address
        self.broker_port = broker_port
        # Callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.subscriptions = []

    def on_connect(self, client, userdata, flags, rc):
        for topic, qos in self.subscriptions:
            client.subscribe(topic, qos=qos)

    def on_message(self, client, userdata, msg):
        try:
            topic_name=msg.topic
            parts = topic_name.split('/')
            reqdata=DotDictLibrary(json.loads(msg.payload.decode('utf-8')))
            asyncio.run(EnergyController.get_energy_data(reqdata,parts[1],parts[2]))
        except Exception as e:
            print("Error in on_message",e)
    

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port, 60)
        self.client.loop_start()

    def subscribe(self, topics):
        for topic, qos in topics:
            self.subscriptions.append((topic, qos))
            if self.client.is_connected():
                self.client.subscribe(topic, qos=qos)

    def publish(self, topic, message, qos=0):
        self.client.publish(topic, message, qos=qos)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()