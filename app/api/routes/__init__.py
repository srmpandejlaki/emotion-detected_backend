from .data_collection_router import router as data_collection_router
from .preprocessing_router import router as preprocessing_router
from .processing_router import router as processing_router
from .validation_route import router as validation_route
from .evaluation_route import router as evaluation_route

all_routers = [data_collection_router, preprocessing_router, processing_router, validation_route, evaluation_route]
