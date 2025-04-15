from app.database.database import engine
from app.models import models

# create table in database
models.Base.metadata.create_all(bind=engine)

# jalankan dengan cara python app/create_db.py