from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.like import Like
from ..schemas.like import LikeCreate, LikeResponse
from ..routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[LikeResponse])
async def get_likes(
    product_id: int = None,
    user_id: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Like)
    
    if product_id:
        query = query.filter(Like.product == str(product_id))
    
    if user_id:
        query = query.filter(Like.user == user_id)
    
    likes = query.all()
    return likes

@router.post("/", response_model=LikeResponse)
async def create_like(
    like: LikeCreate,
    db: Session = Depends(get_db)
):
    # Check if like already exists
    existing_like = db.query(Like).filter(
        Like.user == like.user,
        Like.product == like.product
    ).first()
    
    if existing_like:
        # Update existing like
        existing_like.is_favorite = like.is_favorite
        db.commit()
        db.refresh(existing_like)
        return existing_like
    
    # Create new like
    db_like = Like(**like.dict())
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

@router.delete("/{like_id}")
async def delete_like(
    like_id: int,
    db: Session = Depends(get_db)
):
    like = db.query(Like).filter(Like.id == like_id).first()
    if like is None:
        raise HTTPException(status_code=404, detail="Like not found")
    
    db.delete(like)
    db.commit()
    return {"message": "Like deleted successfully"} 