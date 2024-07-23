from fastapi import HTTPException
import requests
import json
import base64
from typing import Any
from fastapi.encoders import jsonable_encoder


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
def webhooks_send_downlink():
    # try:
        # payload = {
        #     'downlinks': [
        #         {
        #             'frm_payload': '*hello#',
        #             'f_port': 15,
        #             'priority': 'HIGHEST'
        #             # 'priority': 'NORMAL'
        #         }
        #     ]
        # }
        
        # headers = {
        #     'Content-Type': 'application/json',
        #     'Authorization': 'Bearer NNSXS.SKSGTTX6IIDKM7THS3RATJBRL5ZHMKO4A6ZBGXY.WVF3AVQVGOAVWK3E7CIGPVLXPHREIL5D5FXJCK5E2BCKZWL6PAVA',
        # }
        
        # url = 'https://eu1.cloud.thethings.network/api/v3/as/applications/streetlighttechavo/webhooks/test/devices/eui-0080e115002b5637/down/replace'
        
        # # Perform a synchronous POST request
        # response = requests.post(url, headers=headers, json=payload)
        
        # # Check if the request was successful
        # # response.raise_for_status()
        # print("///////////////")
        # print(jsonable_encoder(response))

        # try:
        #     return {"status":"success"}  # Return the JSON response
        # except ValueError:
        #     raise HTTPException(status_code=500, detail="Invalid JSON response from the server")

    # except requests.exceptions.RequestException as e:
    #     # Handle network errors or bad responses
    #     raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    
    url = "https://eu1.cloud.thethings.network/api/v3/as/applications/streetlighttechavo/webhooks/test/devices/eui-0080e115002b5637/down/replace"

    payload = json.dumps({
    "downlinks": [
        {
        "frm_payload": "aGVsbG8=",
        "f_port": 15,
        "priority": "NORMAL"
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer NNSXS.SKSGTTX6IIDKM7THS3RATJBRL5ZHMKO4A6ZBGXY.WVF3AVQVGOAVWK3E7CIGPVLXPHREIL5D5FXJCK5E2BCKZWL6PAVA'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)