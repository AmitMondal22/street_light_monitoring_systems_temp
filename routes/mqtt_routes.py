from fastapi import APIRouter, HTTPException,Response,Depends,Request
from controllers.user import UserController
from middleware.MyMiddleware import mw_client,mw_user,mw_user_client


# from Library.MqttLibrary import mqtt_client, MQTT_TOPIC,publish_energy_message
from Library.MqttLibraryClass import MqttLibraryClass

from controllers.device_to_server import DeviceController

from utils.response import errorResponse, successResponse
import json

from models.mqtt_model import MqttEnergyDeviceData,MqttPublishDeviceData

from hooks.update_event_hooks import update_topics

mqtt_routes = APIRouter()

mqtt_client = MqttLibraryClass("techavoiot.co.in", 1883)
# Connect to the MQTT broker
mqtt_client.connect()


# @mqtt_routes.on_event("startup")
# async def startup_event():
#     mqtt_client.subscribe([("hello", 0),("hello1", 0)])
 
@mqtt_routes.on_event("startup")
async def startup_event():
    await subscribe_topics()

# =========================================================
# MQTT TOPIC

async def subscribe_topics():
    try:
        data = await update_topics()
        print("data",data)
        mqtt_client.subscribe(data)
    except Exception as e:
        print(e)
        
# =========================================================
@mqtt_routes.post("/publish/")
async def publish_message(message_data: MqttEnergyDeviceData):
    try:
        # mqtt_client = MqttLibraryClass("test/topic")
        mqtt_client.publish(f"slms/{message_data.ib_id}/{message_data.device}", message_data.json(), qos=0)
        return {"message": "Message published successfully"}
    except Exception as e:
        return {"error": str(e)}

@mqtt_routes.post("/publish_schedule", dependencies=[Depends(mw_user_client)])
async def publish_message(request: Request, message_data: MqttPublishDeviceData):
    try:
        user_data=request.state.user_data
        data= await DeviceController.device_schedule_settings(user_data, message_data)
        # mqtt_client.publish(f"SCHEDULING/{message_data.device_type}/{user_data['client_id']}/{message_data.device}", message_data.json(), qos=0)
        # print(f"SCHEDULING/{message_data.device_type}/{user_data['client_id']}/{message_data.device}")
        # *scheduling,123,21321,65456,545.132#
        #scheduling/EN/1/ABCDE01003
        #SCHEDULING/{message_data.device_type}/{user_data['client_id']}/{message_data.device}
        resdata = successResponse(data, message="Message published successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
