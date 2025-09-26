from fastapi import FastAPI
from datetime import datetime
import zoneinfo
from models import Transaction, Invoice
from db import create_all_tables
from .routers import customers


app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)


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


@app.post("/transactions")
async def create_transaction(transaction: Transaction):
    return transaction


@app.post("/invoices")
async def create_invoice(invoice: Invoice):
    return invoice
