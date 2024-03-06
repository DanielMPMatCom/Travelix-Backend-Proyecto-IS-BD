from fastapi import APIRouter
from api.endpoints.agency_router import router as agency_router

router = APIRouter()
router.include_router(agency_router)