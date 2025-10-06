from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import auth, customers, parts, orders
from app.database import engine, Base
import os

# Create DB tables (simple startup auto-create; for production use migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zapchat CRM")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(parts.router, prefix="/parts", tags=["parts"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])

# serve static frontend
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get('/')
def root():
    return {"msg":"Zapchat CRM running. Open /static/index.html for simple frontend."}
