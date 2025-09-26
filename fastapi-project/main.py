from fastapi import FastAPI
from datetime import datetime
import zoneinfo
from models import Customer, Transaction, Invoice, CustomerCreate
from db import SessionDependency


app = FastAPI()


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


db_customers: list[Customer] = []


@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDependency):
    customer = Customer.model_validate(customer_data.model_dump())
    db_customers.append(customer)
    customer.id = len(db_customers)
    return customer


@app.get("/customers", response_model=list[Customer])
async def list_customers():
    return db_customers


@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer_by_id(customer_id: int):
    return next((x for x in db_customers if x.id == customer_id), None)


@app.post("/transactions")
async def create_transaction(transaction: Transaction):
    return transaction


@app.post("/invoices")
async def create_invoice(invoice: Invoice):
    return invoice
