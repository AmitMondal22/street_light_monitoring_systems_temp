from fastapi import APIRouter, HTTPException,Request
from controllers.api import LoraApi
from typing import Dict, Any


webhooks_routes = APIRouter()


@webhooks_routes.post("/testing")
@webhooks_routes.get("/testing")
async def testing(request: Request):
    # try:
        payload = await request.json()
        print(payload)
        await LoraApi.webhooks_send_downlink()
        return "data"
    # except Exception as e:
    #     raise e
    
    
@webhooks_routes.get('/abc')
async def testing():
    try:
       
        return "data"
    except Exception as e:
        raise e