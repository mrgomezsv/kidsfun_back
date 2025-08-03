from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Product(Base):
    __tablename__ = "t_app_product_product"
    
    id = Column(Integer, primary_key=True, index=True)
    img = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50), nullable=False)
    created = Column(DateTime(timezone=True), nullable=False)
    important = Column(Boolean, nullable=False)
    img1 = Column(String(100), nullable=False)
    img2 = Column(String(100), nullable=False)
    img3 = Column(String(100), nullable=False)
    img4 = Column(String(100), nullable=False)
    img5 = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
    youtube_url = Column(String(255), nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="products")
    
    def __str__(self):
        return f"{self.title} - by {self.user.username if self.user else 'Unknown'}" 