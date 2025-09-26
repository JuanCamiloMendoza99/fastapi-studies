from fastapi import FastAPI
from datetime import datetime
import zoneinfo
from db import create_all_tables
from .routers import customers
from .routers import invoices
from .routers import transactions


app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(invoices.router)
app.include_router(transactions.router)


@app.get("/")
async def read_root():
    return {"message": "Hello world 🚀"}


@app.get("/user/{name}")
async def read_item(name: str):
    return {"message": f"Hello {name}, welcome to FastAPI"}


country_timezones = {
    "CO": "America/Bogota",
    "US": "America/New_York",
    "FR": "Europe/Paris",
    "IN": "Asia/Kolkata",
}


@app.get("/time/{iso_code}")
async def get_time(iso_code: str):
    if not iso_code:
        return {"error": "ISO code is required"}

    timezone = country_timezones.get(iso_code.upper())
    if not timezone:
        return {"error": "Country not found"}

    return {"time": datetime.now(zoneinfo.ZoneInfo(timezone))}
