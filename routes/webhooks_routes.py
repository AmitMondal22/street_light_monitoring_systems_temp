from fastapi import APIRouter, HTTPException,Request
from controllers.api import LoraApi
from typing import Dict, Any
import base64


webhooks_routes = APIRouter()


@webhooks_routes.post("/testing")
@webhooks_routes.get("/testing")
async def testing(request: Request):
    # try:
        data = await request.json()
        print(data)
        frm_payload_base64 = data["uplink_message"]["frm_payload"]
        frm_payload_bytes = base64.b64decode(frm_payload_base64)
        data_str = frm_payload_bytes.decode('utf-8')
        data_list = data_str.split(',')
        device_id = data_list[0]
        date = data_list[1]
        time = data_list[2]
        VOLTAGE = float(data_list[3])
        CURRENT = float(data_list[4])
        REALPOWER = float(data_list[5])
        PF = float(data_list[6])
        KWH = float(data_list[7])
        RUNHR = float(data_list[8])
        UPLOADFLAG = int(data_list[9])
        DOMODE = int(data_list[10])
        print("Decoded frm_payload:")
        print(data_list)
        
        
        
        
        abc = await LoraApi.webhooks_send_downlink()
        return {"status":"success"}
    # except Exception as e:
    #     raise e
    
    
@webhooks_routes.get('/abc')
async def testing():
    try:
       
        return "data"
    except Exception as e:
        raise e