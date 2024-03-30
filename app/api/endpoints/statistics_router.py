from fastapi import APIRouter, HTTPException, Path, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db.config import get_db
import os
from db.exporter import export_to_excel

import db.crud.statistics_crud as crud

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/packages-above-average")
def get_packages_above_average(export: str = None, db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    
    if export is None:
        return crud.packages_above_average(db)
    if export == "excel":
        background_tasks.add_task(os.remove, "packages_above_average.xlsx")
        return export_to_excel("packages_above_average.xlsx", crud.packages_above_average(db))

@router.get("/agencies-balance")
def get_agencies_balance(export: str = None, db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):

    if export is None:
        return crud.agencies_balance(db)
    if export == "excel":
        background_tasks.add_task(os.remove, "agencies_balance.xlsx")
        return export_to_excel("agencies_balance.xlsx",  crud.agencies_balance(db))

