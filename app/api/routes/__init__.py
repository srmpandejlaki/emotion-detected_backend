from fastapi import APIRouter

from app.api.routes import (
    data_collection_router,
    preprocessing_router,
    processing_router,
    validation_router
)

router = APIRouter()

router.include_router(data_collection_router.router, prefix="/dataset", tags=["Data Collection"])
router.include_router(preprocessing_router.router, prefix="/preprocessing", tags=["Preprocessing"])
router.include_router(processing_router.router, prefix="/processing", tags=["Processing"])
router.include_router(validation_router.router, prefix="/validation", tags=["Validation"])
