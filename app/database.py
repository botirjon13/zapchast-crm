# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Agar SQLite ishlatayotgan bo‘lsangiz:
SQLALCHEMY_DATABASE_URL = "sqlite:///./store.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# MUHIM: Base shu yerda e’lon qilinadi
Base = declarative_base()

# DB session olish uchun
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
