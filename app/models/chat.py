from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class ChatAdministrator(Base):
    __tablename__ = "t_app_chat_administrator"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User")
    
    def __str__(self):
        return self.email

class ChatRoom(Base):
    __tablename__ = "t_app_chat_room"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    last_message_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    messages = relationship("ChatMessage", back_populates="chat_room", cascade="all, delete-orphan")
    
    def __str__(self):
        return f"Chat with {self.user.username if self.user else 'Unknown'}"

class ChatMessage(Base):
    __tablename__ = "t_app_chat_message"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_room_id = Column(Integer, ForeignKey("t_app_chat_room.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, default=False)
    
    # Relationships
    chat_room = relationship("ChatRoom", back_populates="messages")
    sender = relationship("User")
    
    def __str__(self):
        return f"Message from {self.sender.username if self.sender else 'Unknown'} at {self.timestamp}" 