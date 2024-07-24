from fastapi import APIRouter, HTTPException,Request
from controllers.api import LoraApi
from typing import Dict, Any
import base64
from controllers.device_to_server import EnergyController
from models import device_data_model


webhooks_routes = APIRouter()


@webhooks_routes.post("/testing")
@webhooks_routes.get("/testing")
async def testing(request: Request):
    # try:
        data = await request.json()
        print(data)
        print("////////////////////////////'''''''''''''''''''''''''''",data["uplink_message"])
        frm_payload_base64 = data["uplink_message"]["frm_payload"]
        frm_payload_bytes = base64.b64decode(frm_payload_base64)
        print("////////////////////////////'''''''''''''''''''''''''''",frm_payload_bytes)
        data_str = frm_payload_bytes.decode('utf-8')
        data_list = data_str.split(',')
        
        
        
        
        device_data = device_data_model.StreetLightDeviceData(
            CLIENT_ID = 1,
            UID=data_list[0],
            TW=1.0,  # TW is not provided in the data_list, so assign a default or calculated value
            VOLTAGE=float(data_list[3]),
            CURRENT=float(data_list[4]),
            REALPOWER=float(data_list[5]),
            PF=float(data_list[6]),
            KWH=float(data_list[7]),
            RUNHR=float(data_list[8]),
            FREQ=50.0,  # FREQ is not provided in the data_list, so assign a default or calculated value
            UPLOADFLAG=int(data_list[9]),
            DOMODE=int(data_list[10]),
            SENSORFLAG=0  # SENSORFLAG is not provided in the data_list, so assign a default or calculated value
        )
        request_data = device_data.json()
        
        
        # device_id = data_list[0]
        # date = data_list[1]
        # time = data_list[2]
        # VOLTAGE = float(data_list[3])
        # CURRENT = float(data_list[4])
        # REALPOWER = float(data_list[5])
        # PF = float(data_list[6])
        # KWH = float(data_list[7])
        # RUNHR = float(data_list[8])
        # UPLOADFLAG = int(data_list[9])
        # DOMODE = int(data_list[10])
        # print("Decoded frm_payload:")
        print("ZZZZZZZZZZZZZZZZZZZZZZzz")
        print(request_data)
        
        
        
        
        abc = await LoraApi.webhooks_send_downlink()
        zzz = await EnergyController.get_energy_data(request_data,1,data_list[0])
        print("ws--------------------")
        print(zzz)
        return {"status":"success"}
    # except Exception as e:
    #     raise e
    
    
@webhooks_routes.get('/abc')
async def testing():
    try:
       
        return "data"
    except Exception as e:
        raise e