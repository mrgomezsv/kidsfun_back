from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class RelativeBase(BaseModel):
    name: str
    age: int

class RelativeCreate(RelativeBase):
    pass

class RelativeResponse(RelativeBase):
    pass

class WaiverCreate(BaseModel):
    user_id: str
    user_name: str
    user_email: EmailStr
    relatives: List[RelativeCreate]

class WaiverResponse(BaseModel):
    message: str
    waiver: dict
    email_sent: bool
    is_new: bool

class WaiverValidation(BaseModel):
    qr_code: str

class WaiverDataCreate(BaseModel):
    user_id: str
    user_name: str
    relative_name: str
    relative_age: int

class WaiverDataResponse(BaseModel):
    id: int
    user_id: str
    user_name: str
    relative_name: str
    relative_age: int

    class Config:
        from_attributes = True

class WaiverValidatorCreate(BaseModel):
    email: EmailStr

class WaiverValidatorResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True 