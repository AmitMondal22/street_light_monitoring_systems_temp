from fastapi import HTTPException
import requests
import json
import base64
from typing import Any

@staticmethod
async def uplink(user, params):
    try:
        return "data"
    except Exception as e:
        raise e
    

@staticmethod
def send_downlink(user: Any, params: Any) -> dict:
    try:
        payload = {
            "downlinks": [
                {
                    "frm_payload": "vu8=",
                    "f_port": 15,
                    "priority": "NORMAL"
                }
            ]
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer NNSXS.SKSGTTX6IIDKM7THS3RATJBRL5ZHMKO4A6ZBGXY.WVF3AVQVGOAVWK3E7CIGPVLXPHREIL5D5FXJCK5E2BCKZWL6PAVA',
        }
        
        url = 'https://eu1.cloud.thethings.network/api/v3/as/applications/streetlighttechavo/webhooks/test/devices/eui-0080e115002b5016/down/replace'
        
        # Perform a synchronous POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if the request was successful
        response.raise_for_status()

        try:
            return response.json()  # Return the JSON response
        except ValueError:
            raise HTTPException(status_code=500, detail="Invalid JSON response from the server")

    except requests.HTTPError as e:
        # Handle HTTP error responses
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except requests.RequestException as e:
        # Handle general request exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred while making the request: {str(e)}")
    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
    
@staticmethod
def webhooks_send_downlink():
    try:
        payload = {
            "downlinks": [
                {
                    "frm_payload": "vu8=",
                    "f_port": 15,
                    "priority": "NORMAL"
                }
            ]
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer NNSXS.SKSGTTX6IIDKM7THS3RATJBRL5ZHMKO4A6ZBGXY.WVF3AVQVGOAVWK3E7CIGPVLXPHREIL5D5FXJCK5E2BCKZWL6PAVA',
        }
        
        url = 'https://eu1.cloud.thethings.network/api/v3/as/applications/streetlighttechavo/webhooks/test/devices/eui-0080e115002b5637/down/replace'
        
        # Perform a synchronous POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if the request was successful
        response.raise_for_status()

        try:
            return response.json()  # Return the JSON response
        except ValueError:
            raise HTTPException(status_code=500, detail="Invalid JSON response from the server")

    except requests.HTTPError as e:
        # Handle HTTP error responses
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except requests.RequestException as e:
        # Handle general request exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred while making the request: {str(e)}")
    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")