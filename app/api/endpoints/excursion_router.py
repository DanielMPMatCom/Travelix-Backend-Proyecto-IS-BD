from fastapi import APIRouter, HTTPException, Path, Depends, status
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

@router.get("/get/{excursion_id}")
async def get_excursion(excursion_id: int, db: Session = Depends(get_db)):
    excursion = crud.get_excursion(db, excursion_id)
    return excursion if excursion is not None else HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Excursion not found")

@router.get("/list_remaining/{agency_id}")
async def list_remaining(agency_id: int, db: Session = Depends(get_db)):
    return crud.list_remaining_excursions(db, agency_id)

@router.get("/list_reservable")
async def list_reservable(db: Session = Depends(get_db)):
    return crud.list_reservable_excursions(db)

@router.get("/list_reservable/{agency_id}")
async def list_reservable_by_id(agency_id: int, db: Session = Depends(get_db)):
    return crud.list_reservable_excursions_by_id(db, agency_id)