from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import ExtendedExcursionSchema
from db.config import get_db
import db.crud.extended_excursion_crud as crud


router = APIRouter(prefix="/extended_excursion", tags=["extended_excursion"])


@router.get("/list")
async def list_extended_excursion(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_extended_excursion(db, skip, limit)

@router.post("/create", response_model=str)
async def create_extended_excursion(extended_excursion_create: ExtendedExcursionSchema, db: Session = Depends(get_db)):
    return crud.create_extended_excursion(db, extended_excursion_create)

@router.post("/delete", response_model=str)
async def delete_extended_excursion(extended_excursion_delete: ExtendedExcursionSchema, db: Session = Depends(get_db)):
    return crud.delete_extended_excursion(db, extended_excursion_delete)

@router.post("/update", response_model=str)
async def update_extended_excursion(extended_excursion_update: ExtendedExcursionSchema, db: Session = Depends(get_db)):
    return crud.update_extended_excursion(db, extended_excursion_update)