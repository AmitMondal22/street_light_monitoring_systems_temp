from fastapi import APIRouter, HTTPException,Request
from controllers.api import LoraApi
from typing import Dict, Any
import base64
from controllers.device_to_server import EnergyController
from models import device_data_model
from models.webhooks_model import WhDownlinkParams

from db_model.MASTER_MODEL import select_data, insert_data,select_one_data,select_last_data,update_data

from utils.base64 import decode_base64
import json


webhooks_routes = APIRouter()






@webhooks_routes.post("/testing")
@webhooks_routes.get("/testing")
async def testing(request: Request):
    try:
        data = await request.json()
        frm_payload_base64 = data["uplink_message"]["frm_payload"]
        frm_payload_bytes = base64.b64decode(frm_payload_base64)
        data_str = frm_payload_bytes.decode('utf-8')
        data_list = data_str.split(',')
        
        
        
        # UID,VOLTAGE,CURRENT,REALPOWER,PF,KWH,RUNHR,frequencyUPLOADFLAG,DOMODE,sensorflag
        device_data = device_data_model.StreetLightDeviceData(
            CLIENT_ID = 1,
            UID=data_list[0],
            TW=1.0,  # TW is not provided in the data_list, so assign a default or calculated value
            VOLTAGE=float(data_list[1]),
            CURRENT=float(data_list[2]),
            REALPOWER=float(data_list[3]),
            PF=float(data_list[4]),
            KWH=float(data_list[5]),
            RUNHR=float(data_list[6]),
            FREQ=float(data_list[7]),
            UPLOADFLAG=int(data_list[8]),
            DOMODE=int(data_list[9]),
            SENSORFLAG=int(data_list[10])  # SENSORFLAG is not provided in the data_list, so assign a default or calculated value
        )
        # request_data = device_data.json()
        request_data = device_data
        
        abc = await LoraApi.webhooks_send_downlink()
        zzz = await EnergyController.get_energy_data(request_data,1,data_list[0])
        return {"status":"success"}
    except Exception as e:
        raise e
    
    
    

@webhooks_routes.post("/sl-webhooks")
@webhooks_routes.get("/sl-webhooks")
async def testing2(request: Request,event: str):
    # try:
    if event != "up":
      return {"status":"success"}   
    else:
        
        event =  await request.json()
        # Extract Device EUI and the uplink payload
        dev_eui = event.get("devEUI")
        decodedev_eui=decode_base64(dev_eui)
        print(">>>>>>>>>>>>>>>>>>>>>>>decodedev_eui",decodedev_eui)

        uplink_data = event.get("data")
        print("uplink_data",uplink_data)
        decodeuplink_data=base64.b64decode(uplink_data).decode('utf-8')  
        data_list = decodeuplink_data.split(',')
        
        # TECH000001,0.00,0.00,0.00,0.00,0.00,0.50,0.00,1,1,0
        
        # UID,VOLTAGE,CURRENT,REALPOWER,PF,KWH,RUNHR,frequencyUPLOADFLAG,DOMODE,sensorflag
        device_data = device_data_model.StreetLightDeviceData(
            CLIENT_ID = 1,
            UID=data_list[0],
            TW=1.0,  # TW is not provided in the data_list, so assign a default or calculated value
            VOLTAGE=float(data_list[1]),
            CURRENT=float(data_list[2]),
            REALPOWER=float(data_list[3]),
            PF=float(data_list[4]),
            KWH=float(data_list[5]),
            RUNHR=float(data_list[6]),
            FREQ=float(data_list[7]),
            UPLOADFLAG=int(data_list[8]),
            DOMODE=int(data_list[9]),
            SENSORFLAG=int(data_list[10])  # SENSORFLAG is not provided in the data_list, so assign a default or calculated value
        )
        
        select="sunrise_hour, sunrise_min, sunset_hour, sunset_min,device,device_id,device"
        condition = f"device={decodedev_eui}"
        
        stdata = select_one_data("st_sl_settings_scheduling",select,condition,order_by=None)
        print("stdata",stdata)
        # paydata =f"*R1, ,1,{sunrise['hour']},{sunrise['min']},{sunset['hour']},{sunset['min']},{get_current_datetime_string()},0,ZZ#"
        paydata="*R1, ,1,10,22,17,30,23,7,2034,16,07,33,ZZ#"
        
        # *R1, ,datalogtimeMin,SRHR,SRMM,SSHR,SSMM,DD,MM,YYYY,HR,MM,SS,ZZ#

        #     Ex:
        #     *R1, ,1,10,22,17,30,23,7,2034,16,07,33,ZZ#
        await LoraApi.webhooks_send_downlink_test(decodedev_eui, paydata)
        await EnergyController.get_energy_data(device_data,1,data_list[0])

      
        print("?????????????????????????????????????")
        return {"status":"success"}
    # except Exception as e:
    #     raise e

@webhooks_routes.post("/testing22")
@webhooks_routes.get("/testing22")
async def testing2(request: Request):
    # try:
         # Parse the incoming webhook request
        event = await request.json()
        print("event",event)

        # Extract Device EUI and the uplink payload
        dev_eui = event.get("devEUI")
        print(">>>>>>>>>>>>>>>>>>>>>>>devEUI",dev_eui)
        decodedev_eui=decode_base64(dev_eui)
        print(">>>>>>>>>>>>>>>>>>>>>>>decodedev_eui",decodedev_eui)
        
        
        
        uplink_data = event.get("data")
        print("dev_eui",dev_eui)

        
        
        # Send a downlink message
        await LoraApi.webhooks_send_downlink_test(decodedev_eui, "hello")

        # return {"message": "Uplink processed and downlink queued"}
        
        
        
        # # UID,VOLTAGE,CURRENT,REALPOWER,PF,KWH,RUNHR,frequencyUPLOADFLAG,DOMODE,sensorflag
        # device_data = device_data_model.StreetLightDeviceData(
        #     CLIENT_ID = 1,
        #     UID=data_list[0],
        #     TW=1.0,  # TW is not provided in the data_list, so assign a default or calculated value
        #     VOLTAGE=float(data_list[1]),
        #     CURRENT=float(data_list[2]),
        #     REALPOWER=float(data_list[3]),
        #     PF=float(data_list[4]),
        #     KWH=float(data_list[5]),
        #     RUNHR=float(data_list[6]),
        #     FREQ=float(data_list[7]),
        #     UPLOADFLAG=int(data_list[8]),
        #     DOMODE=int(data_list[9]),
        #     SENSORFLAG=int(data_list[10])  # SENSORFLAG is not provided in the data_list, so assign a default or calculated value
        # )
        # # request_data = device_data.json()
        # request_data = device_data
        
        # abc = await LoraApi.webhooks_send_downlink_test(data['devEUI'])
        # zzz = await EnergyController.get_energy_data(request_data,1,data_list[0])
        return {"status":"success"}
    # except Exception as e:
    #     raise e
    
    
@webhooks_routes.post("/street_light_scheduler")
async def street_light_scheduler(params:WhDownlinkParams):
    try:
        # print("???????????????????????????")
        params_json = params.json()
        downlink_data = base64.b64encode(params_json.encode()).decode()
        print("Request data",downlink_data)
        # Example usage:
        current_application_id = "testapplication"
        fPort = 2
        await LoraApi.manage_devices(current_application_id, downlink_data, fPort)
        return {"status":"success"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    