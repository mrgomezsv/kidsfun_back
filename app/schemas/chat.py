from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class ChatRoomCreate(BaseModel):
    pass

class ChatRoomResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    is_active: bool
    last_message_at: datetime
    user_name: str

    class Config:
        from_attributes = True

class ChatMessageCreate(BaseModel):
    content: str

class ChatMessageResponse(BaseModel):
    id: int
    chat_room_id: int
    sender_id: int
    content: str
    timestamp: datetime
    is_read: bool
    sender_name: str

    class Config:
        from_attributes = True

class ChatAdministratorCreate(BaseModel):
    email: EmailStr

class ChatAdministratorResponse(BaseModel):
    id: int
    user_id: int
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True 