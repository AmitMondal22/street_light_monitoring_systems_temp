from fastapi import APIRouter, HTTPException,Request
from controllers.api import LoraApi
from typing import Dict, Any
import base64
from controllers.device_to_server import EnergyController
from models import device_data_model
from models.webhooks_model import WhDownlinkParams

from db_model.MASTER_MODEL import select_one_data

from utils.base64 import decode_base64
from utils.date_time_format import get_current_datetime_string
from utils.number_conversion import dec_to_num
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
        print(event)
        # Extract Device EUI and the uplink payload
        dev_eui = event.get("devEUI")
        # rssi = event.get("rxInfo")
        rxInfo = event.get("rxInfo")

        # Print RSSI value
        if rxInfo and len(rxInfo) > 0:
            rssi=rxInfo[0].get("rssi")
            # print(rxInfo[0].get("rssi"))
        else:
            rssi=0.0
        decodedev_eui=decode_base64(dev_eui)
        print(">>>>>>>>>>>>>>>>>>>>>>>decodedev_eui",decodedev_eui)

        uplink_data = event.get("data")
        print("uplink_data",uplink_data)
        decodeuplink_data=base64.b64decode(uplink_data).decode('utf-8')  
        data_list = decodeuplink_data.split(',')
        # 0         1        2        3     4   5   6    7         8          9        10         11          12  13    14   15
    #    clientid,VOLTAGE,CURRENT,REALPOWER,PF,KWH,RUNHR,frequency,UPLOADFLAG,DOMODE,sensorflag,log_sec_ref,sr_h,sr_m,ss_h,ss_m,dimming
    #    1,        0.00,    0.00,   0.00,  0.00,0.00,0.50, 0.00,       1,         1,     0,        30,        18,  0,   16,  30
                                                                                    # light status
    
    #  ['0.000', '0.00', '0.00', '0.00', '0.00', '0.50', '0.00', '1', '1', '0', '30', '18', '0', '16', '30']
        

        device_data = device_data_model.StreetLightDeviceData(
            CLIENT_ID = data_list[0],
            UID=decodedev_eui,
            TW=rssi,  # TW is not provided in the data_list, so assign a default or calculated value
            VOLTAGE=float(data_list[1]),
            CURRENT=float(data_list[2]),
            REALPOWER=float(data_list[3]),
            PF=float(data_list[4]),
            KWH=float(data_list[5]),
            RUNHR=float(data_list[6]),
            FREQ=float(data_list[7]),
            UPLOADFLAG=int(data_list[8]),
            DOMODE=int(data_list[9]),
            SENSORFLAG=int(data_list[10])
        )
        
        print("device_dataaaaaaaaaaaaaaaaaaaaaaaaaaaaa",data_list,device_data)
        # ['1', '240.82', '0.08', '0.71', '0.04', '105.7852', '105.79', '0.00', '1', '2', '0', '2', '6', '55', '18', '13', '79']
        
            # select="sunrise_hour, sunrise_min, sunset_hour, sunset_min,device,device_id,device_mode,dimming,v_rms, irms,datalog_interval"
            # condition = f"device='{decodedev_eui}'"
        # print(select,"////////////", condition)
        
        # select_one_data("md_device","device_id",f"client_id={client_id} AND device='{device}'")
        await LoraApi.update_device_schedule_settings(data_list[0],decodedev_eui,data_list[9],data_list[12],data_list[13],data_list[14],data_list[15],data_list[11],data_list[16])
            # stdata = select_one_data("st_sl_settings_scheduling",select,condition)
            # print("stdataMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",stdata['sunrise_hour'])
        #  {'sunrise_hour': '10', 'sunrise_min': '29', 'sunset_hour': '17', 'sunset_min': '38', 'device': '0080e115002b54b0', 'device_id': 28}
        # paydata =f"*R1, ,1,{sunrise['hour']},{sunrise['min']},{sunset['hour']},{sunset['min']},{get_current_datetime_string()},0,ZZ#"
        #         //*R1, ,datalogtimeMin,SRHR,SRMM,SSHR,SSMM,DD,MM,YYYY,HR,MM,SS,domode,VRMS,IRMS,ZZ#
        #   //**R1, ,1,10,32,17,46,21,08,2024,11,57,55,0,235.6,1.5,ZZ
        # paydata=f"*R1, ,{stdata['datalog_interval']},{stdata['sunrise_hour']},{stdata['sunrise_min']},{stdata['sunset_hour']},{stdata['sunset_min']},{get_current_datetime_string()},{dec_to_num(stdata['device_mode'])},{dec_to_num(stdata['v_rms'])},{dec_to_num(stdata['irms'])},ZZ#"
            # paydata=f"*R1, ,{stdata['datalog_interval']},{stdata['sunrise_hour']},{stdata['sunrise_min']},{stdata['sunset_hour']},{stdata['sunset_min']},{get_current_datetime_string()},{stdata['device_mode']},{stdata['dimming']},ZZ#"
            # print("================================",paydata)
        # paydata=f"*R1, ,1,10,22,17,30,23,7,2034,16,07,33,ZZ#"
        
        # *R1, ,datalogtimeMin,SRHR,SRMM,SSHR,SSMM,DD,MM,YYYY,HR,MM,SS,DM,ZZ#

        #     Ex:
        #     *R1, ,1,10,22,17,30,23,7,2034,16,07,33,ZZ#
        paydata=f"*DATA, ,{get_current_datetime_string()},YY#"
        await LoraApi.webhooks_send_downlink_test(decodedev_eui, paydata)
       
        
        await EnergyController.get_energy_data(device_data,1,decodedev_eui)

      
        # print("?????????????????????????????????????")
        return {"status":"success"}
    # except Exception as e:
    #     raise e
    
    
async def mqttdata_sl_data(data_list,client_id,decodedev_eui):
    # event =  await request.json()
    
    # 0         1        2        3     4   5   6    7         8          9        10         11          12  13    14   15
    #    clientid,VOLTAGE,CURRENT,REALPOWER,PF,KWH,RUNHR,frequency,UPLOADFLAG,DOMODE,sensorflag,log_sec_ref,sr_h,sr_m,ss_h,ss_m
    #    1,        0.00,    0.00,   0.00,  0.00,0.00,0.50, 0.00,       1,         1,     0,        30,        18,  0,   16,  30
                                                                                    # light status

    #  ['0.000', '0.00', '0.00', '0.00', '0.00', '0.50', '0.00', '1', '1', '0', '30', '18', '0', '16', '30']
    
    # device_data = device_data_model.StreetLightDeviceData(
    #     CLIENT_ID = data_list[0],
    #     UID=decodedev_eui,
    #     TW=rssi,  # TW is not provided in the data_list, so assign a default or calculated value
    #     VOLTAGE=float(data_list[1]),
    #     CURRENT=float(data_list[2]),
    #     REALPOWER=float(data_list[3]),
    #     PF=float(data_list[4]),
    #     KWH=float(data_list[5]),
    #     RUNHR=float(data_list[6]),
    #     FREQ=float(data_list[7]),
    #     UPLOADFLAG=int(data_list[8]),
    #     DOMODE=int(data_list[9]),
    #     SENSORFLAG=int(data_list[10])
    # )
    
    device_data = device_data_model.StreetLightDeviceData(
        CLIENT_ID = client_id,
        UID=decodedev_eui,
        TW=float(data_list.TW),  # TW is not provided in the data_list, so assign a default or calculated value
        VOLTAGE=float(data_list.VOLTAGE),
        CURRENT=float(data_list.CURRENT),
        REALPOWER=float(data_list.REALPOWER),
        PF=float(data_list.PF),
        KWH=float(data_list.KWH),
        RUNHR=float(data_list.RUNHR),
        FREQ=float(data_list.FREQ),
        UPLOADFLAG=int(data_list.UPLOADFLAG),
        DOMODE=int(data_list.DOMODE),
        SENSORFLAG=int(data_list.SENSORFLAG)
    )

    await LoraApi.update_device_schedule_settings(client_id, decodedev_eui, data_list.DOMODE, data_list.SR_H, data_list.SR_M, data_list.SS_H, data_list.SS_M,data_list.SENSORFLAG, data_list.dimming)
    await EnergyController.get_energy_data(device_data,client_id,decodedev_eui)
    return {"status":"success"}

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
    