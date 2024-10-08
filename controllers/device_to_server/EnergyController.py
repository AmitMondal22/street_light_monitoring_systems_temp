from db_model.MASTER_MODEL import insert_data,custom_select_sql_query,select_one_data
from utils.date_time_format import get_current_datetime,get_current_date,get_current_time,get_current_date_utc,get_current_time_utc
from fastapi import BackgroundTasks
from Library.DecimalEncoder import DecimalEncoder
from Library import AlertLibrary
import json
from models import device_data_model




async def get_energy_data(data:device_data_model.StreetLightDeviceData,client_id,device):
    try:
        print(";;;;;;;;;;;;;;;;;;;;;;;",data)
        # background_tasks = BackgroundTasks()
        device_data=select_one_data("md_device","device_id",f"client_id={client_id} AND device='{device}'")
        if device_data is None:
            raise ValueError("device not found")
        
        device_id=device_data["device_id"]
        current_datetime = get_current_datetime()
      
        # date_obj = datetime.strptime(data.DT, "%d%m%y")
        # formatted_date = date_obj.strftime("%Y-%m-%d")
        formatted_date = get_current_date()
        
        # time_obj = datetime.strptime(data.TIME, "%H%M%S")
        # formatted_time = time_obj.strftime("%H:%M:%S")
        formatted_time = get_current_time()
        
        
        columns = "client_id, device_id, device, tw, voltage, current, realpower, pf, kwh, runhr, frequency, domode, sensor_flag, upload_flag, date, time, created_at, updated_at"
        value = f"{client_id}, {device_id}, '{device}', {data.TW}, {data.VOLTAGE}, {data.CURRENT}, {data.REALPOWER}, {data.PF}, {data.KWH}, {data.RUNHR}, {data.FREQ}, {data.DOMODE}, {data.SENSORFLAG}, {data.UPLOADFLAG}, '{formatted_date}', '{formatted_time}', '{current_datetime}', '{current_datetime}'"
        
        print("value",value)
        energy_data_id = insert_data("td_energy_data", columns, value)
        
        
        if energy_data_id is None:
            raise ValueError("energy data was not inserted")
        else:
            await send_last_energy_data(client_id, device_id,device)
            user_data = {"energy_data_id":energy_data_id, "device_id": device_id, "device": device}
        return user_data
    except Exception as e:
        raise ValueError("Could not fetch data",e)
    
    

  
async def send_last_energy_data(client_id, device_id, device):
        try:
            print("////////////////HHHHHH")
            # Lazy import inside the function
            from Library.WsConnectionManagerManyDeviceTypes import WsConnectionManagerManyDeviceTypes
            manager = WsConnectionManagerManyDeviceTypes()
            background_tasks = BackgroundTasks()
            from routes.ws_routes import sennd_ws_message            
            custom_sql=f""" SELECT 
                                td.energy_data_id, 
                                td.client_id, 
                                td.device_id, 
                                td.device, 
                                td.tw, 
                                td.voltage,
                                td.current,
                                td.realpower,
                                td.pf,
                                td.kwh,
                                td.runhr,
                                td.frequency,
                                td.domode,
                                td.sensor_flag,
                                td.upload_flag,
                                td.date, 
                                td.time,
                                COALESCE((SELECT MAX(kwh) FROM td_energy_data WHERE DATE(date) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND device_id = td.device_id AND client_id = td.client_id AND device = td.device ORDER BY date DESC LIMIT 1), 0.0) AS kwh_yesterday,
                                COALESCE((SELECT MAX(kwh) FROM td_energy_data WHERE DATE(date) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND device_id = td.device_id AND client_id = td.client_id AND device = td.device ORDER BY date DESC LIMIT 1), 0.0) AS kwh_past_month,
                                COALESCE((SELECT MAX(kwh) FROM td_energy_data WHERE YEAR(date) = YEAR(CURDATE())-1 AND device_id = td.device_id AND client_id = td.client_id AND device = td.device), 0.0) AS kwh_past_year
                               
                            FROM 
                                td_energy_data td
                            WHERE 
                                td.device_id = {device_id}
                                AND td.device = '{device}'
                                AND td.client_id = {client_id}
                            ORDER BY 
                                td.energy_data_id DESC LIMIT 1"""
            lastdata=custom_select_sql_query(custom_sql,None)
            print(lastdata)
            # week_date=weekdays_date()
            
            try:
                custom_sql2=f"""SELECT 
                                curr.date,
                                curr.time,
                                curr.kwh
                            FROM 
                                (
                                    SELECT 
                                        *,
                                        LAG(kwh) OVER (ORDER BY date, time) AS prev_kwh,
                                        ROW_NUMBER() OVER (PARTITION BY date ORDER BY time DESC) AS rn
                                    FROM 
                                        td_energy_data
                                    WHERE 
                                        client_id = {client_id} 
                                        AND device_id = {device_id}
                                        AND device = '{device}'
                                        AND date BETWEEN DATE_SUB('{lastdata['date']}', INTERVAL (WEEKDAY('{lastdata['date']}') + 2) DAY) 
                                                    AND DATE_SUB('{lastdata['date']}', INTERVAL (WEEKDAY('{lastdata['date']}') - 6) DAY)
                                ) AS curr
                            WHERE 
                                curr.rn = 1
                            ORDER BY 
                                curr.date DESC;"""
                
                lastdata_weekdata=custom_select_sql_query(custom_sql2,1)
                print("Last data",lastdata_weekdata)

            except:
                lastdata_weekdata=None
            
            # background_tasks.add_task(AlertLibrary.send_alert, client_id, device_id, device, json.dumps(lastdata, cls=DecimalEncoder))
            
            # await AlertLibrary.send_alert(client_id, device_id, device, json.dumps(lastdata, cls=DecimalEncoder))
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>|||||||||||")
            
            # await manager.send_personal_message("SLMS",client_id, device_id, device, json.dumps(lastdata, cls=DecimalEncoder))
            twodata={"lastdata_weekdata":lastdata_weekdata,"lastdata":lastdata}
            # twodata={"lastdata":lastdata}
            print(twodata)
            await sennd_ws_message("SLMS",client_id, device_id, device, json.dumps(twodata, cls=DecimalEncoder))
            return json.dumps(lastdata, cls=DecimalEncoder)
        except Exception as e:
            raise ValueError("Could not fetch data",e)
    
    
