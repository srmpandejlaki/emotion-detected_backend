from .dataset import router as dataset_router
from .preprocessing import router as preprocessing_router
from .training import router as training_router
from .validation import router as validation_router

all_routers = [dataset_router, preprocessing_router, training_router, validation_router]
