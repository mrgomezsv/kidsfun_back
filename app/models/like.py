from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Like(Base):
    __tablename__ = "t_app_like"
    
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(100), nullable=False)
    product = Column(String(100), nullable=False)
    is_favorite = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __str__(self):
        return f"{self.user} - {self.product} - {self.is_favorite}" 