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