from .auth import router as auth_router
from .validation import router as validation_router
from .dataset import router as dataset_router

all_routers = [auth_router, validation_router, dataset_router]
