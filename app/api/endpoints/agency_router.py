from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import AgencySchema
from db.config import get_db
import db.crud.agency_crud as crud


router = APIRouter(prefix="/agency", tags=["agency"])


@router.get("/list")
async def list_agency(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_agency(db, skip, limit)

@router.post("/create", response_model=str)
async def create_agency(agency_create: AgencySchema, db: Session = Depends(get_db)):
    return crud.create_agency(db, agency_create)

@router.post("/delete", response_model=str)
async def delete_agency(agency_delete: AgencySchema, db: Session = Depends(get_db)):
    return crud.delete_agency(db, agency_delete)

@router.post("/update", response_model=str)
async def update_agency(agency_update: AgencySchema, db: Session = Depends(get_db)):
    return crud.update_agency(db, agency_update)
