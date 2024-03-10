from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import ExcursionSchema
from db.config import get_db
import db.crud.excursion_crud as crud


router = APIRouter(prefix="/excursion", tags=["excursion"])


@router.get("/list")
async def list_excursion(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_excursion(db, skip, limit)