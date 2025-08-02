from pydantic import BaseModel, Field
from datetime import datetime

class CommentaryBase(BaseModel):
    comment: str = Field(..., min_length=1, max_length=256)
    user_id: str = Field(..., min_length=1, max_length=100)
    product_id: int

class CommentaryCreate(CommentaryBase):
    pass

class CommentaryResponse(CommentaryBase):
    id: int
    
    class Config:
        from_attributes = True 