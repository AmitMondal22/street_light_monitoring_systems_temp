# import paho.mqtt.publish as publish
# import paho.mqtt.client as mqtt

# class MqttLibraryClass:
#     def __init__(self, broker, port, topic):
#         self.broker = broker
#         self.port = port
#         self.topic = topic
#         self.client = mqtt.Client()
#         self.client.on_connect = self.on_connect
#         self.client.on_message = self.on_message
#         self.client.connect(self.broker, self.port, 60)
#         # self.client.loop_start() 
#         self.client.loop_start()

#     def on_connect(self, client, userdata, flags, rc):
#         print("Connected with result code " + str(rc))
        

#     def on_message(self, client, userdata, msg):
#         print(msg.topic + " " + str(msg.payload))
#         # Call the handle_received_message function
#         # return msg.payload.decode()

#     async def publish_message(self, message_data):
#         try:
#             message = message_data.json()
#             self.client.publish(self.topic, message)
#             return {"message": "Published message: {}".format(message)}
#         except Exception as e:
#             return {"error": str(e)}
        
#     def start_loop(self):
#         return self.client.loop_start()  # Start the MQTT client's loop

# # mqtt_client = MqttLibraryClass("techavoiot.co.in", 1883, "test/topic")



import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

class MqttLibraryClass:
    def __init__(self, broker, port):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribe to the topic when connected
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print("RReceived message on topic", msg.topic, ":", msg.payload.decode())
        # Call a function to handle the received message
        # handle_received_message(msg.topic, msg.payload.decode())

    def publish_message(self, topic, message):
        try:
            self.client.publish(topic, message)
            return {"message": "Published message: {}".format(message)}
        except Exception as e:
            return {"error": str(e)}

    def start_loop(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()  # Start the MQTT client's loop

    def set_topic(self, topic):
        self.topic = topic