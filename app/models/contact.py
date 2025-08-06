from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from ..database import Base

class Contact(Base):
    __tablename__ = "t_app_contact"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    contact_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, default=False)
    is_responded = Column(Boolean, default=False)
    
    def __str__(self):
        return f"Contact from {self.first_name} {self.last_name} - {self.email}" 