from fastapi import HTTPException
import requests
import json
import base64
from typing import Any
from fastapi.encoders import jsonable_encoder
import time


api_key = 'NNSXS.SKSGTTX6IIDKM7THS3RATJBRL5ZHMKO4A6ZBGXY.WVF3AVQVGOAVWK3E7CIGPVLXPHREIL5D5FXJCK5E2BCKZWL6PAVA'
application_id = 'streetlighttechavo'
device_id = 'eui-0080e115002b5637'

@staticmethod
async def uplink(user, params):
    try:
        return "data"
    except Exception as e:
        raise e
    

@staticmethod
def send_downlink(user: Any, params: Any) -> dict:
    # Replace these values with your actual values
   

    url = f'https://eu1.cloud.thethings.network/api/v3/as/applications/{application_id}/devices/{device_id}/packages/storage/uplink_message'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'text/event-stream'
    }
    # Use params argument provided to the method
    response_params = params or {
        'limit': 10,
        'after': '2020-08-20T00:00:00Z'
    }

    response = requests.get(url, headers=headers, params=response_params)

    if response.status_code == 200:
        return response.json()  # Convert the response to a dictionary
    else:
        # Optionally, handle errors more gracefully
        return {'error': f'Error: {response.status_code} - {response.text}'}
        
    
@staticmethod
async def webhooks_send_downlink():
   
    frm_payload = "R1, ,1,10,22,17,30,24,7,2024,16,07,33,ZZ"

    # Encode the string to bytes first
    frm_payload_bytes = frm_payload.encode('utf-8')

    # Base64 encode the bytes
    encoded_payload = base64.b64encode(frm_payload_bytes)
    encoded_string = encoded_payload.decode('utf-8')
    
    # time.sleep(2)
    url = "https://eu1.cloud.thethings.network/api/v3/as/applications/streetlighttechavo/webhooks/test/devices/eui-0080e115002b5637/down/replace"

    print(encoded_string)
    print("///////////////////////")
    payload = json.dumps({
    "downlinks": [
        {
        "frm_payload": encoded_string,
        "f_port": 15,
        "priority": "NORMAL"
        }
    ]
    })
    print(payload)
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer NNSXS.SKSGTTX6IIDKM7THS3RATJBRL5ZHMKO4A6ZBGXY.WVF3AVQVGOAVWK3E7CIGPVLXPHREIL5D5FXJCK5E2BCKZWL6PAVA'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return{'success': 'Downlink sent successfully'}



@staticmethod
async def webhooks_send_downlink_test(dev_eui: str, payload: str):
   
    # frm_payload = uid

    # Encode the string to bytes first
    # frm_payload_bytes = frm_payload.encode('utf-8')

    # Base64 encode the bytes
    # encoded_payload = base64.b64encode(frm_payload_bytes)
    # encoded_string = encoded_payload.decode('utf-8')
    
    # time.sleep(2)
    # url = f"http://lora.techavo.in:8080/api/devices/{encoded_string}/queue"
    url = f"http://lora.techavo.in:8080/api/devices/{dev_eui}/queue"

    # print(encoded_string)
    print("///////////////////////")
    data = {
        "confirmed": False,
        "f_port": 1,  # Use a valid f_port value
        "data": payload,
        "devEUI": dev_eui,
        "fCnt": 0,
        "fPort": 0,
        "jsonObject": "string"
    }
    print(payload)
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiYTBmOTUzZTQtNWRlMi00NDhiLWJiMmQtYWQxOTM3OTMxMGRlIiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTcyMjk0NDE5Miwic3ViIjoiYXBpX2tleSJ9.ep4D5-YaGQru0o0ur77TK5CuwtFFNPlQaSu0zfrw6Lo",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=data)
    # response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return{'success': 'Downlink sent successfully'}