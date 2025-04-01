from .auth import router as auth_router
from .dataset import router as dataset_router
from .preprocessing import router as preprocessing_router
from .training import router as training_router
from .validation import router as validation_router

all_routers = [auth_router, validation_router, dataset_router]
