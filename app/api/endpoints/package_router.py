from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session

from schemas import PackageSchema
from db.config import get_db
import db.crud.package_crud as crud


router = APIRouter(prefix="/package", tags=["package"])


@router.get("/list")
async def list_package(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_package(db, skip, limit)