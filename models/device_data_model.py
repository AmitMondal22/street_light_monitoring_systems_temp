from pydantic import BaseModel, Field, constr, validator
from datetime import date,datetime,time
import re
from typing import Optional,List


class EnergyDeviceData(BaseModel):
    CLIENT_ID:  Optional[int] = 0
    UID: str
    DT: str
    TIME: str
    TW: int
    CH: int
    KWH1: float
    KWH2: Optional[float] = 0.0
    KWH3: Optional[float] = 0.0
    R: float
    Y: Optional[float] = 0.0
    B: Optional[float] = 0.0
    R_Y: Optional[float] = 0.0
    Y_B: Optional[float] = 0.0
    B_R: Optional[float] = 0.0
    # R_Y: Optional[float] = Field(0.0, alias="R-Y")
    # Y_B: Optional[float] = Field(0.0, alias="R-Y")
    # B_R: Optional[float] = Field(0.0, alias="R-Y")
    AMP1: float
    AMP2: Optional[float] = 0.0
    AMP3: Optional[float] = 0.0
    KW1: float
    KW2: Optional[float] = 0.0
    KW3: Optional[float] = 0.0
    KVA1: float
    KVA2: Optional[float] = 0.0
    KVA3: Optional[float] = 0.0
    KVAR1: float
    KVAR2: Optional[float] = 0.0
    KVAR3: Optional[float] = 0.0
    PF1: float
    PF2: Optional[float] = 0.0
    PF3: Optional[float] = 0.0
    AVGVLN: float
    AVGVLL: float
    AVGAMP: float
    TOTKW: float
    TOTKVA: float
    TOTKVAR: float
    FREQ: float
    RUNHR: float
#     client_id: int
#     device_id: int
#     device: str
#     do_channel: int
#     e1: float
#     e2: Optional[float] = None
#     e3: Optional[float] = None
#     r: float
#     y: Optional[float] = None
#     b: Optional[float] = None
#     r_y: Optional[float] = None
#     y_b: Optional[float] = None
#     b_r: Optional[float] = None
#     curr1: float
#     curr2: Optional[float] = None
#     curr3: Optional[float] = None
#     activep1: float
#     activep2: Optional[float] = None
#     activep3: Optional[float] = None
#     apparentp1: float
#     apparentp2: Optional[float] = None
#     apparentp3: Optional[float] = None
#     pf1: float
#     pf2: Optional[float] = None
#     pf3: Optional[float] = None
#     freq: Optional[float] = None
#     reactvp1: float
#     reactvp2: Optional[float] = None
#     reactvp3: Optional[float] = None
#     avaragevln: Optional[float] = None
#     avaragevll: Optional[float] = None
#     avaragecurrent: Optional[float] = None
#     totkw: Optional[float] = None
#     totkva: Optional[float] = None
#     totkvar: Optional[float] = None
#     runhr: Optional[float] = None
    
   
# $flow=(round((100*$r->rpm)/2800, 2) >100)?100:round((100*$r->rpm)/2800, 2);


class DeviceAutoRegister(BaseModel):
    # client_id: int
    ib_id: int
    # device_id: int
    do_channel:int
    model:str
    lat:str
    lon:str
    imei_no:str


class CheckedDevices(BaseModel):
    device:str
    
class EnergyData(BaseModel):
    client_id: int
    device_id: int
    device: str
    start_date: date
    end_date: date
    
    
class EnergyUsed(BaseModel):
    device_id: int
    device: str
    type: str
    # start_date: date
    # end_date: date
    # start_date_time: datetime = Field(..., alias="start_date_time", description="Format: '%Y-%m-%d %H:%M:%S'")
    # start_date_time: datetime
    # end_date_time: datetime
    
    
class VoltageData(BaseModel):
    client_id: int
    device_id: int
    device: str
    start_date_time: datetime
    end_date_time: datetime
    
class WsEnergyData(BaseModel):
    client_id: int
    device_id: int
    device: str
    
    
    
# ==========================================
# ==========================================



class UpsDeviceData(BaseModel):
    client_id: int
    device_id: int
    device: str
    do_channel: int
    device_location: str
    device_output_current: float
    device_input_current: float
    
    
    
# ========================================

class AddAlert(BaseModel):
    client_id: int
    organization_id: int
    device_id: int
    device: str
    unit_id: int
    alert_type: str
    alert_status: str
    alert_status: str
    alert_value: float
    alert_email : str
    create_by: int
    @validator('alert_type')
    def validate_alert_type(cls, v):
        valid_alert_types = {"3H", "2L", "1CL", "4CH"}
        if v not in valid_alert_types:
            raise ValueError('Invalid alert type')
        return v
    @validator('alert_status')
    def validate_alert_status(cls, v):
        valid_alert_status = {"Y", "N"}
        if v not in valid_alert_status:
            raise ValueError('Invalid alert status')
        return v
    @validator('alert_email')
    def validate_email(cls, alert_email):
        # Regular expression for basic email validation
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, alert_email):
            raise ValueError("Invalid email address")
        return alert_email
    
class EditAlert(BaseModel):
    alert_id: int
    client_id: int
    organization_id: int
    device_id: int
    device: str
    unit_id: int
    alert_type: str
    alert_status: str
    alert_status: str
    alert_value: float
    alert_email : str
    create_by: int
    @validator('alert_type')
    def validate_alert_type(cls, v):
        valid_alert_types = {"3H", "2L", "1CL", "4CH"}
        if v not in valid_alert_types:
            raise ValueError('Invalid alert type')
        return v
    @validator('alert_status')
    def validate_alert_status(cls, v):
        valid_alert_status = {"Y", "N"}
        if v not in valid_alert_status:
            raise ValueError('Invalid alert status')
        return v
    @validator('alert_email')
    def validate_email(cls, alert_email):
        # Regular expression for basic email validation
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, alert_email):
            raise ValueError("Invalid email address")
        return alert_email

class DeleteAlert(BaseModel):
    alert_id: int
    client_id: int
    organization_id: int
    device_id: int
    
    
class DeviceAdd(BaseModel):
    client_id: int
    device: str
    device_name: str
    do_channel: int
    model: str
    lat: str
    lon: str
    imei_no: str
    device_type: str
    meter_type: str
    last_maintenance: date
    @validator('meter_type')
    def validate_meter_type(cls, v):
        validate_meter_type = {"ENSF", "ENTF"}
        if v not in validate_meter_type:
            raise ValueError('Invalid alert status')
        return v
    @validator('device_type')
    def validate_device_type(cls, v):
        valid_device_type = {"EN", "UPS"}
        if v not in valid_device_type:
            raise ValueError('Invalid alert status')
        return v

class DeviceEdit(BaseModel):
    device_id:int
    client_id: int
    device: str
    device_name: str
    do_channel: int
    model: str
    lat: str
    lon: str
    imei_no: str
    device_type: str
    meter_type: str
    @validator('meter_type')
    def validate_meter_type(cls, v):
        valid_meter_type = {"ENSF", "ENTF"}
        if v not in valid_meter_type:
            raise ValueError('Invalid alert status')
        return v
    @validator('device_type')
    def validate_device_type(cls, v):
        valid_device_type = {"EN", "UPS"}
        if v not in valid_device_type:
            raise ValueError('Invalid alert status')
        return v
    
class UserDeviceList(BaseModel):
    client_id: int
    device_id: int
    device: str
    user_id: int
    organization_id:int



class WsDeviceData(BaseModel):
    client_id: int
    device_id: int
    device: str
    

class BllingData(BaseModel):
    billing_type: str
    billing_price: float
    billing_status: str
    billing_day: int

class OrganizationSettings(BaseModel):
    organization_id: int
    client_id: int
    countries_id: int
    states_id: int
    regions_id: int
    subregions_id: int
    cities_id: int
    address: str
    created_by: int
    billing_data: List[BllingData]
    
class OrganizationSettingsList(BaseModel):
    organization_id: int
    
class AddBill(BaseModel):
    organization_id: int
    billing_type: str
    billing_price: float
    billing_day: int
    
class EditOrganization(BaseModel):
    organization_id: int
    countries_id: int
    states_id: int
    regions_id: int
    subregions_id: int
    cities_id: int
    address: str
    
class DeviceSchedule(BaseModel):
    client_id: int
    device_id: int
    device: str