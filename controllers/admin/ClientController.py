
from db_model.MASTER_MODEL import select_data, insert_data,update_data,delete_data
from utils.date_time_format import get_current_datetime

@staticmethod
def add_organization(organization):
    try:
              
        current_datetime = get_current_datetime()
        columns = "client_id,organization_name, created_by, created_at"
        value = f"{organization.client_id},'{organization.organization_name}', {organization.created_by},'{current_datetime}'"
        organization_id = insert_data("md_organization", columns, value)
        if organization_id is None:
            raise ValueError("organization registration failed")
        else:
            user_data = {"user_id": organization_id, "organization_name": organization.organization_name, "created_by": organization.created_by}
        return user_data
    except Exception as e:
        raise e
    
@staticmethod
def list_organization(params,user_data):
    try:
        if user_data["user_type"]=='U' or user_data["user_type"]=='O':
            condition =f"client_id = {user_data['client_id']} AND organization_id = {user_data['organization_id']}"
        elif user_data["user_type"]=='C':
            condition =f"client_id = {user_data['client_id']}"
            
        select="client_id,organization_id, organization_name, created_by, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at"
        data = select_data("md_organization", select,condition)
        return data
    except Exception as e:
        raise e
    
    
@staticmethod
def edit_organization(organization):
    try:
        condition = f"organization_id = {organization.organization_id} AND client_id={organization.client_id}"
        columns={"organization_name":organization.organization_name,"created_by":organization.created_by,"updated_at":get_current_datetime()}
        data = update_data("md_organization", columns, condition)
        return data
    except Exception as e:
        raise e

@staticmethod
def delete_organization(organization):
    try:
        condition = f"organization_id = {organization.organization_id} AND client_id={organization.client_id}"
        data = delete_data("md_organization", condition)
        return data
    except Exception as e:
        raise e
    

@staticmethod
def energy_data(energy_data):
    try:
        table="td_energy_data AS ed, md_device AS md"
        select="ed.energy_data_id, ed.device_id, ed.device, ed.do_channel, ed.e1, ed.e2, ed.e3, ed.r, ed.y, ed.b, ed.r_y, ed.y_b, ed.b_r, ed.curr1, ed.curr2, ed.curr3, ed.activep1, ed.activep2, ed.activep3, ed.apparentp1, ed.apparentp2, ed.apparentp3, ed.pf1, ed.pf2, ed.pf3, ed.freq, ed.reactvp1, ed.reactvp2, ed.reactvp3, ed.avaragevln, ed.avaragevll, ed.avaragecurrent, ed.totkw, ed.totkva, ed.totkvar, ed.runhr, ed.date, ed.time , DATE_FORMAT(ed.created_at, '%Y-%m-%d %H:%i:%s') AS created_at,md.device,md.device_type, md.meter_type, md.device_name"
        
        condition = f"ed.device_id=md.device_id AND ed.device_id = {energy_data.device_id} AND ed.device = '{energy_data.device}' AND ed.date BETWEEN '{energy_data.start_date}' AND '{energy_data.end_date}'"
        order_by="ed.date DESC, ed.time DESC"
        data=select_data(table, select,condition,order_by)
        return data
    except Exception as e:
        raise e