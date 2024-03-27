from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import AgencyExcursionAssociationSchema
from db.config import get_db
import db.crud.agency_excursion_crud as crud


router = APIRouter(prefix="/agency_excursion", tags=["agency_excursion"])


@router.get("/list")
async def list_agency_excursion(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_agency_excursion(db, skip, limit)

@router.post("/create", response_model=str)
async def create_agency_excursion(agency_excursion_create: AgencyExcursionAssociationSchema, db: Session = Depends(get_db)):
    return crud.create_agency_excursion(db, agency_excursion_create)

@router.get("/delete/{agency_id}{excursion_id}", response_model=str)
async def delete_agency_excursion(agency_id: int, excursion_id: int, db: Session = Depends(get_db)):
    return crud.delete_agency_excursion(db, agency_id, excursion_id)

@router.get("/get_weekend_excursions/{agency_id}")
async def get_weekend_excursions(agency_id:int, db:Session=Depends(get_db)):
    return crud.get_weekend_excursions(db, agency_id)