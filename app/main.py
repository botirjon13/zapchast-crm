from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import auth, customers, parts, orders
from app.database import engine, Base
import os

# Create DB tables (simple startup auto-create; for production use migrations)
Base.metadata.create_all(bind=engine)

from app.database import SessionLocal
from app import models
from app.security import hash_password
from app.core import DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_FULLNAME

def create_default_admin():
    db = SessionLocal()
    try:
        existing = db.query(models.User).filter(models.User.username == DEFAULT_ADMIN_USERNAME).first()
        if not existing:
            user = models.User(
                username=DEFAULT_ADMIN_USERNAME,
                full_name=DEFAULT_ADMIN_FULLNAME,
                password_hash=hash_password(DEFAULT_ADMIN_PASSWORD),
                is_admin=True
            )
            db.add(user)
            db.commit()
            print('Default admin created:', DEFAULT_ADMIN_USERNAME)
        else:
            print('Default admin already exists')
    except Exception as e:
        print('Error creating default admin:', e)
    finally:
        db.close()

# create default admin AFTER tables are created
create_default_admin()

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
