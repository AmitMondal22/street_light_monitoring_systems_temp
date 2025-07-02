from fastapi import APIRouter, HTTPException,Response,Depends,Request
from controllers.user import UserController
from middleware.MyMiddleware import mw_client,mw_user,mw_user_client


# from Library.MqttLibrary import mqtt_client, MQTT_TOPIC,publish_energy_message
from Library.MqttLibraryClass import MqttLibraryClass

from controllers.device_to_server import DeviceController

from utils.response import errorResponse, successResponse
import json

from models.mqtt_model import MqttEnergyDeviceData,MqttPublishDeviceData,MqttGroupPublishDeviceData

from hooks.update_event_hooks import update_topics

mqtt_routes = APIRouter()

mqtt_client = MqttLibraryClass("62.72.31.243", 1883,'ibfps','ib8520')
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
        print("KKKKKKKKKKKKK",data['device_type']['device_type'])
        if data['device_type']['device_type'] == 'MQTT':
            if message_data.device_mode == 2 or message_data.device_mode == "2":
                paydaya=data['paydata_data']
                paydaya = paydaya.replace('ZZ#', f"{data['device_type']['lat']},{data['device_type']['lon']},ZZ#")
                
                mqtt_client.publish(f"/SL/SCHEDULING/{message_data.device}", paydaya, qos=0)
                print(f"/SL/SCHEDULING/{message_data.device}", paydaya)
            else:
                mqtt_client.publish(f"/SL/SCHEDULING/{message_data.device}", data['paydata_data'], qos=0)
                print(f"/SL/SCHEDULING/{message_data.device}", data['paydata_data'])
        resdata = successResponse(data, message="Message published successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")




@mqtt_routes.post("/publish_group_schedule", dependencies=[Depends(mw_user_client)])
async def publish_message(request: Request, message_data: MqttGroupPublishDeviceData):
    try:
        user_data=request.state.user_data
        deviceData=await DeviceController.device_data(message_data)
        
        

        print("Publishing message",deviceData)
        for item in deviceData:
            try:
               data = await DeviceController.device_group_schedule_settings(user_data, message_data,item['device'],item['device_id'])
            #    data = await DeviceController.device_group_schedule_settings(user_data, message_data,item['device'],item['device_id'])
            #    data = await DeviceController.device_group_schedule_settings(user_data, message_data,item['device'],item['device_id'])
               print("Data",data)
            except Exception as e:
                print(e)
        print("Publishing message",deviceData)
        
        try:
            await DeviceController.add_update_group(user_data, message_data)
        except Exception as e:
            print(e)
        
            # await DeviceController.group_device_schedule_settings(user_data, message_data,item['device'],item['device_id'])
        # resdata = successResponse(data, message="Message published successfully")
        return Response(content=json.dumps(True), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error2wq 
        raise HTTPException(status_code=500, detail="Internal server error")
