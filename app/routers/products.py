from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import os
import shutil
from datetime import datetime

from ..database import get_db
from ..models.product import Product
from ..models.user import User
from ..models.like import Like
from ..models.commentary import Commentary
from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductList, ProductWithStats
from ..routers.auth import get_current_user
from ..config import settings

router = APIRouter()

def save_upload_file(upload_file: UploadFile, destination: str):
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

@router.get("/", response_model=List[ProductWithStats])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    
    if search:
        query = query.filter(Product.title.ilike(f"%{search}%"))
    
    products = query.offset(skip).limit(limit).all()
    
    # Agregar conteos de likes y comentarios
    result = []
    for product in products:
        likes_count = db.query(Like).filter(
            Like.product == str(product.id),
            Like.is_favorite == True
        ).count()
        
        comments_count = db.query(Commentary).filter(
            Commentary.product_id == product.id
        ).count()
        
        product_dict = {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "category": product.category,
            "created": product.created,
            "user_id": product.user_id,
            "youtube_url": product.youtube_url,
            "img": product.img,
            "img1": product.img1,
            "img2": product.img2,
            "img3": product.img3,
            "img4": product.img4,
            "img5": product.img5,
            "likes_count": likes_count,
            "comments_count": comments_count
        }
        result.append(product_dict)
    
    return result

@router.get("/{product_id}", response_model=ProductWithStats)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Agregar conteos de likes y comentarios
    likes_count = db.query(Like).filter(
        Like.product == str(product.id),
        Like.is_favorite == True
    ).count()
    
    comments_count = db.query(Commentary).filter(
        Commentary.product_id == product.id
    ).count()
    
    product_dict = {
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "created": product.created,
        "user_id": product.user_id,
        "youtube_url": product.youtube_url,
        "img": product.img,
        "img1": product.img1,
        "img2": product.img2,
        "img3": product.img3,
        "img4": product.img4,
        "img5": product.img5,
        "likes_count": likes_count,
        "comments_count": comments_count
    }
    
    return product_dict

@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_product = Product(**product.dict(), user_id=current_user.id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user owns the product or is admin
    if db_product.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user owns the product or is admin
    if db_product.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.post("/{product_id}/upload-image")
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Check file size
    if file.size > settings.max_file_size:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Get product
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check permissions
    if db_product.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(settings.upload_dir, "product_images")
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    save_upload_file(file, file_path)
    
    # Update product image (for now, just update the main image)
    db_product.img = f"product_images/{filename}"
    db.commit()
    db.refresh(db_product)
    
    return {"filename": filename, "url": f"/media/product_images/{filename}"} 