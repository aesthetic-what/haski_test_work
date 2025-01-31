from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str
    
class IMEI_Request(BaseModel):
    imei: int