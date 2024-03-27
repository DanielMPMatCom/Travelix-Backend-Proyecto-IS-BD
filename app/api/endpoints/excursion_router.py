from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import ExcursionSchema
from db.config import get_db
import db.crud.excursion_crud as crud


router = APIRouter(prefix="/excursion", tags=["excursion"])


@router.get("/list")
async def list_excursion(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_excursion(db, skip, limit)

@router.post("/create", response_model=str)
async def create_excursion(excursion_create: ExcursionSchema, db: Session = Depends(get_db)):
    return crud.create_excursion(db, excursion_create)

@router.get("/delete/{excursion_id}", response_model=str)
async def delete_excursion(excursion_id: int, db: Session = Depends(get_db)):
    return crud.delete_excursion(db, excursion_id)

@router.post("/update", response_model=str)
async def update_excursion(excursion_update: ExcursionSchema, db: Session = Depends(get_db)):
    return crud.update_excursion(db, excursion_update)
