from fastapi import APIRouter, status
from models import Plan
from db import SessionDependency
from sqlmodel import select

router = APIRouter(tags=["Plans"])


@router.post("/plans", response_model=Plan, status_code=status.HTTP_201_CREATED)
async def create_plan(plan: Plan, session: SessionDependency):
    plan = Plan.model_validate(plan.model_dump())
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@router.get("/plans", response_model=list[Plan])
async def list_plans(session: SessionDependency):
    return session.exec(select(Plan)).all()
