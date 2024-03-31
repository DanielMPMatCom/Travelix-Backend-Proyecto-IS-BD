from fastapi import APIRouter, HTTPException, Path, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session

from schemas import AgencySchema
from db.config import get_db
import db.crud.agency_crud as crud
from db.exporter import export_to_excel
import os


router = APIRouter(prefix="/agency", tags=["agency"])


@router.get("/list")
async def list_agency(db:Session=Depends(get_db), skip:int=0, limit:int=10):
    return crud.list_agency(db, skip, limit)

@router.post("/create", response_model=str)
async def create_agency(agency_create: AgencySchema, db: Session = Depends(get_db)):
    return crud.create_agency(db, agency_create)

@router.get("/delete/{agency_id}", response_model=str)
async def delete_agency(agency_id: int, db: Session = Depends(get_db)):
    return crud.delete_agency(db, agency_id)

@router.post("/update", response_model=str)
async def update_agency(agency_update: AgencySchema, db: Session = Depends(get_db)):
    return crud.update_agency(db, agency_update)


@router.get("/get/{agency_id}")
async def get_agency(agency_id: int, db: Session = Depends(get_db)):
    agency = crud.get_agency(db, agency_id)
    return agency if agency is not None else HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Agency not found")

@router.get("/agency-balance/{agency_id}")
def get_agency_balance(agency_id: int, export: str = None, db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):

    if export is None:
        return crud.agency_balance_by_agency(db, agency_id)
    if export == "excel":
        background_tasks.add_task(os.remove, "agency_balance.xlsx")
        return export_to_excel("agency_balance.xlsx",  crud.agency_balance_by_agency(db, agency_id))

@router.get("/packages_above_average/{agency_id}")
async def packages_above_average(agency_id:int, export: str = None, db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    
    packages = crud.agency_packages_above_average(db, agency_id)

    if export is None:
        return packages
    if export == "excel":
        background_tasks.add_task(os.remove, "packages_above_average.xlsx")
        return export_to_excel("packages_above_average.xlsx", packages)
    
@router.get("/most_frecuent_tourists/{agency_id}")
async def most_frecuent_tourists(agency_id:int, export: str = None, db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    
    tourists = crud.most_frecuent_tourists(db, agency_id)

    if export is None:
        return tourists
    if export == "excel":
        background_tasks.add_task(os.remove, "most_frecuent_tourists.xlsx")
        return export_to_excel("most_frecuent_tourists.xlsx", tourists)