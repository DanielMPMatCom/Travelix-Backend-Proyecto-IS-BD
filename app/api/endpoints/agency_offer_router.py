from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import AgencyOfferAssociationSchema
from db.config import get_db
import db.crud.agency_offer_crud as crud


router = APIRouter(prefix="/agency_offer", tags=["agency_offer"])


@router.get("/list")
async def list_agency_offer(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_agency_offer(db, skip, limit)