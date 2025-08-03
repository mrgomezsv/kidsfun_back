from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Product(Base):
    __tablename__ = "t_app_product_product"
    
    id = Column(Integer, primary_key=True, index=True)
    img = Column(String(100), nullable=True)
    title = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    category = Column(String(50), nullable=True)
    created = Column(DateTime(timezone=True), nullable=True)
    img1 = Column(String(100), nullable=True)
    img2 = Column(String(100), nullable=True)
    img3 = Column(String(100), nullable=True)
    img4 = Column(String(100), nullable=True)
    img5 = Column(String(100), nullable=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=True)
    youtube_url = Column(String(255), nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="products")
    
    def __str__(self):
        return f"{self.title} - by {self.user.username if self.user else 'Unknown'}" 