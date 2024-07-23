
from db_model.MqttData import mqtt_topic_name
async def update_topics():
    # Retrieve topics from the database
    data = await mqtt_topic_name()

    # Generate SLMS topic names
    slms_topics = [("slms/" + data[i]['concatenated_string'], 0) for i in range(len(data))]

    

    # Combine SLMS and UPSMS topic lists
    all_topics = slms_topics

    return all_topics