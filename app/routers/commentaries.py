from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.commentary import Commentary
from ..schemas.commentary import CommentaryCreate, CommentaryResponse

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
    db: Session = Depends(get_db)
):
    db_commentary = Commentary(**commentary.dict())
    db.add(db_commentary)
    db.commit()
    db.refresh(db_commentary)
    return db_commentary

@router.delete("/{commentary_id}")
async def delete_commentary(
    commentary_id: int,
    db: Session = Depends(get_db)
):
    commentary = db.query(Commentary).filter(Commentary.id == commentary_id).first()
    if commentary is None:
        raise HTTPException(status_code=404, detail="Commentary not found")
    
    db.delete(commentary)
    db.commit()
    return {"message": "Commentary deleted successfully"} 