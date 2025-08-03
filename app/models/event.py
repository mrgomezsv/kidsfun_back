from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Event(Base):
    __tablename__ = "t_app_event"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(200), nullable=False)
    start_datetime = Column(DateTime(timezone=True), nullable=False)
    organizer_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
    ticket_price = Column(Numeric(10, 2), default=0.00)
    published = Column(Boolean, default=False)
    partners = Column(String(50), nullable=False)
    
    # Relationship
    organizer = relationship("User")
    
    def __str__(self):
        return self.title 