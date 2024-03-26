from fastapi import APIRouter, HTTPException, Path, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db.config import get_db
import os

import db.crud.statistics_crud as crud

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/packages-above-average")
def get_packages_above_average(db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    background_tasks.add_task(os.remove, "packages_above_average.xlsx")
    return crud.packages_above_average(db, "packages_above_average.xlsx")


@router.get("/agencies-balance")
def get_agencies_balance(db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    background_tasks.add_task(os.remove, "agencies_balance.xlsx")
    return crud.agencies_balance(db, "agencies_balance.xlsx")

