from db_model.MASTER_MODEL import select_data,update_data,select_one_data,batch_insert_data,insert_data
from utils.date_time_format import get_current_datetime, get_current_date_time_utc
from utils.last12month import last_12_month
from routes.mqtt_routes import subscribe_topics


@staticmethod
async def list_device(client_id):
    try:
        select="device_id, device,device_type,meter_type"
        # select="device_id, device,  model, lat, lon, imei_no, last_maintenance, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        condition=f"client_id={client_id} AND device_type='EN'"
        data = select_data("md_device", select, condition)
        return data
    except Exception as e:
        raise e
    
    
@staticmethod
async def user_device_list(client_id, user_id, organization_id):
    try:
        select="d.device_id, d.device, d.model, d.lat, d.lon, d.imei_no,d.device_type,d.meter_type, d.last_maintenance, DATE_FORMAT(d.created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(d.updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        
        condition = f"d.device_id = mud.device_id AND d.client_id = mud.client_id AND mud.client_id = {client_id} AND mud.user_id = {user_id} AND mud.organization_id = {organization_id} AND d.device_type='EN'"
        find_devices=select_data("md_device AS d, md_manage_user_device AS mud", select, condition,order_by="d.device_id ASC")
        print("find_devices>>>>>>>>>>>>>>>>>",find_devices)
        return find_devices
    except Exception as e:
        raise ValueError("Could not fetch data")


@staticmethod
async def device_info(params,userdata):
    try:
        condition = f"client_id={userdata['client_id']} AND device_id = {params.device_id} AND device_type='EN'"
        select="device_id, client_id, device, device_name, model, lat, lon, imei_no, last_maintenance,device_type,meter_type, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        data = select_one_data("md_device",select, condition,order_by="device_id DESC")
        
        select2="count(a.alert_id) alert, a.alert_type, a.unit_id,u.unit,u.unit_name"
        condition2 = f"a.unit_id=u.unit_id AND a.client_id={userdata['client_id']} AND a.device_id = {params.device_id} GROUP BY a.alert_type, a.unit_id, u.unit, u.unit_name"
        table2="td_alert AS a, md_unit AS u"
        alert=select_data(table2,select2, condition2)
        return {"data":data, "data2":alert}
    except Exception as e:
        raise e

@staticmethod
async def add_device(params):
    try:
        
        
        column="client_id, device, device_name, model, lat, lon, imei_no, device_type, meter_type, last_maintenance, created_at"
        
        rows_data = []
        for params_data in params:
            row_data = {
                "client_id": params_data.client_id,
                "device": params_data.device,
                "device_name": params_data.device_name,
                # "do_channel": params_data.
                "model": params_data.model,
                "lat": params_data.lat,
                "lon": params_data.lon,
                "imei_no": params_data.imei_no,
                "device_type": params_data.device_type,
                "meter_type": params_data.meter_type,
                "last_maintenance": params_data.last_maintenance,
                "created_at": get_current_datetime()  # Assuming get_current_datetime() returns the current datetime
            }
            rows_data.append(row_data)        
        batch_dataid=batch_insert_data("md_device", column, rows_data)
        print("batch_dataid---------------------", batch_dataid)
        
        
        await subscribe_topics()
        return batch_dataid
    except Exception as e:
        raise e
    
@staticmethod
async def edit_device(params):
    try:
        condition = f"device_id = {params.device_id} AND client_id = {params.client_id}"
        columns={"device":params.device, "device_name":params.device_name, "model":params.model, "lat":params.lat, "lon":params.lon, "imei_no":params.imei_no, "device_type" :params.device_type, "meter_type":params.meter_type, "updated_at":get_current_datetime()}
        data = update_data("md_device", columns, condition)
        print(data)
        return data
    except Exception as e:
        raise e
    

@staticmethod
async def manage_list_device(params):
    try:
        condition = f"a.client_id = {params.client_id} AND a.device_type='EN'"
        
        select="a.device_id, a.client_id, a.device, a.device_name, a.model, a.lat, a.lon, a.imei_no, a.device_type,a.meter_type,a.last_maintenance, DATE_FORMAT(a.created_at, '%Y-%m-%d') AS device_created_at,DATE_FORMAT(a.updated_at, '%Y-%m-%d %H:%i:%s') AS device_updated_at, b.energy_data_id, b.device_id AS b_device_id, b.voltage, b.current, b.realpower, b.pf, b.kwh, b.runhr, b.frequency, b.domode, b.sensor_flag, b.upload_flag,  DATE_FORMAT(b.date, '%Y-%m-%d') AS date, TIME_FORMAT(b.time, '%H:%i:%s') AS time, DATE_FORMAT(b.created_at, '%Y-%m-%d %H:%i:%s') AS energy_data_created_at, DATE_FORMAT(b.updated_at, '%Y-%m-%d %H:%i:%s') AS energy_data_updated_at"
        
        table="""md_device a LEFT JOIN (SELECT t1.*
    FROM td_energy_data t1
    INNER JOIN (
        SELECT device_id, MAX(CONCAT(date, ' ', time)) AS max_datetime
        FROM td_energy_data
        GROUP BY device_id
    ) t2 ON t1.device_id = t2.device_id AND CONCAT(t1.date, ' ', t1.time) = t2.max_datetime) b ON a.device_id = b.device_id AND a.client_id = b.client_id"""
        
        order_by="a.device_id ASC"
        data = select_data(table, select,condition,order_by)
        print("????????????????>>>>>>>>>>>>>>>>",data)
        return data
    except Exception as e:
        raise e
    



    
# =========================================================
@staticmethod
async def energy_used(params,user_data):
    try:
        if params.type=="Y" :
            condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
            select="ed.energy_data_id, ed.device_id, ed.e1, ed.e2, ed.e3, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time "
            table =f"td_energy_data AS ed INNER JOIN (SELECT  MAX(energy_data_id) AS max_energy_data_id,  YEAR(date) AS year, MONTH(date) AS month FROM td_energy_data WHERE client_id = {user_data['client_id']} AND device_id = {params.device_id} GROUP BY  YEAR(date), MONTH(date) ) AS sub_ed ON ed.energy_data_id = sub_ed.max_energy_data_id"
            data = select_data(table,select, condition,order_by="ed.date DESC, ed.time DESC")
        elif params.type =="M":
            condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
            select="ed.energy_data_id, ed.device_id, ed.e1, ed.e2, ed.e3, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time"
            table=f"""td_energy_data AS ed
                            INNER JOIN (
                                SELECT
                                    date,
                                    MAX(time) AS max_time
                                FROM
                                    td_energy_data
                                WHERE
                                    client_id = {user_data['client_id']} AND device_id = {params.device_id}
                                    AND date BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE()
                                GROUP BY
                                    date
                            ) AS sub_ed ON ed.date = sub_ed.date AND ed.time = sub_ed.max_time"""
            data = select_data(table,select, condition,order_by="date DESC, time DESC")
        elif params.type =="D":
            condition = f"client_id = {user_data['client_id']} AND device_id = {params.device_id} AND date = CURDATE() AND (date, time) IN ( SELECT date, MAX(time) FROM td_energy_data WHERE date = CURDATE() GROUP BY date, HOUR(time))"
            select = "energy_data_id, device_id, e1, e2, e3, DATE_FORMAT(date, '%Y-%m-%d') AS date, TIME_FORMAT(time, '%H:%i:%s') AS time"
            data = select_data("td_energy_data AS ed",select, condition,order_by="date DESC, time DESC")
        else:
            return "Invalid type"
        return data
    except Exception as e:
        raise e
    
@staticmethod
async def voltage_data(params,user_data):
    try:
        if params.type=="Y" :
                condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
                select="ed.energy_data_id, ed.device_id, ed.r, ed.y, ed.b, ed.r_y, ed.y_b, ed.b_r, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time "
                table =f"td_energy_data AS ed INNER JOIN (SELECT  MAX(energy_data_id) AS max_energy_data_id,  YEAR(date) AS year, MONTH(date) AS month FROM td_energy_data WHERE client_id = {user_data['client_id']} AND device_id = {params.device_id} GROUP BY  YEAR(date), MONTH(date) ) AS sub_ed ON ed.energy_data_id = sub_ed.max_energy_data_id"
                data = select_data(table,select, condition,order_by="ed.date DESC, ed.time DESC")
        elif params.type =="M":
            condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
            select="ed.energy_data_id, ed.device_id, ed.r, ed.y, ed.b, ed.r_y, ed.y_b, ed.b_r, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time"
            table=f"""td_energy_data AS ed
                            INNER JOIN (
                                SELECT
                                    date,
                                    MAX(time) AS max_time
                                FROM
                                    td_energy_data
                                WHERE
                                    client_id = {user_data['client_id']} AND device_id = {params.device_id}
                                    AND date BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE()
                                GROUP BY
                                    date
                            ) AS sub_ed ON ed.date = sub_ed.date AND ed.time = sub_ed.max_time"""
            data = select_data(table,select, condition,order_by="date DESC, time DESC")
        elif params.type =="D":
            condition = f"client_id = {user_data['client_id']} AND device_id = {params.device_id} AND date = CURDATE() AND (date, time) IN ( SELECT date, MAX(time) FROM td_energy_data WHERE date = CURDATE() GROUP BY date, HOUR(time))"
            select = "energy_data_id, device_id, ed.r, ed.y, ed.b, ed.r_y, ed.y_b, ed.b_r, DATE_FORMAT(date, '%Y-%m-%d') AS date, TIME_FORMAT(time, '%H:%i:%s') AS time"
            data = select_data("td_energy_data AS ed",select, condition,order_by="date DESC, time DESC")
        else:
            return "Invalid type"
        return data
    except Exception as e:
        raise e

@staticmethod
async def current_data(params,user_data):
    try:
        # end_date_time=params.end_date_time
        # start_date_time=params.start_date_time
        
        # condition = f"client_id = {user_data['client_id']} AND device_id = {params.device_id} AND created_at BETWEEN '{start_date_time.strftime('%Y-%m-%d %H:%M:%S')}' AND '{end_date_time.strftime('%Y-%m-%d %H:%M:%S')}'"
        # select="energy_data_id, device_id,  curr1, curr2, curr3, DATE_FORMAT(date, '%Y-%m-%d') AS date, TIME_FORMAT(time, '%H:%i:%s') AS time, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        # data = select_data("td_energy_data",select, condition,order_by="energy_data_id DESC")
        # return data
        if params.type=="Y" :
                condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
                select="ed.energy_data_id, ed.device_id, ed.curr1, ed.curr2, ed.curr3, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time "
                table =f"td_energy_data AS ed INNER JOIN (SELECT  MAX(energy_data_id) AS max_energy_data_id,  YEAR(date) AS year, MONTH(date) AS month FROM td_energy_data WHERE client_id = {user_data['client_id']} AND device_id = {params.device_id} GROUP BY  YEAR(date), MONTH(date) ) AS sub_ed ON ed.energy_data_id = sub_ed.max_energy_data_id"
                data = select_data(table,select, condition,order_by="ed.date DESC, ed.time DESC")
        elif params.type =="M":
            condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
            select="ed.energy_data_id, ed.device_id, ed.curr1, ed.curr2, ed.curr3, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time"
            table=f"""td_energy_data AS ed
                            INNER JOIN (
                                SELECT
                                    date,
                                    MAX(time) AS max_time
                                FROM
                                    td_energy_data
                                WHERE
                                    client_id = {user_data['client_id']} AND device_id = {params.device_id}
                                    AND date BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE()
                                GROUP BY
                                    date
                            ) AS sub_ed ON ed.date = sub_ed.date AND ed.time = sub_ed.max_time"""
            data = select_data(table,select, condition,order_by="date DESC, time DESC")
        elif params.type =="D":
            condition = f"client_id = {user_data['client_id']} AND device_id = {params.device_id} AND date = CURDATE() AND (date, time) IN ( SELECT date, MAX(time) FROM td_energy_data WHERE date = CURDATE() GROUP BY date, HOUR(time))"
            select = "energy_data_id, device_id,  ed.curr1, ed.curr2, ed.curr3, DATE_FORMAT(date, '%Y-%m-%d') AS date, TIME_FORMAT(time, '%H:%i:%s') AS time"
            data = select_data("td_energy_data AS ed",select, condition,order_by="date DESC, time DESC")
        else:
            return "Invalid type"
        return data
    except Exception as e:
        raise e
    
    
@staticmethod
async def power_data(params,user_data):
    try:
        # end_date_time=params.end_date_time
        # start_date_time=params.start_date_time
    
        # condition = f"client_id = {user_data['client_id']} AND device_id = {params.device_id} AND created_at BETWEEN '{start_date_time.strftime('%Y-%m-%d %H:%M:%S')}' AND '{end_date_time.strftime('%Y-%m-%d %H:%M:%S')}'"
        # select="energy_data_id, device_id,  activep1, activep2, activep3, apparentp1, apparentp2, apparentp3, pf1, pf2, pf3, DATE_FORMAT(date, '%Y-%m-%d') AS date, TIME_FORMAT(time, '%H:%i:%s') AS time, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        # data = select_data("td_energy_data",select, condition,order_by="energy_data_id DESC")
        # return data
    
        if params.type=="Y" :
                condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
                select="ed.energy_data_id, ed.device_id, ed.activep1, ed.activep2, ed.activep3, ed.apparentp1, ed.apparentp2, ed.apparentp3, ed.pf1, ed.pf2, ed.pf3, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time "
                table =f"td_energy_data AS ed INNER JOIN (SELECT  MAX(energy_data_id) AS max_energy_data_id,  YEAR(date) AS year, MONTH(date) AS month FROM td_energy_data WHERE client_id = {user_data['client_id']} AND device_id = {params.device_id} GROUP BY  YEAR(date), MONTH(date) ) AS sub_ed ON ed.energy_data_id = sub_ed.max_energy_data_id"
                data = select_data(table,select, condition,order_by="ed.date DESC, ed.time DESC")
        elif params.type =="M":
            condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
            select="ed.energy_data_id, ed.device_id, ed.activep1, ed.activep2, ed.activep3, ed.apparentp1, ed.apparentp2, ed.apparentp3, ed.pf1, ed.pf2, ed.pf3, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time"
            table=f"""td_energy_data AS ed
                            INNER JOIN (
                                SELECT
                                    date,
                                    MAX(time) AS max_time
                                FROM
                                    td_energy_data
                                WHERE
                                    client_id = {user_data['client_id']} AND device_id = {params.device_id}
                                    AND date BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE()
                                GROUP BY
                                    date
                            ) AS sub_ed ON ed.date = sub_ed.date AND ed.time = sub_ed.max_time"""
            data = select_data(table,select, condition,order_by="date DESC, time DESC")
        elif params.type =="D":
            condition = f"client_id = {user_data['client_id']} AND device_id = {params.device_id} AND date = CURDATE() AND (date, time) IN ( SELECT date, MAX(time) FROM td_energy_data WHERE date = CURDATE() GROUP BY date, HOUR(time))"
            select = "energy_data_id, device_id,  ed.activep1, ed.activep2, ed.activep3, ed.apparentp1, ed.apparentp2, ed.apparentp3, ed.pf1, ed.pf2, ed.pf3, DATE_FORMAT(date, '%Y-%m-%d') AS date, TIME_FORMAT(time, '%H:%i:%s') AS time"
            data = select_data("td_energy_data AS ed",select, condition,order_by="date DESC, time DESC")
        else:
            return "Invalid type"
        return data
    except Exception as e:
        raise e
    
@staticmethod
async def total_power_analisis(params,user_data):
    try:
        # end_date_time=params.end_date_time
        # start_date_time=params.start_date_time
        # condition = f"client_id = {user_data['client_id']} AND device_id = {params.device_id} AND created_at BETWEEN '{start_date_time.strftime('%Y-%m-%d %H:%M:%S')}' AND '{end_date_time.strftime('%Y-%m-%d %H:%M:%S')}'"
        # select="energy_data_id, device_id,  totkw, totkva, totkvar, runhr, DATE_FORMAT(date, '%Y-%m-%d') AS date, TIME_FORMAT(time, '%H:%i:%s') AS time, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at, DATE_FORMAT(updated_at, '%Y-%m-%d %H:%i:%s') AS updated_at"
        # data = select_data("td_energy_data",select, condition,order_by="energy_data_id DESC")
        # return data
    
    
    
        if params.type=="Y" :
                condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
                select="ed.energy_data_id, ed.device_id,ed.totkw, ed.totkva, ed.totkvar, ed.runhr, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time "
                table =f"td_energy_data AS ed INNER JOIN (SELECT  MAX(energy_data_id) AS max_energy_data_id,  YEAR(date) AS year, MONTH(date) AS month FROM td_energy_data WHERE client_id = {user_data['client_id']} AND device_id = {params.device_id} GROUP BY  YEAR(date), MONTH(date) ) AS sub_ed ON ed.energy_data_id = sub_ed.max_energy_data_id"
                data = select_data(table,select, condition,order_by="ed.date DESC, ed.time DESC")
        elif params.type =="M":
            condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
            select="ed.energy_data_id, ed.device_id,ed.totkw, ed.totkva, ed.totkvar, ed.runhr, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time"
            table=f"""td_energy_data AS ed
                            INNER JOIN (
                                SELECT
                                    date,
                                    MAX(time) AS max_time
                                FROM
                                    td_energy_data
                                WHERE
                                    client_id = {user_data['client_id']} AND device_id = {params.device_id}
                                    AND date BETWEEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND CURDATE()
                                GROUP BY
                                    date
                            ) AS sub_ed ON ed.date = sub_ed.date AND ed.time = sub_ed.max_time"""
            data = select_data(table,select, condition,order_by="date DESC, time DESC")
        elif params.type =="D":
            condition = f"client_id = {user_data['client_id']} AND device_id = {params.device_id} AND date = CURDATE() AND (date, time) IN ( SELECT date, MAX(time) FROM td_energy_data WHERE date = CURDATE() GROUP BY date, HOUR(time))"
            select = "energy_data_id, device_id, ed.totkw, ed.totkva, ed.totkvar, ed.runhr, DATE_FORMAT(date, '%Y-%m-%d') AS date, TIME_FORMAT(time, '%H:%i:%s') AS time"
            data = select_data("td_energy_data AS ed",select, condition,order_by="date DESC, time DESC")
        else:
            return "Invalid type"
        return data
    
    except Exception as e:
        raise e
    


@staticmethod
async def organization_settings(client_id,user_id,params):
    try:

        
        #  column="client_id, device, device_name,  model, lat, lon, imei_no, device_type, meter_type, last_maintenance, created_at"
        
        # rows_data = []
        # for params_data in params:
        #     row_data = {
        #         "client_id": params_data.client_id,
        #         "device": params_data.device,
        #         "device_name": params_data.device_name,
        #         "do_channel": params_data.
        #         "model": params_data.model,
        #         "lat": params_data.lat,
        #         "lon": params_data.lon,
        #         "imei_no": params_data.imei_no,
        #         "device_type": params_data.device_type,
        #         "meter_type": params_data.meter_type,
        #         "last_maintenance": params_data.last_maintenance,
        #         "created_at": get_current_datetime()  # Assuming get_current_datetime() returns the current datetime
        #     }
        #     rows_data.append(row_data)        
        # batch_dataid=batch_insert_data("md_device", column, rows_data)
        # print("batch_dataid---------------------", batch_dataid)
        # return batch_dataid

        
        rows_data = []
        for params_data in params.billing_data:
            row_data = {
                "client_id":params.client_id,
                "organization_id":params.organization_id,
                "billing_type":params_data.billing_type,
                "billing_price":params_data.billing_price,
                "billing_status":"Y",
                "billing_day":params_data.billing_day,
                "created_by":user_id,
                "created_at":get_current_datetime()
            }
            rows_data.append(row_data)
        column="client_id, organization_id, billing_type, billing_price, billing_status, billing_day, created_by, created_at"
        batch_dataid=batch_insert_data("md_billing_organization", column, rows_data)
        
        
        columndata="organization_id, client_id, countries_id, states_id, regions_id, subregions_id, cities_id, address, create_by, created_at"
        insdata=f"{params.organization_id}, {params.client_id}, {params.countries_id}, {params.states_id}, {params.regions_id}, {params.subregions_id}, {params.cities_id}, '{params.address}', {user_id}, '{get_current_datetime()}'"
        st_view_organization=insert_data("st_ms_organization",columndata,insdata)
    
    
        res={"billing_data":batch_dataid,"settings_organization":st_view_organization}
        return res
    except Exception as e:
        raise e
    
@staticmethod
async def organization_settings_list(client_id,user_id,params):
    try:
        condition = f"""st_org.client_id = sb_org.client_id 
                        AND st_org.organization_id = sb_org.organization_id 
                        AND st_org.cities_id = mlc.id
                        AND st_org.states_id = mls.id
                        AND st_org.countries_id = mlco.id
                        AND st_org.regions_id = mlr.id
                        AND st_org.subregions_id = mlsr.id
                        AND st_org.client_id = {client_id} 
                        AND sb_org.client_id = {client_id}  AND st_org.organization_id = {params.organization_id} AND sb_org.organization_id = {params.organization_id} AND sb_org.billing_status ='Y'"""
        
        select="st_org.id_ms_organization,st_org.organization_id, st_org.client_id, st_org.countries_id, st_org.states_id, st_org.regions_id, st_org.subregions_id, st_org.cities_id, st_org.address, DATE_FORMAT(st_org.created_at, '%Y-%m-%d %H:%i:%s') AS created_at, sb_org.billing_organization, sb_org.billing_type, sb_org.billing_price, sb_org.billing_status, sb_org.billing_day, DATE_FORMAT(sb_org.created_at, '%Y-%m-%d %H:%i:%s') AS billing_created_at, mlc.name AS cityes, mls.name AS state, mlco.name AS countries, mlr.name AS subregions, mlsr.name AS regions"
        
        table="st_ms_organization AS st_org, md_billing_organization AS sb_org, md_lo_cities AS mlc, md_lo_states AS mls, md_lo_countries AS mlco, md_lo_regions AS mlr, md_lo_subregions AS mlsr"
        data = select_data(table,select, condition)
        return data
    except Exception as e:
        raise e
    
@staticmethod
async def old_bill_list(client_id, user_id, params):
    try:
        condition = f"client_id = {client_id} AND organization_id = {params.organization_id}"
        # condition = f"client_id = {client_id} AND organization_id = {params.organization_id} AND billing_status = 'N'"
        select = "billing_organization, organization_id, client_id, billing_type, billing_price, billing_status, billing_day, created_at"
        table = "md_billing_organization"
        data = select_data(table, select, condition,order_by="billing_organization DESC")
        return data
    except Exception as e:
        raise e
    
@staticmethod
async def add_bill(client_id, user_id, params):
    try:
        update_condition=f"client_id = {client_id} AND organization_id = {params.organization_id} AND billing_status = 'Y'"
        set_values={"billing_status":"N"}
        update_bill=update_data("md_billing_organization",set_values,update_condition)
        columndata="client_id, organization_id, billing_type, billing_price, billing_status, billing_day, created_by, created_at"
        insdata=f"{client_id},{params.organization_id},'{params.billing_type}',{params.billing_price},'Y',{params.billing_day},{user_id},'{get_current_datetime()}'"
        add_billing=insert_data("md_billing_organization",columndata,insdata)
        return add_billing
    except Exception as e:
        raise e
    
@staticmethod
async def edit_organization_info(client_id,user_id,params):
    try:
        update_condition=f"client_id = {client_id} AND organization_id = {params.organization_id}"
        set_values={"countries_id":params.countries_id,"states_id":params.states_id,"regions_id":params.regions_id,"subregions_id":params.subregions_id,"cities_id":params.cities_id,"address":params.address,"create_by":user_id}
        edit_organization=update_data("st_ms_organization",set_values,update_condition)
        return edit_organization
    except Exception as e:
        raise e
@staticmethod
async def get_device_schedule(userdata,params):
    try:
        condition = f"client_id = {userdata['client_id']} AND device_id = {params.device_id}"
        select = "device_scheduling_id, device_id, device, client_id, device_type, relay_close_time, timer_start_hours, timer_start_minutes, timer_stop_hours_1, timer_stop_minutes_1, create_by, created_at, updated_at"
        table = "st_device_scheduling"
        data = select_one_data(table, select, condition,order_by="device_scheduling_id DESC")
        return data
    except Exception as e:
        raise e
    