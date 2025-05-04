from fastapi import APIRouter
from app.api.routes.data_collection_router import router as data_collection_router
from app.api.routes.preprocessing_router import router as preprocessing_router
from app.api.routes.processing_router import router as processing_router
from app.api.routes.validation_router import router as validation_router

router = APIRouter()
router.include_router(data_collection_router)
router.include_router(preprocessing_router)
router.include_router(processing_router)
router.include_router(validation_router)
