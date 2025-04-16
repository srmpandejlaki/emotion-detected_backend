from fastapi import APIRouter
from controllers.preprocessing_controller import preprocess_data, save_preprocessed

router = APIRouter(prefix="/preprocessing", tags=["Preprocessing"])

router.post("/process")(preprocess_data)
router.post("/save")(save_preprocessed)
