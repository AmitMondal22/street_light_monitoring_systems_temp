from fastapi import APIRouter, HTTPException, Response,WebSocket,WebSocketDisconnect,Depends,Request

from controllers.admin import ClientController, ManageUserController, DeviceManageUserController,DeviceController
from controllers.unit import UnitController
from controllers.alert import AlertController
from controllers.report import ReportAnalysisController
from controllers.settings import ClientSettingsController
from controllers.api import LoraApi

from models.organization_model import AddOrganization, EditOrganization, DeleteOrganization,ListOrganization
from models.manage_user_model import AddUser, EditUser,DeleteUser,UserDeviceAdd,UserDeviceEdit,UserDeviceDelete,ListUsers,UserInfo,ClientId,DeviceInfo
from models.device_data_model import EnergyData,AddAlert,DeviceAdd,DeviceEdit,EditAlert,DeleteAlert,EnergyUsed, VoltageData,OrganizationSettings,OrganizationSettingsList,AddBill,EditOrganization,DeviceSchedule
from models.report_model import EnergyUsageBilling
from models.client_settings import ClientScreenSettings, ClientScreenSettingsEdit

from Library.DecimalEncoder import DecimalEncoder
from Library.CustomEncoder import CustomEncoder
from Library import EmailLibrary
from Library.WsConnectionManager import WsConnectionManager

from db_model.MASTER_MODEL import select_one_data

from middleware.MyMiddleware import mw_client,mw_user,mw_user_client

from utils.response import errorResponse, successResponse
from typing import List
import json

api_client_routes = APIRouter()
manager = WsConnectionManager()

# ==========================================================================
# ==========================================================================

# both
@api_client_routes.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Received:{data}",websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_personal_message("Bye!!!",websocket)
        
#  send_message      
@api_client_routes.get("/send_message", dependencies=[Depends(mw_client)])
async def send_message(message: str):
    await manager.broadcast(message)
    return {"message": "Sent message: {}".format(message)}

# daynamic data
@api_client_routes.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(user_id, f"Message '{data}' received from user {user_id}")
    except Exception as e:
        manager.disconnect(user_id)
        print(f"Connection with user {user_id} closed.")
        
# @api_client_routes.post("/send_message/{user_id}")
# async def send_message(user_id: int, message: str):
#     await manager.send_personal_message(user_id, message)
#     return {"message": "Message sent successfully"}


@api_client_routes.post("/send_message/{client_id}/{device_id}/{device}/{message}", dependencies=[Depends(mw_client)])
async def send_message(client_id: int,device_id:int,device:str, message: str):
    await manager.send_personal_message(client_id, device_id, device, json.dumps(message))
    return {"message": "Message sent successfully"}


@api_client_routes.websocket("/ws/{client_id}/{device_id}/{device}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, device_id: str, device: str):
    await manager.connect(client_id, device_id, device, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(client_id, device_id, device, f"Message '{data}' received from user {client_id}-{device_id}-{device}")
    except Exception as e:
        manager.disconnect(websocket,client_id, device_id, device)
        print(f"Connection with user {client_id}-{device_id}-{device} closed.")


# ================================================================
# ================================================================
class SendEnergySocket:
    @staticmethod
    async def send_last_energy_data(client_id, device_id, device):
        try:
            # Lazy import inside the function
            # from Library import WsConnectionManager
            # manager = WsConnectionManager.WsConnectionManager()
            
            select="energy_data_id, client_id, device_id, voltage, current, realpower, pf, kwh, runhr, frequency, domode, sensor_flag, upload_flag, date, time, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at"
            condition = f"device_id = '{device_id}' AND device ='{device}' AND client_id = '{client_id}'"
            order_by="energy_data_id DESC"
                
            lastdata = select_one_data("td_energy_data", select, condition, order_by)
           
            await manager.send_personal_message(client_id, device_id, device, json.dumps(lastdata, cls=DecimalEncoder))
            
            # await manager.send_personal_message(client_id, device_id, device, json.dumps("hello134"))
            
            
            # await manager.send_personal_message(1, 1, "aa", json.dumps("hello world"))
            print("lastdata last energy data>>>>>>>>>>/////////",lastdata)
            return lastdata
        except Exception as e:
            raise ValueError("Could not fetch data")
# ================================================================
# ================================================================
  

  
# ==========================================================================
# ==========================================================================


@api_client_routes.post("/manage_organization/add", dependencies=[Depends(mw_client)])
async def add_organization(request: Request,organization:AddOrganization):
    try:
        data = ClientController.add_organization(organization)   
        resdata = successResponse(data, message="User registered successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
    
    
@api_client_routes.post("/manage_organization/list", dependencies=[Depends(mw_user_client)])
async def list_organization(request: Request,params:ListOrganization):
    try:
        # print(params)
        user_data=request.state.user_data
        data = ClientController.list_organization(params,user_data)
        resdata = successResponse(data, message="List of organizations")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    
@api_client_routes.post("/manage_organization/edit", dependencies=[Depends(mw_client)])
async def edit_organization(request: Request,organization:EditOrganization):
    try:
        data = ClientController.edit_organization(organization)
        resdata = successResponse(data, message="List of organizations")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error ")
    

@api_client_routes.post("/manage_organization/delete", dependencies=[Depends(mw_client)])
async def delete_organization(request: Request,organization:DeleteOrganization):
    try:
        data = ClientController.delete_organization(organization)
        resdata = successResponse(data, message="Organization deleted successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error ")



# ==========================================================================
# ==========================================================================



@api_client_routes.post("/manage_user/add", dependencies=[Depends(mw_client)])
async def add_user(request: Request,user:AddUser):
    try:
        data = ManageUserController.add_user(user)   
        resdata = successResponse(data, message="User registered successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    
@api_client_routes.post("/manage_user/list", dependencies=[Depends(mw_client)])
async def list_user(request: Request,params:ListUsers):
    try:
        data = ManageUserController.list_user(params)
        resdata = successResponse(data, message="List of users")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    
@api_client_routes.post("/manage_user/list_user", dependencies=[Depends(mw_client)])
# @api_client_routes.get("/manage_user/list_user/{user_id}")
async def list_user(request: Request,params:UserInfo):
    try:
        data = ManageUserController.user_info(params)
        resdata = successResponse(data, message="List of users")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    
@api_client_routes.post("/manage_user/edit", dependencies=[Depends(mw_client)])
async def edit_user(request: Request,user:EditUser):
    try:
        data = ManageUserController.edit_user(user)
        resdata = successResponse(data, message="List of users")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error ")


@api_client_routes.post("/manage_user/delete", dependencies=[Depends(mw_client)])
async def delete_user(request: Request,user:DeleteUser):
    try:
        data = ManageUserController.delete_user(user)
        resdata = successResponse(data, message="User deleted successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error ")
    
# =================================================================================================
# =================================================================================================



@api_client_routes.post("/manage_user/add_device", dependencies=[Depends(mw_client)])
async def add_device(request: Request,user:UserDeviceAdd):
    try:
        data = DeviceManageUserController.add_device(user)
        resdata = successResponse(data, message="Device added successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    
@api_client_routes.post("/manage_user/list_user_device", dependencies=[Depends(mw_client)])
async def list_user_device(request: Request,params:ClientId):
    try:
        data = DeviceManageUserController.list_user_device(params)
        resdata = successResponse(data, message="List of users")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@api_client_routes.post("/manage_user/edit_user_device", dependencies=[Depends(mw_client)])
async def edit_user_device(request: Request,user:UserDeviceEdit):
    try:
        data = DeviceManageUserController.edit_device(user)
        resdata = successResponse(data, message="List of user devices")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error ")
    
    
@api_client_routes.post("/manage_user/delete_user_device", dependencies=[Depends(mw_client)])
async def delete_user_device(request: Request,user:UserDeviceDelete):
    try:
        data = DeviceManageUserController.delete_device(user)
        resdata = successResponse(data, message="List of users")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error ")
    
# =================================================================================================
# =================================================================================================

@api_client_routes.post("/devices/list", dependencies=[Depends(mw_user_client)])
async def list_device(request: Request):
    try:
        user_credentials = request.state.user_data
        client_id=user_credentials['client_id']
        if user_credentials["user_type"] == "U":
            user_id=user_credentials["user_id"]
            organization_id=user_credentials["organization_id"]
            data= await DeviceController.user_device_list(client_id, user_id, organization_id)
        else:
            data = await DeviceController.list_device(client_id)
        resdata = successResponse(data, message="List of devices")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
    
@api_client_routes.post("/devices/device_info", dependencies=[Depends(mw_user_client)])
async def list_device(request: Request,params:DeviceInfo):
    try:
        userdata=request.state.user_data
        data = await DeviceController.device_info(params,userdata)
        resdata = successResponse(data, message="List of devices")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    


# @api_client_routes.post("/manage/devices/add")
@api_client_routes.post("/manage/devices/add", dependencies=[Depends(mw_client)])
async def add_device(request: Request,params:List[DeviceAdd]):
    try:
        data = await DeviceController.add_device(params)
        resdata = successResponse(data, message="Device added successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@api_client_routes.post("/manage/devices/edit", dependencies=[Depends(mw_client)])
async def edit_device(request: Request,params:DeviceEdit):
    try:
        data = await DeviceController.edit_device(params)
        resdata = successResponse(data, message="Device edited successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")



@api_client_routes.post("/manage/devices/list", dependencies=[Depends(mw_client)])
async def list_device(request: Request,params:ClientId):
    try:
        data = await DeviceController.manage_list_device(params)
        resdata = successResponse(data, message="List of devices")
        return Response(content=json.dumps(resdata, cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")

# =================================================================================================
# =================================================================================================
@api_client_routes.post("/devices/energy_data", dependencies=[Depends(mw_user_client)])
async def energy_data(request: Request,params:EnergyData):
    try:
        data = ClientController.energy_data(params)
        resdata = successResponse(data, message="devices Data")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
    
    
    
@api_client_routes.post("/devices/graphical_view/energy_used", dependencies=[Depends(mw_user_client)])
async def energy_used(request: Request,params:EnergyUsed):
    # try:
        user_data=request.state.user_data
        data = await DeviceController.energy_used(params,user_data)
        resdata = successResponse(data, message="energy used Data")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    # except ValueError as ve:
    #     raise HTTPException(status_code=400, detail=str(ve))
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Internal server error")
    


@api_client_routes.post("/devices/graphical_view/voltage", dependencies=[Depends(mw_user_client)])
async def voltage_data(request: Request,params:EnergyUsed):
    try:
        user_data=request.state.user_data
        data = await DeviceController.voltage_data(params,user_data)
        resdata = successResponse(data, message="Voltage Data")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@api_client_routes.post("/devices/graphical_view/current", dependencies=[Depends(mw_user_client)])
async def current_data(request: Request,params:EnergyUsed):
    try:
        user_data=request.state.user_data
        data = await DeviceController.current_data(params,user_data)
        resdata = successResponse(data, message="Current Data")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    

@api_client_routes.post("/devices/graphical_view/power", dependencies=[Depends(mw_user_client)])
async def power_data(request: Request,params:EnergyUsed):
    try:
        user_data=request.state.user_data
        data = await DeviceController.power_data(params,user_data)
        resdata = successResponse(data, message="Power Data")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
# @api_client_routes.post("/devices/graphical_view/total_power_analisis", dependencies=[Depends(mw_user_client)])
# async def  total_power_analisis(request: Request,params:EnergyUsed):
#     try:
#         user_data=request.state.user_data
#         data = await DeviceController.total_power_analisis(params,user_data)
#         resdata = successResponse(data, message="Total Power Analisis Data")
#         return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail=str(ve))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")


# =================================================================================================
# =================================================================================================










# =================================================================================================
# =================================================================================================



# @api_client_routes.post("/unit/list", dependencies=[Depends(mw_client)])
@api_client_routes.post("/unit/list")
async def list_unit(request: Request):
    try:
        data = await UnitController.list_unit()
        resdata = successResponse(data, message="List of units")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    

@api_client_routes.post("/alert/add", dependencies=[Depends(mw_client)])
async def add_alert(request: Request,alert:List[AddAlert]):
    try:
        data = AlertController.add_alert(alert)
        resdata = successResponse(data, message="Alert added successfully")
        print(">>>>>>>>>>>>>>>>>>>>>",resdata)
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")

@api_client_routes.post("/alert/list", dependencies=[Depends(mw_user_client)])
async def list_alert(request: Request,params:ClientId):
    try:
        user_data=request.state.user_data
        data = await AlertController.list_alert(params,user_data)
        resdata = successResponse(data, message="List of alerts")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    
@api_client_routes.post("/alert/edit", dependencies=[Depends(mw_client)])
async def edit_alert(request: Request,params:EditAlert):
    try:
        data = await AlertController.edit_alert(params)
        resdata = successResponse(data, message="Alert edited successfully")
        return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")

@api_client_routes.post("/alert/delete", dependencies=[Depends(mw_client)])
async def delete_alert(request: Request,params:DeleteAlert):
    try:
        data = await AlertController.delete_alert(params)
        if data > 0:
            resdata = successResponse(data, message="Alert deleted successfully")
            return Response(content=json.dumps(resdata), media_type="application/json", status_code=200)
        else:
            resdata = errorResponse(message="Alert not deleted successfully")
            return Response(content=json.dumps(resdata), media_type="application/json", status_code=404)
    except ValueError as ve:
        # If there's a ValueError, return a 400 Bad Request with the error message
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For any other unexpected error, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
    
# ====================================================================================
# ====================================================================================


@api_client_routes.post("/organization_settings", dependencies=[Depends(mw_client)])
async def organization_settings(request: Request,params:OrganizationSettings):
    try:
        userdata=request.state.user_data
        client_id=userdata['client_id']
        user_id=userdata["user_id"]
        data = await DeviceController.organization_settings(client_id,user_id,params)
        resdata = successResponse(data, message="Organization settings")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@api_client_routes.post("/organization_settings/list", dependencies=[Depends(mw_client)])
async def organization_settings_list(request: Request,params:OrganizationSettingsList):
    try:
        userdata=request.state.user_data
        client_id=userdata['client_id']
        user_id=userdata["user_id"]
        data = await DeviceController.organization_settings_list(client_id,user_id,params)
        resdata = successResponse(data, message="Organization settings")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@api_client_routes.post("/organization_settings/old_bill_list", dependencies=[Depends(mw_client)])
async def organization_settings_old_bill_list(request: Request,params:OrganizationSettingsList):
    try:
        userdata=request.state.user_data
        client_id=userdata['client_id']
        user_id=userdata["user_id"]
        data = await DeviceController.old_bill_list(client_id,user_id,params)
        resdata = successResponse(data, message="Organization settings")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
@api_client_routes.post("/organization_settings/add_bill", dependencies=[Depends(mw_client)])
async def add_bill(request: Request,params:AddBill):
    try:
        userdata=request.state.user_data
        client_id=userdata['client_id']
        user_id=userdata["user_id"]
        data = await DeviceController.add_bill(client_id,user_id,params)
        resdata = successResponse(data, message="Organization settings")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@api_client_routes.post("/organization_settings/edit_organization_info", dependencies=[Depends(mw_client)])
async def edit_organization_info(request: Request,params:EditOrganization):
    try:
        userdata=request.state.user_data
        client_id=userdata['client_id']
        user_id=userdata["user_id"]
        data = await DeviceController.edit_organization_info(client_id,user_id,params)
        resdata = successResponse(data, message="Organization settings")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")



    
# ====================================================================================
# ====================================================================================


@api_client_routes.post("/report_analysis/energy_usage_billing", dependencies=[Depends(mw_user_client)])
async def energy_usage_billing(request: Request,params:EnergyUsageBilling):
    try:
        userdata=request.state.user_data
        data = await ReportAnalysisController.energy_usage_billing(userdata,params)
        resdata = successResponse(data, message="Organization settings")
        print(resdata)
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@api_client_routes.post("/report_analysis/new_energy_usage_billing", dependencies=[Depends(mw_user_client)])
async def new_energy_usage_billing(request: Request,params:EnergyUsageBilling):
    # try:
        userdata=request.state.user_data
        data = await ReportAnalysisController.new_energy_usage_billing(userdata,params)
        resdata = successResponse(data, message="Organization settings")
        print(resdata)
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    # except ValueError as ve:
    #     raise HTTPException(status_code=400, detail=str(ve))
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Internal server error")
    
# ===========================================================
# ===========================================================

@api_client_routes.post("/settings/client_screen_settings", dependencies=[Depends(mw_client)])
async def client_screen_settings(request: Request,params:ClientScreenSettings):
    try:
        userdata=request.state.user_data
        data = await ClientSettingsController.client_screen_settings(userdata,params)
        resdata = successResponse(data, message="Organization settings")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    



# ===========================================================
# ===========================================================
    
@api_client_routes.post("/settings/client_screen_settings_edit", dependencies=[Depends(mw_client)])
async def client_screen_settings_edit(request: Request,params:ClientScreenSettingsEdit):
    try:
        userdata=request.state.user_data
        data = await ClientSettingsController.client_screen_settings_edit(userdata,params)
        # requestlorawalapi
        await LoraApi.send_downlink(userdata, params)
        resdata = successResponse(data, message="Organization settings add and edit successfully")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@api_client_routes.post('/device_schedule', dependencies=[Depends(mw_user_client)])
async def device_schedule(request: Request,params:DeviceSchedule):
    try:
        userdata=request.state.user_data
        data = await DeviceController.get_device_schedule(userdata,params)
        resdata = successResponse(data, message="Device Schedule successfully")
        return Response(content=json.dumps(resdata,cls=DecimalEncoder), media_type="application/json", status_code=200)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")