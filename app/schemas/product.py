from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = None
    category: str = Field(..., min_length=1, max_length=50)
    circuits: Optional[str] = None
    dimensions: Optional[str] = None
    space: Optional[str] = None
    youtube_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    circuits: Optional[str] = None
    dimensions: Optional[str] = None
    space: Optional[str] = None
    youtube_url: Optional[str] = None
    publicated: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    img: str
    img1: str
    img2: str
    img3: str
    img4: str
    img5: str
    created: datetime
    publicated: bool
    user_id: Optional[int] = None
    likes_count: Optional[int] = 0
    comments_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class ProductList(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    per_page: int

class ProductWithStats(ProductResponse):
    likes_count: int = 0
    comments_count: int = 0 