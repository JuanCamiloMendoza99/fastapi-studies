from pydantic import BaseModel, NameEmail
from sqlmodel import SQLModel


class CustomerBase(SQLModel):
    name: str
    description: str | None
    email: NameEmail
    age: int


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase, table=True):
    id: int | None = None


class Transaction(BaseModel):
    id: int
    amount: int
    description: str


class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def amount_total(self) -> int:
        return sum(transaction.amount for transaction in self.transactions)
