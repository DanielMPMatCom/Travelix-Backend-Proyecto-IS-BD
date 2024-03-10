from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import AgencyExcursionAssociationSchema
from db.config import get_db
import db.crud.agency_excursion_crud as crud


router = APIRouter(prefix="/agency_excursion", tags=["agency_excursion"])


@router.get("/list")
async def list_agency_excursion(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_agency_excursion(db, skip, limit)