from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import balance as balance_schema
from app.models import models
from app.core.database import get_db

router = APIRouter()

@router.get("/balance/{user_id}", response_model=List[balance_schema.BalanceCreate])
def get_balance(user_id: int, db: Session = Depends(get_db)):
    """Get a user's balance by user ID."""
    balance = db.query(models.Balance).filter(models.Balance.user_id == user_id).all()
    return balance

@router.get("/balance/", response_model=List[balance_schema.BalanceCreate])
def get_all_balance(db: Session = Depends(get_db)):
    """Get overall balances for all users."""
    balance = db.query(models.Balance).order_by(models.Balance.id.asc()).all()  # Ordered by id ascending
    return balance
