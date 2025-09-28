from fastapi import APIRouter, HTTPException, status, Query
from models import Customer, Transaction, TransactionCreate
from db import SessionDependency
from sqlmodel import select


router = APIRouter(tags=["Transactions"])


@router.post(
    "/transactions", response_model=Transaction, status_code=status.HTTP_201_CREATED
)
async def create_transaction(
    transaction: TransactionCreate, session: SessionDependency
):
    transaction_data_dict = transaction.model_dump()
    customer = session.get(Customer, transaction_data_dict.get("customer_id"))
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    transaction = Transaction.model_validate(transaction_data_dict)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.get("/transactions", response_model=list[Transaction])
async def list_transactions(
    session: SessionDependency,
    offset: int = Query(0, description="Offset for pagination"),
    limit: int = Query(10, description="Limit for pagination"),
):
    return session.exec(select(Transaction).offset(offset).limit(limit)).all()
