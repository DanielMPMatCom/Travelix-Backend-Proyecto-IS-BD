from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import OfferSchema
from db.config import get_db
import db.crud.offer_crud as crud


router = APIRouter(prefix="/offer", tags=["offer"])


@router.get("/list")
async def list_offer(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_offer(db, skip, limit)

@router.post("/create", response_model=str)
async def create_offer(offer_create: OfferSchema, db: Session = Depends(get_db)):
    return crud.create_offer(db, offer_create)

@router.get("/delete/{offer_id}", response_model=str)
async def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    return crud.delete_offer(db, offer_id)

@router.post("/update", response_model=str)
async def update_offer(offer_update: OfferSchema, db: Session = Depends(get_db)):
    return crud.update_offer(db, offer_update)
