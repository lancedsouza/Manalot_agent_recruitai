from app.db_jd.db import engine, Base
from app.db_jd.jd_models import JD

# Create the database tables
Base.metadata.create_all(bind=engine)   

print("Database tables created successfully.") 
