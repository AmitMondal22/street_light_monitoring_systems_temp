from db_model.MASTER_MODEL import select_data, insert_data,select_one_data,select_last_data,update_data
from utils.date_time_format import get_current_datetime,get_time_time_firmat
from utils.utils import increment_string


from hooks.update_event_hooks import update_topics

   
@staticmethod
async def device_auto_register(data):
    try:
        select="device_id, device, do_channel, model, lat, lon, imei_no, last_maintenance,device_type,meter_type, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        find_device=select_one_data("md_device", select, f"imei_no = '{data.imei_no}' AND device_type = 'EN'")

        if find_device is not None:
            device_data={"device": find_device['device'], "do_channel": find_device['do_channel'], "model": find_device['model'], "lat": find_device['lat'], "lon": find_device['lon'], "imei_no": find_device['imei_no'], "created_at": find_device['created_at'], "updated_at": find_device['updated_at']}
            return device_data
        
        device_name = select_last_data("md_device", select,None,"created_at")
        if device_name is not None:
            u_id = increment_string(device_name['device'])
            
        else:
            # u_id = "C1TS00000001"
            u_id = "IB00000001"
        current_datetime = get_current_datetime()
        columns = "client_id, device, do_channel, model, lat, lon, imei_no, created_at"
        value = f"{data.ib_id},'{u_id}', '{data.do_channel}', '{data.model}', '{data.lat}', '{data.lon}', '{data.imei_no}', '{current_datetime}'"
        
        

        await update_topics()
        device_id = insert_data("md_device", columns, value)
        if device_id is None:
            raise ValueError("device registration failed")
        else:
            device_data = {"device_id": device_id, "device_name": u_id, "do_channel": data.do_channel, "model": data.model, "lat": data.lat, "lon": data.lon, "imei_no": data.imei_no, "created_at": current_datetime}
        return device_data
    except Exception as e:
        raise ValueError("Could not fetch data")
    
@staticmethod
async def checked_devices(data):
    try:
        select="device_id, device, do_channel, model, lat, lon, imei_no, last_maintenance,device_type,meter_type, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        condition = f"device = '{data.device}'"
        find_devices=select_one_data("md_device", select, condition,None)
        print("find_devices>>>>>>>>>>>>>>>>>",find_devices)
        if find_devices is not None:
            device_data={"device": find_devices['device'], "do_channel": find_devices['do_channel'], "model": find_devices['model'], "lat": find_devices['lat'], "lon": find_devices['lon'], "imei_no": find_devices['imei_no'], "created_at": find_devices['created_at'], "updated_at": find_devices['updated_at']}
            return device_data
        else:
            return "Device not found"
    except Exception as e:
        raise ValueError("Could not fetch data")
    
    
    

@staticmethod
async def user_device_list(data):
    try:
        select="d.device_id, d.device, d.do_channel, d.model, d.lat, d.lon, d.imei_no,d.device_type,d.meter_type, d.last_maintenance, DATE_FORMAT(d.created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(d.updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        condition = f"d.device_id = mud.device_id AND d.client_id = mud.client_id AND mud.client_id = {data.client_id} AND mud.user_id = {data.user_id} AND mud.organization_id = {data.organization_id}"
        find_devices=select_data("md_device AS d, md_manage_user_device AS mud", select, condition,None)
        print("find_devices>>>>>>>>>>>>>>>>>",find_devices)
        return find_devices
    except Exception as e:
        raise ValueError("Could not fetch data")
    
    
    
@staticmethod
async def device_schedule_settings(used_data,requestdata):
    try:
        
        current_datetime = get_current_datetime()
        select="device_scheduling_id, device_id, device, client_id, device_type, do_channel, relay_close_time, timer_start_hours, timer_start_minutes, timer_stop_hours_1, timer_stop_minutes_1, create_by"
        conditions=f"device_id = {requestdata.device_id} AND client_id = {used_data['client_id']} "
        
        find_devices=select_one_data("st_device_scheduling", select, conditions,None)
        print(find_devices)
        if find_devices is None or not find_devices:
            print("No devices found")
            columns="device_id, device, client_id, device_type, do_channel, relay_close_time, timer_start_hours, timer_start_minutes, timer_stop_hours_1, timer_stop_minutes_1, create_by,created_at"
            # row_data= f"'{current_datetime}'"
            row_data= f"{requestdata.device_id}, '{requestdata.device}', {used_data['client_id']}, '{requestdata.device_type}', {requestdata.do_channel}, '{get_time_time_firmat(requestdata.relay_close_time)}', '{get_time_time_firmat(requestdata.timer_start_hours)}', '{get_time_time_firmat(requestdata.timer_start_minutes)}', '{get_time_time_firmat(requestdata.timer_stop_hours_1)}', '{get_time_time_firmat(requestdata.timer_stop_minutes_1)}', {used_data['user_id']}, '{current_datetime}'"
            insdata=insert_data("st_device_scheduling", columns, row_data)
        else:
            print("Error inserting")
            setvalue={"relay_close_time": get_time_time_firmat(requestdata.relay_close_time), "timer_start_hours": get_time_time_firmat(requestdata.timer_start_hours), "timer_start_minutes": get_time_time_firmat(requestdata.timer_start_minutes), "timer_stop_hours_1": get_time_time_firmat(requestdata.timer_stop_hours_1), "timer_stop_minutes_1": get_time_time_firmat(requestdata.timer_stop_minutes_1), "create_by": used_data['user_id'], "updated_at": current_datetime}
            # conditions=""
            insdata=update_data("st_device_scheduling",setvalue , conditions)
        
        
        
        print("find_devices>>>>>>>>>>>>>>>>>",insdata)
        return insdata
    except Exception as e:
        raise ValueError("Could not fetch data")