from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class ContactBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, description="Nombre del contacto")
    last_name: str = Field(..., min_length=1, max_length=100, description="Apellido del contacto")
    contact_number: str = Field(..., min_length=1, max_length=20, description="Número de teléfono")
    email: EmailStr = Field(..., description="Email del contacto")
    reason: str = Field(..., min_length=1, description="Mensaje o razón del contacto")

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    is_read: Optional[bool] = None
    is_responded: Optional[bool] = None

class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    is_read: bool
    is_responded: bool
    
    class Config:
        from_attributes = True

class ContactList(BaseModel):
    contacts: list[ContactResponse]
    total: int
    page: int
    per_page: int 