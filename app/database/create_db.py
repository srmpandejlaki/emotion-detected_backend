from app.database.database import engine
from app.database import model_database

# create table in database
model_database.Base.metadata.create_all(bind=engine)

# jalankan dengan cara python app/create_db.py