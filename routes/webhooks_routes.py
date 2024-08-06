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
    


@webhooks_routes.post("/testing2")
@webhooks_routes.get("/testing2")
async def testing2(request: Request):
    # try:
        data = await request.json()
        print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZrequest",data['devEUI'])
        # frm_payload_base64 = data["uplink_message"]["frm_payload"]
        # frm_payload_bytes = base64.b64decode(frm_payload_base64)
        # data_str = frm_payload_bytes.decode('utf-8')
        # data_list = data_str.split(',')
        
        
        
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
        
        abc = await LoraApi.webhooks_send_downlink_test(data.devEUI)
        # zzz = await EnergyController.get_energy_data(request_data,1,data_list[0])
        return {"status":"success"}
    # except Exception as e:
    #     raise e