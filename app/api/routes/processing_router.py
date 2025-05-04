from fastapi import APIRouter
from app.api.controllers import processing_controller

router = APIRouter()
router.include_router(processing_controller.router)
