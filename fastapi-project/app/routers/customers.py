from fastapi import APIRouter, HTTPException, status, Query
from models import (
    Customer,
    CustomerUpdate,
    CustomerCreate,
    Plan,
    CustomerPlan,
    StatusEnum,
)
from db import SessionDependency
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags=["Customers"])


@router.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CustomerCreate, session: SessionDependency):
    try:
        customer_data_dict = customer_data.model_dump()
        customer = Customer.model_validate(customer_data_dict)
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )


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


@router.post(
    "/customers/{customer_id}/plans/{plan_id}",
    response_model=CustomerPlan,
    status_code=status.HTTP_201_CREATED,
)
async def subscribe_customer_to_plan(
    customer_id: int,
    plan_id: int,
    session: SessionDependency,
    plan_status: StatusEnum = Query(),
):
    customer = session.get(Customer, customer_id)
    plan = session.get(Plan, plan_id)
    if not customer or not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer or Plan not found"
        )

    customer_plan = CustomerPlan(
        customer_id=customer.id, plan_id=plan.id, status=plan_status
    )
    session.add(customer_plan)
    session.commit()
    session.refresh(customer_plan)
    return customer_plan


@router.get("/customers/{customer_id}/plans", response_model=list[CustomerPlan])
async def list_customer_plans(
    customer_id: int,
    session: SessionDependency,
    plan_status: StatusEnum = Query(),
):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.status == plan_status)
    )
    customer_plans = session.exec(query).all()  # Ensure the relationship is loaded

    return customer_plans
