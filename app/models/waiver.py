from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class WaiverData(Base):
    __tablename__ = "api_waiver_waiverdata"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False)
    user_name = Column(String(100), nullable=False)
    relative_name = Column(String(100), nullable=False)
    relative_age = Column(Integer, nullable=False)
    timestamp = Column(String(30), nullable=False)
    user_email = Column(String(255), nullable=True)

class WaiverValidator(Base):
    __tablename__ = "api_waiver_waiverqr"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __str__(self):
        return self.email

class WaiverDataDB(Base):
    __tablename__ = "t_app_product_waiverdata"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    user_name = Column(String(100), nullable=False)
    relative_name = Column(String(100), nullable=False)
    relative_age = Column(Integer, nullable=False) 