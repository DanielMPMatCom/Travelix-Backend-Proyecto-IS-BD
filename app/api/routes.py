from fastapi import APIRouter
from api.endpoints.agency_router import router as agency_router
from api.endpoints.tourist_router import router as tourist_router

router = APIRouter()
router.include_router(agency_router)
router.include_router(tourist_router)
