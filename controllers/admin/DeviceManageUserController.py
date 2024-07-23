from db_model.MASTER_MODEL import select_data, insert_data,update_data,delete_data
from utils.date_time_format import get_current_datetime

@staticmethod
def add_device(device):
    try:
        current_datetime = get_current_datetime()
        columns = "client_id,organization_id, user_id, device_id,device, created_by, created_at"
        value = f"{device.client_id},{device.organization_id}, {device.user_id}, {device.device_id},'{device.device}', '{device.created_by}', '{current_datetime}'"
        device_id = insert_data("md_manage_user_device", columns, value)
        print(device_id)
        if device_id is None:
            raise ValueError("device registration failed")
        else:
            device_data = {"device_id": device_id, "client_id": device.client_id, "organization_id": device.organization_id, "user_id": device.user_id, "device_id": device.device_id, "device": device.device, "created_by": device.created_by, "created_at": current_datetime}
        return device_data
    except Exception as e:
        raise e
    
    
@staticmethod
def list_user_device(params):
    try:
        select="o.organization_name,o.organization_id,u.user_id,u.user_name,u.user_email,u.user_active_status,d.device_id,d.device,d.do_channel,d.model,d.lat,d.lon,d.imei_no,d.device_type,d.meter_type, mud.manage_user_device_id"
        
        table="md_manage_user_device AS mud, users AS u, md_device AS d, md_organization  AS o"
        condition=f"mud.user_id = u.user_id AND mud.device_id = d.device_id AND o.organization_id=mud.organization_id AND o.client_id={params.client_id} AND d.device_type='EN'"
        
        
        data = select_data(table, select,condition)
        return data
    except Exception as e:
        raise e

@staticmethod
def edit_device(device):
    try:
        condition = f"manage_user_device_id = {device.manage_user_device_id} AND client_id = {device.client_id}"
        columns={"organization_id":device.organization_id, "user_id":device.user_id, "device_id":device.device_id,"device":device.device, "created_by":device.created_by,"updated_at":get_current_datetime()}
        data = update_data("md_manage_user_device", columns, condition)
        print(data)
        return data
    except Exception as e:
        raise e

@staticmethod
def delete_device(device):
    try:
        condition = f"manage_user_device_id = {device.manage_user_device_id} AND client_id = {device.client_id}"
        data = delete_data("md_manage_user_device", condition)
        return data
    except Exception as e:
        raise e