from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()
engine = create_engine("sqlite:///scheduler.db", echo=True, future=True) #specify the database type that you want to use. File or in-memory database. Connects to a sqlite db
from models import *
Base.metadata.create_all(bind=engine) #this is only being used during dev but I will replace it with Alembic once all is done. And Alembic will handle both creating tables and updating them when there needs to be updates.
SessionLocal = sessionmaker(autoflush=False, bind=engine)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()