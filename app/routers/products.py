from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
import os
import shutil
from datetime import datetime
from decimal import Decimal

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
    publicated: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    # Construir query base
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    
    if search:
        query = query.filter(Product.title.ilike(f"%{search}%"))
    
    if publicated is not None:
        query = query.filter(Product.publicated == publicated)
    
    # Obtener productos con paginación
    products = query.offset(skip).limit(limit).all()
    
    if not products:
        return []
    
    # Obtener IDs de productos para consultas optimizadas
    product_ids = [p.id for p in products]
    
    # Consulta optimizada para likes - obtener todos los likes de una vez
    likes_query = db.query(
        Like.product,
        func.count(Like.id).label('likes_count')
    ).filter(
        and_(
            Like.product.in_([str(pid) for pid in product_ids]),
            Like.is_favorite == True
        )
    ).group_by(Like.product)
    
    likes_results = likes_query.all()
    likes_dict = {row.product: row.likes_count for row in likes_results}
    
    # Consulta optimizada para comentarios - obtener todos los comentarios de una vez
    comments_query = db.query(
        Commentary.product_id,
        func.count(Commentary.id).label('comments_count')
    ).filter(
        Commentary.product_id.in_(product_ids)
    ).group_by(Commentary.product_id)
    
    comments_results = comments_query.all()
    comments_dict = {row.product_id: row.comments_count for row in comments_results}
    
    # Construir resultado
    result = []
    for product in products:
        product_dict = {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "price": Decimal(str(product.price)) if product.price else None,
            "category": product.category,
            "created": product.created,
            "publicated": product.publicated,
            "user_id": product.user_id,
            "youtube_url": product.youtube_url,
            "img": product.img,
            "img1": product.img1,
            "img2": product.img2,
            "img3": product.img3,
            "img4": product.img4,
            "img5": product.img5,
            "dimensions": product.dimensions,
            "circuits": product.circuits,
            "space": product.space,
            "likes_count": likes_dict.get(str(product.id), 0),
            "comments_count": comments_dict.get(product.id, 0)
        }
        result.append(product_dict)
    
    return result

@router.get("/{product_id}", response_model=ProductWithStats)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    # Obtener producto con consulta optimizada
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Consultas optimizadas para likes y comentarios
    likes_count = db.query(func.count(Like.id)).filter(
        and_(
            Like.product == str(product.id),
            Like.is_favorite == True
        )
    ).scalar() or 0
    
    comments_count = db.query(func.count(Commentary.id)).filter(
        Commentary.product_id == product.id
    ).scalar() or 0
    
    product_dict = {
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "price": Decimal(str(product.price)) if product.price else None,
        "category": product.category,
        "created": product.created,
        "publicated": product.publicated,
        "user_id": product.user_id,
        "youtube_url": product.youtube_url,
        "img": product.img,
        "img1": product.img1,
        "img2": product.img2,
        "img3": product.img3,
        "img4": product.img4,
        "img5": product.img5,
        "dimensions": product.dimensions,
        "circuits": product.circuits,
        "space": product.space,
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