from fastapi import FastAPI, Request
from datetime import datetime
import zoneinfo
from db import create_all_tables
from .routers import customers, invoices, transactions, plans
import time


app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(invoices.router)
app.include_router(plans.router)
app.include_router(transactions.router)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"Request {request.url.path} took {duration:.4f} seconds")
    return response


@app.middleware("http")
async def log_requests_headers(request: Request, call_next):
    print(f"Request Headers: {request.headers}")
    response = await call_next(request)
    return response


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
