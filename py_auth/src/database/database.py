from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(url=DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine, autoflush=False)
session = Session()