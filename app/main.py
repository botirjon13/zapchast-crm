from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, customers, parts, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Store Management")

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(parts.router)
app.include_router(orders.router)
