
from pydantic import BaseModel
from typing import Optional,List

class WhDownlinkParams(BaseModel):
    device_id: int
    start_time: str
    end_time: str
    start_time: Optional[str]
    end_time: Optional[str]
    on_off_flag: Optional[bool]
    dimming:int
