from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerPlan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)


class Plan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    price: int
    description: str | None
    customers: list["Customer"] = Relationship(
        back_populates="plans", link_model=CustomerPlan
    )


class CustomerBase(SQLModel):
    name: str
    description: str | None
    email: EmailStr = Field(unique=True)
    age: int


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(
        back_populates="customers", link_model=CustomerPlan
    )


class TransactionBase(SQLModel):
    amount: int
    description: str | None


class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")


class TransactionCreate(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id")


class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def amount_total(self) -> int:
        return sum(transaction.amount for transaction in self.transactions)
