from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routers import auth, customers, parts, orders, stats

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Zapchat CRM')

app.include_router(auth.router, prefix='/auth')
app.include_router(customers.router)
app.include_router(parts.router)
app.include_router(orders.router)
app.include_router(stats.router)

from fastapi.staticfiles import StaticFiles
app.mount('/static', StaticFiles(directory='app/static'), name='static')
