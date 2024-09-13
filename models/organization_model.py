from pydantic import BaseModel, Field, constr, validator

class AddOrganization(BaseModel):
    client_id: int
    organization_name: str
    created_by: int


class EditOrganization(BaseModel):
    client_id: int
    organization_id: int
    organization_name: str
    created_by: int
    
class DeleteOrganization(BaseModel):
    client_id: int
    organization_id: int
    # created_by: int
    
class ListOrganization(BaseModel):
    client_id: int