from fastapi import APIRouter, HTTPException, Response
from models import auth_model
from utils.response import errorResponse, successResponse
import json

from controllers.device_to_server import DeviceController
from models import device_data_model
from Library.DecimalEncoder import DecimalEncoder

user_routes = APIRouter()


@user_routes.post("/deevice/list")
async def get_device_list(user_id: device_data_model.UserDeviceList):
    try:
        data= await DeviceController.user_device_list(user_id)
        resdata = successResponse(data, message="List of devices")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")