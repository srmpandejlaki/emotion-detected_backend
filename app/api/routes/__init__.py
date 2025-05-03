from app.api.routes import data_collection_router, preprocessing_router, processing_router, validation_router

all_routers = [
    data_collection_router.router,
    preprocessing_router.router,
    processing_router.router,
    validation_router.router,
    # tambahkan yang lain nanti di sini
]

