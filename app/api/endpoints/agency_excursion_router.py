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

@router.post("/delete", response_model=str)
async def delete_agency_excursion(agency_excursion_delete: AgencyExcursionAssociationSchema, db: Session = Depends(get_db)):
    return crud.delete_agency_excursion(db, agency_excursion_delete)
