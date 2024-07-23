from pydantic import BaseModel, Field, constr, field_validator,FieldValidationInfo
from datetime import date,datetime,time


class MqttEnergyDeviceData(BaseModel):
    ib_id: int
    device_id: int
    device: str
    do_channel: int
    device_type: str
    device_location: str
    device_run_hours: float # number of hours the device has been running
    # device_run_hours: time # time
    device_dc_bus_voltage: float
    device_output_current: float
    device_settings_freq: float
    device_running_freq: float
    device_rpm: float
    device_flow: float
    
    
class MqttPublishDeviceData(BaseModel):
    device_id: int
    device: str
    device_type: str
    do_channel: int
    relay_close_time: str
    timer_start_hours: str
    timer_start_minutes: str
    timer_stop_hours_1: str
    timer_stop_minutes_1: str

    # @field_validator('relay_close_time', 'timer_start_hours', 'timer_start_minutes', 'timer_stop_hours_1', 'timer_stop_minutes_1')
    # def validate_time_format(cls, value: str, info: FieldValidationInfo) -> str:
    #     try:
    #         datetime.strptime(value, '%H:%M:%S')
    #     except ValueError:
    #         raise ValueError(f"Field '{info.field_name}' should be in 'H:i:s' format")
    #     return value
