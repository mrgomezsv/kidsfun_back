from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.commentary import Commentary
from ..models.user import User
from ..schemas.commentary import CommentaryCreate, CommentaryResponse, CommentaryUpdate
from ..routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CommentaryResponse])
async def get_commentaries(
    product_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(Commentary)
    
    if product_id:
        query = query.filter(Commentary.product_id == product_id)
    
    commentaries = query.all()
    return commentaries

@router.post("/", response_model=CommentaryResponse)
async def create_commentary(
    commentary: CommentaryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_commentary = Commentary(**commentary.dict())
    db.add(db_commentary)
    db.commit()
    db.refresh(db_commentary)
    return db_commentary

@router.put("/{commentary_id}", response_model=CommentaryResponse)
async def update_commentary(
    commentary_id: int,
    commentary_update: CommentaryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    commentary = db.query(Commentary).filter(Commentary.id == commentary_id).first()
    if commentary is None:
        raise HTTPException(status_code=404, detail="Commentary not found")
    
    # Check if user owns the commentary or is admin
    if commentary.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = commentary_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(commentary, field, value)
    
    db.commit()
    db.refresh(commentary)
    return commentary

@router.delete("/{commentary_id}")
async def delete_commentary(
    commentary_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    commentary = db.query(Commentary).filter(Commentary.id == commentary_id).first()
    if commentary is None:
        raise HTTPException(status_code=404, detail="Commentary not found")
    
    # Check if user owns the commentary or is admin
    if commentary.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(commentary)
    db.commit()
    return {"message": "Commentary deleted successfully"} 