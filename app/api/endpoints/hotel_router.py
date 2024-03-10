from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import HotelSchema
from db.config import get_db
import db.crud.hotel_crud as crud


router = APIRouter(prefix="/hotel", tags=["hotel"])


@router.get("/list")
async def list_hotel(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_hotel(db, skip, limit)