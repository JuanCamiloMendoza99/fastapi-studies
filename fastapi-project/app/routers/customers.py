from fastapi import APIRouter, HTTPException, status
from models import Customer, CustomerUpdate, CustomerCreate
from db import SessionDependency
from sqlmodel import select

router = APIRouter(tags=["Customers"])


@router.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDependency):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.get("/customers", response_model=list[Customer])
async def list_customers(session: SessionDependency):
    return session.exec(select(Customer)).all()


@router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer_by_id(customer_id: int, session: SessionDependency):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer


@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDependency):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    session.delete(customer)
    session.commit()
    return {"message": "Customer deleted successfully"}


@router.patch("/customers/{customer_id}", response_model=Customer)
async def update_customer(
    customer_id: int, customer_data: CustomerUpdate, session: SessionDependency
):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(customer_data_dict)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer
