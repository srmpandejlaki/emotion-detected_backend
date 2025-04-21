from fastapi import APIRouter
from app.api.controllers.processing_controller import train_model_endpoint, delete_model_endpoint

router = APIRouter()

# Menambahkan endpoint ke router
router.post("/train_model/{ratio_str}")(train_model_endpoint)
router.delete("/delete_model/{model_id}")(delete_model_endpoint)
