from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str
    location: str = Field(..., min_length=1, max_length=200)
    start_datetime: datetime
    ticket_price: Decimal = Field(default=0.00)
    published: bool = False
    partners: str = Field(..., min_length=1, max_length=50)

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    start_datetime: Optional[datetime] = None
    ticket_price: Optional[Decimal] = None
    published: Optional[bool] = None
    partners: Optional[str] = Field(None, min_length=1, max_length=50)

class EventResponse(EventBase):
    id: int
    organizer_id: int
    
    class Config:
        from_attributes = True 