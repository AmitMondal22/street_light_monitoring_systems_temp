from db_model.MASTER_MODEL import insert_data,custom_select_sql_query,select_one_data
from utils.date_time_format import get_current_datetime,get_current_date,get_current_time
from fastapi import BackgroundTasks
from Library.DecimalEncoder import DecimalEncoder
from Library import AlertLibrary
import json
from models import device_data_model
# from utils.week_date import weekdays_date
from datetime import datetime



@staticmethod
async def get_energy_data(data:device_data_model.EnergyDeviceData,client_id,device):
    try:
        background_tasks = BackgroundTasks()
        device_data=select_one_data("md_device","device_id",f"client_id={client_id} AND device='{device}'")
        if device_data is None:
            raise ValueError("device not found")
        
        device_id=device_data["device_id"]
        current_datetime = get_current_datetime()
      
        date_obj = datetime.strptime(data.DT, "%d%m%y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        
        time_obj = datetime.strptime(data.TIME, "%H%M%S")
        formatted_time = time_obj.strftime("%H:%M:%S")
        
        
        columns = "client_id, device_id, device, do_channel,tw,e1, e2, e3, r, y, b, r_y, y_b, b_r, curr1, curr2, curr3, activep1, activep2, activep3, apparentp1, apparentp2, apparentp3, pf1, pf2, pf3, freq, reactvp1, reactvp2, reactvp3, avaragevln, avaragevll, avaragecurrent, totkw, totkva, totkvar, runhr, date, time, created_at"
        # value = f"{client_id}, {device_id}, '{device}', {data.CH}, {data.KWH1}, {data.KWH2}, {data.KWH3}, {data.R}, {data.Y}, {data.B}, {data.R_Y}, {data.Y_B}, {data.B_R}, {data.curr1}, {data.curr2}, {data.curr3}, {data.activep1}, {data.activep2}, {data.activep3}, {data.apparentp1}, {data.apparentp2}, {data.apparentp3}, {data.pf1}, {data.pf2}, {data.pf3}, {data.freq}, {data.reactvp1}, {data.reactvp2}, {data.reactvp3}, {data.avaragevln}, {data.avaragevll}, {data.avaragecurrent}, {data.totkw}, {data.totkva}, {data.totkvar}, {data.runhr}, '{get_current_date()}', '{get_current_time()}', '{current_datetime}'"

        value = f"{client_id}, {device_id}, '{device}', {data.CH},{data.TW}, {data.KWH1}, {data.KWH2}, {data.KWH3}, {data.R}, {data.Y}, {data.B}, {data.R_Y}, {data.Y_B}, {data.B_R}, {data.AMP1}, {data.AMP2}, {data.AMP3}, {data.KW1}, {data.KW2}, {data.KW3}, {data.KVA1}, {data.KVA2}, {data.KVA3}, {data.PF1}, {data.PF2}, {data.PF3}, {data.FREQ}, {data.KVAR1}, {data.KVAR2}, {data.KVAR3}, {data.AVGVLN}, {data.AVGVLL}, {data.AVGAMP}, {data.TOTKW}, {data.TOTKVA}, {data.TOTKVAR}, {data.RUNHR}, '{formatted_date}', '{formatted_time}', '{current_datetime}'"
        
        print("value",value)
        energy_data_id = insert_data("td_energy_data", columns, value)
        
        
        
        # mqtt_client = MqttLibraryClass("techavoiot.co.in", 1883)
        # # Connect to the MQTT broker
        # mqtt_client.connect()
        
        # data=await update_topics()
        # print("data",data)
        # mqtt_client.subscribe(data)
        
        
        
        
        if energy_data_id is None:
            raise ValueError("energy data was not inserted")
        else:
            # from routes.api_client_routes import SendEnergySocket
            # lastdata=await SendEnergySocket.send_last_energy_data(data.client_id, device_id, data.device)
            # lastdata=await send_last_energy_data(client_id, device_id,device)
            await send_last_energy_data(client_id, device_id,device)
            # background_tasks.add_task(send_last_energy_data, client_id, device_id,device)
            # if lastdata is None:
            #     raise ValueError("Could not fetch data")
            user_data = {"energy_data_id":energy_data_id, "device_id": device_id, "device": device, "do_channel": data.CH}
        return user_data
    except Exception as e:
        raise ValueError("Could not fetch data",e)
    
    

@staticmethod  
async def send_last_energy_data(client_id, device_id, device):
        try:
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
                                td.do_channel, 
                                td.tw, 
                                td.e1, 
                                td.e2, 
                                td.e3, 
                                td.r, 
                                td.y, 
                                td.b, 
                                td.r_y, 
                                td.y_b, 
                                td.b_r, 
                                td.curr1, 
                                td.curr2, 
                                td.curr3, 
                                td.activep1, 
                                td.activep2, 
                                td.activep3, 
                                td.apparentp1, 
                                td.apparentp2, 
                                td.apparentp3, 
                                td.pf1, 
                                td.pf2, 
                                td.pf3, 
                                td.freq, 
                                td.reactvp1, 
                                td.reactvp2, 
                                td.reactvp3, 
                                td.avaragevln, 
                                td.avaragevll, 
                                td.avaragecurrent, 
                                td.totkw, 
                                td.totkva, 
                                td.totkvar, 
                                td.runhr, 
                                td.date, 
                                td.time, 
                                COALESCE((SELECT MAX(e1) FROM td_energy_data WHERE DATE(date) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND device_id = td.device_id AND client_id = td.client_id AND device = td.device ORDER BY date DESC LIMIT 1), 0.0) AS e1_yesterday,
    COALESCE((SELECT MAX(e2) FROM td_energy_data WHERE DATE(date) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND device_id = td.device_id AND client_id = td.client_id AND device = td.device ORDER BY date DESC LIMIT 1), 0.0) AS e2_yesterday,
    COALESCE((SELECT MAX(e3) FROM td_energy_data WHERE DATE(date) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND device_id = td.device_id AND client_id = td.client_id AND device = td.device ORDER BY date DESC LIMIT 1), 0.0) AS e3_yesterday,
    COALESCE((SELECT MAX(e1) FROM td_energy_data WHERE DATE(date) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND device_id = td.device_id AND client_id = td.client_id AND device = td.device ORDER BY date DESC LIMIT 1), 0.0) AS e1_past_month,
    COALESCE((SELECT MAX(e2) FROM td_energy_data WHERE DATE(date) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND device_id = td.device_id AND client_id = td.client_id AND device = td.device ORDER BY date DESC LIMIT 1), 0.0) AS e2_past_month,
    COALESCE((SELECT MAX(e3) FROM td_energy_data WHERE DATE(date) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND device_id = td.device_id AND client_id = td.client_id AND device = td.device ORDER BY date DESC LIMIT 1), 0.0) AS e3_past_month,
    COALESCE((SELECT MAX(e1) FROM td_energy_data WHERE YEAR(date) = YEAR(CURDATE())-1 AND device_id = td.device_id AND client_id = td.client_id AND device = td.device), 0.0) AS e1_past_year,
    COALESCE((SELECT MAX(e2) FROM td_energy_data WHERE YEAR(date) = YEAR(CURDATE())-1 AND device_id = td.device_id AND client_id = td.client_id AND device = td.device), 0.0) AS e2_past_year,
    COALESCE((SELECT MAX(e3) FROM td_energy_data WHERE YEAR(date) = YEAR(CURDATE())-1 AND device_id = td.device_id AND client_id = td.client_id AND device = td.device), 0.0) AS e3_past_year
                            FROM 
                                td_energy_data td
                            WHERE 
                                td.device_id = {device_id}
                                AND td.device = '{device}'
                                AND td.client_id = {client_id}
                            ORDER BY 
                                td.energy_data_id DESC LIMIT 1"""
            lastdata=custom_select_sql_query(custom_sql,None)
            
            
            # week_date=weekdays_date()
            
            
            custom_sql2=f""" SELECT 
                                curr.energy_data_id,
                                curr.client_id,
                                curr.device_id,
                                curr.device,
                                curr.do_channel,
                                curr.tw,
                                curr.e1 - COALESCE(curr.prev_e1, 0) AS e1_diff,
                                curr.e2 - COALESCE(curr.prev_e2, 0) AS e2_diff,
                                curr.e3 - COALESCE(curr.prev_e3, 0) AS e3_diff,
                                curr.date,
                                curr.time
                            FROM 
                                (
                                    SELECT 
                                        *,
                                        LAG(e1) OVER (ORDER BY date, time) AS prev_e1,
                                        LAG(e2) OVER (ORDER BY date, time) AS prev_e2,
                                        LAG(e3) OVER (ORDER BY date, time) AS prev_e3,
                                        ROW_NUMBER() OVER (PARTITION BY date ORDER BY time DESC) AS rn
                                    FROM 
                                        td_energy_data
                                    WHERE 
                                        client_id = {client_id} 
                                        AND device_id = {device_id}
                                        AND device = '{device}'
                                        AND date BETWEEN DATE_SUB(CURDATE(), INTERVAL (WEEKDAY(CURDATE()) + 2) DAY) 
                                                    AND DATE_SUB(CURDATE(), INTERVAL (WEEKDAY(CURDATE()) - 6) DAY)
                                ) AS curr
                            WHERE 
                                curr.rn = 1
                            ORDER BY 
                                curr.date DESC; """
            
            lastdata_weekdata=custom_select_sql_query(custom_sql2,1)
            print("Last data",lastdata_weekdata)
            background_tasks.add_task(AlertLibrary.send_alert, client_id, device_id, device, json.dumps(lastdata, cls=DecimalEncoder))
            
            # await AlertLibrary.send_alert(client_id, device_id, device, json.dumps(lastdata, cls=DecimalEncoder))
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            
            # await manager.send_personal_message("SLMS",client_id, device_id, device, json.dumps(lastdata, cls=DecimalEncoder))
            twodata={"lastdata_weekdata":lastdata_weekdata,"lastdata":lastdata}
            print(twodata)
            await sennd_ws_message("SLMS",client_id, device_id, device, json.dumps(twodata, cls=DecimalEncoder))
            return json.dumps(lastdata, cls=DecimalEncoder)
        except Exception as e:
            raise ValueError("Could not fetch data",e)
    
    
