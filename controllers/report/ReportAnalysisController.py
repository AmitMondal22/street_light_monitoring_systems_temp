from db_model.MASTER_MODEL import insert_data,custom_select_sql_query,select_one_data,select_data
from utils.first_day_last_day import first_day_last_day,first_year_day_last_year_day
# from Library.DecimalEncoder import DecimalEncoder
# import json

@staticmethod
async def energy_usage_billing(user_data,params):
    try:
        if user_data['user_type'] == "C":
            if params.report_type == "M": # monthly
                fdatetdate=first_day_last_day(params.start_date_time)
                print("??????????????-----------------???????",fdatetdate["first_day"])
                condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
                select="ed.e1,ed.e2,ed.e3,ed.energy_data_id, ed.device_id, ed.do_channel, ed.activep1, ed.activep2, ed.activep3, ed.apparentp1, ed.apparentp2, ed.apparentp3, ed.pf1, ed.pf2, ed.pf3, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time"
                table=f"""td_energy_data AS ed
                                INNER JOIN (
                                    SELECT
                                        date,
                                        MAX(time) AS max_time
                                    FROM
                                        td_energy_data
                                    WHERE
                                        client_id = {user_data['client_id']} AND device_id = {params.device_id}
                                        AND date BETWEEN '{fdatetdate["first_day"]}' AND '{fdatetdate["last_day"]}'
                                    GROUP BY
                                        date
                                ) AS sub_ed ON ed.date = sub_ed.date AND ed.time = sub_ed.max_time"""
                data = select_data(table,select, condition,order_by="ed.date ASC, ed.time ASC")
                # data = select_data(table,select, condition,order_by="ed.date ASC, ed.time ASC")
                # if params.end_date_time == None:
                    #     condition=f"a.client_id={user_data['client_id']} AND a.device_id={params.device_id} AND a.date BETWEEN '{params.start_date_time}' AND '{params.start_date_time}'"
                    # condition=f"a.client_id={user_data['client_id']} AND a.device_id={params.device_id} AND a.date BETWEEN '{params.start_date_time}' AND '{params.end_date_time}'"
            elif params.report_type == "Y":  #yearly
                fdatetdate=first_year_day_last_year_day(params.start_date_time)
                condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
                select=f""" ed.energy_data_id,
                            ed.device_id,
                            ed.do_channel,
                            ed .e1,
                            ed .e2,
                            ed .e3,
                            DATE_FORMAT(ed.date, '%Y-%m-%d') AS date,
                            TIME_FORMAT(ed.time, '%H:%i:%s') AS time"""
                            
                table =f""" td_energy_data AS ed
                                INNER JOIN(
                                    SELECT
                                        MAX(energy_data_id) AS max_energy_data_id,
                                        YEAR(DATE) AS YEAR,
                                        MONTH(DATE) AS MONTH
                                    FROM
                                        td_energy_data
                                    WHERE
                                        client_id = 1 AND device_id = 1
                                        AND date BETWEEN '{fdatetdate["first_day"]}' AND '{fdatetdate["last_day"]}'
                                    GROUP BY
                                        YEAR(DATE),
                                        MONTH(DATE)
                                ) AS sub_ed
                                ON
                                ed.energy_data_id = sub_ed.max_energy_data_id """
                data = select_data(table,select, condition,order_by="ed.date ASC, ed.time ASC")
            elif params.report_type == "C": # customized
                condition = f"ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}"
                select="ed.e1,ed.e2,ed.e3,ed.energy_data_id, ed.device_id, ed.do_channel, ed.activep1, ed.activep2, ed.activep3, ed.apparentp1, ed.apparentp2, ed.apparentp3, ed.pf1, ed.pf2, ed.pf3, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time"
                table=f"""td_energy_data AS ed
                                INNER JOIN (
                                    SELECT
                                        date,
                                        MAX(time) AS max_time
                                    FROM
                                        td_energy_data
                                    WHERE
                                        client_id = {user_data['client_id']} AND device_id = {params.device_id}
                                        AND date BETWEEN '{params.start_date_time}' AND '{params.end_date_time}'
                                    GROUP BY
                                        date
                                ) AS sub_ed ON ed.date = sub_ed.date AND ed.time = sub_ed.max_time"""
                data = select_data(table,select, condition,order_by="ed.date ASC, ed.time ASC")
        elif user_data['user_type'] == "U" or user_data['user_type'] == "O":
          print("fxgbxd")
          
        condition_bill = f"a.organization_id=b.organization_id AND c.organization_id=a.organization_id AND c.countries_id=d.id AND a.client_id = {user_data['client_id']} AND b.client_id={user_data['client_id']} AND a.device_id = {params.device_id}"
        select_bill = "b.*,d.*"
        master_bill = select_one_data("md_manage_user_device AS a,md_billing_organization AS b,st_ms_organization AS c,md_lo_countries AS d",select_bill, condition_bill)
        return {"data":data , "master_bill":master_bill}
    except Exception as e:
        return ValueError("Error in energy_usage_billing",e)
    
    


@staticmethod
async def new_energy_usage_billing(user_data,params):
    try:
        if (user_data['user_type'] == "C") or (user_data['user_type'] == "U" or user_data['user_type'] == "O"):
            if params.report_type == "M": # monthly
                fdatetdate=first_day_last_day(params.start_date_time)
                condition = f"""ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id} AND COALESCE(
                                    a.billing_price,
                                    (
                                        SELECT
                                            a2.billing_price
                                        FROM
                                            md_billing_organization AS a2
                                        WHERE
                                            a2.created_at < ed.date
                                        ORDER BY
                                            a2.created_at DESC
                                        LIMIT 1
                                    )
                                ) IS NOT NULL"""
                select=f"""ed.e1,ed.e2,ed.e3,ed.energy_data_id, ed.device_id, ed.do_channel, ed.activep1, ed.activep2, ed.activep3, ed.apparentp1, ed.apparentp2, ed.apparentp3, ed.pf1, ed.pf2, ed.pf3, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time,
                
                
                
                COALESCE(
                    a.billing_price, 
                    (
                        SELECT a2.billing_price 
                        FROM md_billing_organization AS a2 
                        WHERE DATE(a2.created_at) < DATE(ed.date) 
                        ORDER BY DATE(a2.created_at) DESC 
                        LIMIT 1
                    )
                ) AS billing_price
                
                
                
                """
                table=f"""td_energy_data AS ed
                                INNER JOIN (
                                    SELECT
                                        date,
                                        MAX(time) AS max_time
                                    FROM
                                        td_energy_data
                                    WHERE
                                        client_id = {user_data['client_id']} AND device_id = {params.device_id}
                                        AND date BETWEEN '{fdatetdate["first_day"]}' AND '{fdatetdate["last_day"]}'
                                    GROUP BY
                                        date
                                ) AS sub_ed ON ed.date = sub_ed.date AND ed.time = sub_ed.max_time
                                
                                LEFT JOIN 
                                    md_billing_organization AS a ON DATE(ed.date) = DATE(a.created_at)
                                
                                
                                """
                data = select_data(table,select, condition,order_by="ed.date ASC, ed.time ASC")
                
                
                
                condition2=f"""client_id = {user_data['client_id']} AND device_id = {params.device_id} AND date < '{fdatetdate["first_day"]}' """
                
                end_date_last_row=select_one_data("td_energy_data","e1,e2,e3,date,time", condition2, order_by="date DESC, time DESC")
                # data = select_data(table,select, condition,order_by="ed.date ASC, ed.time ASC")
                # if params.end_date_time == None:
                    #     condition=f"a.client_id={user_data['client_id']} AND a.device_id={params.device_id} AND a.date BETWEEN '{params.start_date_time}' AND '{params.start_date_time}'"
                    # condition=f"a.client_id={user_data['client_id']} AND a.device_id={params.device_id} AND a.date BETWEEN '{params.start_date_time}' AND '{params.end_date_time}'"
            elif params.report_type == "Y":  #yearly
                fdatetdate=first_year_day_last_year_day(params.start_date_time)
                condition = f"""ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id} AND COALESCE(
                            a.billing_price,
                            (
                                SELECT
                                    a2.billing_price
                                FROM
                                    md_billing_organization AS a2
                                WHERE
                                    a2.created_at < ed.date
                                ORDER BY
                                    a2.created_at DESC
                                LIMIT 1
                            )
                        ) IS NOT NULL"""
                select=f""" ed.energy_data_id,
                            ed.device_id,
                            ed.do_channel,
                            ed .e1,
                            ed .e2,
                            ed .e3,
                            DATE_FORMAT(ed.date, '%Y-%m-%d') AS date,
                            TIME_FORMAT(ed.time, '%H:%i:%s') AS time,
                            
                            
                            COALESCE(
                                a.billing_price, 
                                (
                                    SELECT a2.billing_price 
                                    FROM md_billing_organization AS a2 
                                    WHERE DATE(a2.created_at) < DATE(ed.date) 
                                    ORDER BY DATE(a2.created_at) DESC 
                                    LIMIT 1
                                )
                            ) AS billing_price
                            """
                            
                table =f""" td_energy_data AS ed
                                INNER JOIN(
                                    SELECT
                                        MAX(energy_data_id) AS max_energy_data_id,
                                        YEAR(DATE) AS YEAR,
                                        MONTH(DATE) AS MONTH
                                    FROM
                                        td_energy_data
                                    WHERE
                                        client_id = 1 AND device_id = 1
                                        AND date BETWEEN '{fdatetdate["first_day"]}' AND '{fdatetdate["last_day"]}'
                                    GROUP BY
                                        YEAR(DATE),
                                        MONTH(DATE)
                                ) AS sub_ed
                                ON
                                ed.energy_data_id = sub_ed.max_energy_data_id 
                                
                                LEFT JOIN 
                                    md_billing_organization AS a ON DATE(ed.date) = DATE(a.created_at)
                                
                                """
                data = select_data(table,select, condition,order_by="ed.date ASC, ed.time ASC")
                
                
                condition2=f"""client_id = {user_data['client_id']} AND device_id = {params.device_id} AND date < '{fdatetdate["first_day"]}' """
                end_date_last_row=select_one_data("td_energy_data","e1,e2,e3, date,time", condition2, order_by="date DESC, time DESC ")
            elif params.report_type == "C": # customized
                condition = f"""ed.client_id = {user_data['client_id']} AND ed.device_id = {params.device_id}  AND COALESCE(
                                a.billing_price,
                                (
                                    SELECT
                                        a2.billing_price
                                    FROM
                                        md_billing_organization AS a2
                                    WHERE
                                        a2.created_at < ed.date
                                    ORDER BY
                                        a2.created_at DESC
                                    LIMIT 1
                                )
                            ) IS NOT NULL"""
                select=f"""ed.e1,ed.e2,ed.e3,ed.energy_data_id, ed.device_id, ed.do_channel, ed.activep1, ed.activep2, ed.activep3, ed.apparentp1, ed.apparentp2, ed.apparentp3, ed.pf1, ed.pf2, ed.pf3, DATE_FORMAT(ed.date, '%Y-%m-%d') AS date, TIME_FORMAT(ed.time, '%H:%i:%s') AS time,
                
                COALESCE(
                                a.billing_price, 
                                (
                                    SELECT a2.billing_price 
                                    FROM md_billing_organization AS a2 
                                    WHERE DATE(a2.created_at) < DATE(ed.date) 
                                    ORDER BY DATE(a2.created_at) DESC 
                                    LIMIT 1
                                )
                            ) AS billing_price
                
                """
                table=f"""td_energy_data AS ed
                                INNER JOIN (
                                    SELECT
                                        date,
                                        MAX(time) AS max_time
                                    FROM
                                        td_energy_data
                                    WHERE
                                        client_id = {user_data['client_id']} AND device_id = {params.device_id}
                                        AND date BETWEEN '{params.start_date_time}' AND '{params.end_date_time}'
                                    GROUP BY
                                        date
                                ) AS sub_ed ON ed.date = sub_ed.date AND ed.time = sub_ed.max_time
                                
                                LEFT JOIN 
                                    md_billing_organization AS a ON DATE(ed.date) = DATE(a.created_at)
                                
                                """
                data = select_data(table,select, condition,order_by="ed.date ASC, ed.time ASC")
                
                
                condition2=f"client_id = {user_data['client_id']} AND device_id = {params.device_id} AND date < '{params.start_date_time}'"
                end_date_last_row=select_one_data("td_energy_data","e1,e2,e3, date,time", condition2, order_by="date DESC, time DESC ")
        # elif user_data['user_type'] == "U" or user_data['user_type'] == "O":
        #     print("fxgbxd")
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
        condition_bill = f"a.organization_id=b.organization_id AND c.organization_id=a.organization_id AND c.countries_id=d.id AND a.client_id = {user_data['client_id']} AND b.client_id={user_data['client_id']} AND a.device_id = {params.device_id}"
        select_bill = "b.*,d.*"
        master_bill = select_one_data("md_manage_user_device AS a,md_billing_organization AS b,st_ms_organization AS c,md_lo_countries AS d",select_bill, condition_bill)
        
        
        return {"data":data , "master_bill":master_bill,"end_date_last_row":end_date_last_row}
    except Exception as e:
        return ValueError("Error in energy_usage_billing",e)
        
    
    