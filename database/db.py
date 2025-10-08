import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/dbname")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_user_role(telegram_id: int):
    session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    session.close()
    if user:
        return user.role
    return None

def add_user(telegram_id: int, full_name: str, role: str):
    session = SessionLocal()
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    if user is None:
        user = User(telegram_id=telegram_id, full_name=full_name, role=role)
        session.add(user)
        session.commit()
    session.close()
