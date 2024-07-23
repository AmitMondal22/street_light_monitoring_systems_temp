import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt


# MQTT Broker settings
MQTT_BROKER = "techavoiot.co.in"
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"

# Create MQTT client
mqtt_client = mqtt.Client()


# =============================================
# =============================================

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)
    
# MQTT on_message callback
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# Set the callback functions
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT Broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()  # Start the loop to listen for MQTT messages



# =============================================
# =============================================



async def publish_energy_message(message_data):
    try:
        print(message_data.json())
        message = message_data.json()
        if message:
            mqtt_client.publish(MQTT_TOPIC, message)
            return message_data
        else:
            return {"error": "Message not provided in JSON data"}
    except Exception as e:
        return {"error": str(e)}

