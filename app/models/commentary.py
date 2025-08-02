from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Commentary(Base):
    __tablename__ = "t_app_commentary"
    
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String(256), nullable=False)
    user_id = Column(String(100), nullable=False)
    product_id = Column(Integer, nullable=False)
    
    def __str__(self):
        return f'Commentary {self.id}' 