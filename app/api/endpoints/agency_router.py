from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import AgencySchema
from db.config import get_db
import db.crud.agency_crud as crud


router = APIRouter(prefix="/agency", tags=["agency"])


@router.get("/list")
async def list_agency(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_agency(db, skip, limit)