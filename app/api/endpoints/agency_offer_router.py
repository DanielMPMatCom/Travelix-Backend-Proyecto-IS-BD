from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import AgencyOfferAssociationSchema
from db.config import get_db
import db.crud.agency_offer_crud as crud


router = APIRouter(prefix="/agency_offer", tags=["agency_offer"])


@router.get("/list")
async def list_agency_offer(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_agency_offer(db, skip, limit)

@router.post("/create", response_model=str)
async def create_agency_offer(agency_offer_create: AgencyOfferAssociationSchema, db: Session = Depends(get_db)):
    return crud.create_agency_offer(db, agency_offer_create)

@router.get("/delete/{agency_id}/{offer_id}", response_model=str)
async def delete_agency_offer(agency_id: int, offer_id:int, db: Session = Depends(get_db)):
    return crud.delete_agency_offer(db, agency_id, offer_id)

@router.post("/update", response_model=str)
async def update_agency_offer(agency_offer_update: AgencyOfferAssociationSchema, db: Session = Depends(get_db)):
    return crud.update_agency_offer(db, agency_offer_update)
