from fastapi import APIRouter
from api.endpoints.agency_router import router as agency_router
from api.endpoints.tourist_router import router as tourist_router
from api.endpoints.excursion_router import router as excursion_router
from api.endpoints.offer_router import router as offer_router
from api.endpoints.hotel_router import router as hotel_router
from api.endpoints.facility_router import router as facility_router
from api.endpoints.tourist_type_router import router as tourist_type_router
from api.endpoints.agency_offer_router import router as agency_offer_router
from api.endpoints.agency_excursion_router import router as agency_excursion_router
from api.endpoints.excursion_reservation_router import router as excursion_reservation_router
from api.endpoints.tourist_type_tourist_router import router as tourist_type_tourist_router
from api.endpoints.package_router import router as package_router
from api.endpoints.extended_excursion_router import router as extended_excursion_router
from api.endpoints.hotel_extended_excursion_router import router as hotel_extended_excursion_router
from api.endpoints.package_facility_router import router as package_facility_router
from api.endpoints.package_reservation_router import router as package_reservation_router
from api.endpoints.statistics_router import router as statistics_router
from api.endpoints.root_router import router as root_router
from api.endpoints.user_router import router as user_router


router = APIRouter()
router.include_router(agency_router)
router.include_router(excursion_router)
router.include_router(extended_excursion_router)
router.include_router(agency_excursion_router)
router.include_router(offer_router)
router.include_router(hotel_router)
router.include_router(agency_offer_router)
router.include_router(hotel_extended_excursion_router)
router.include_router(tourist_router)
router.include_router(tourist_type_router)
router.include_router(tourist_type_tourist_router)
router.include_router(facility_router)
router.include_router(package_router)
router.include_router(package_facility_router)
router.include_router(excursion_reservation_router)
router.include_router(package_reservation_router)
router.include_router(statistics_router)
router.include_router(root_router)
router.include_router(user_router)