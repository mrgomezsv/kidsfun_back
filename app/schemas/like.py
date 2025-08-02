from pydantic import BaseModel, Field
from datetime import datetime

class LikeBase(BaseModel):
    user: str = Field(..., min_length=1, max_length=100)
    product: str = Field(..., min_length=1, max_length=100)
    is_favorite: bool

class LikeCreate(LikeBase):
    pass

class LikeResponse(LikeBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True 