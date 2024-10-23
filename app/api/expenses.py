from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import expenses as expense_schema
from app.models import models
from app.core.database import get_db

router = APIRouter()

@router.post("/expenses/")
def create_expense(expense: expense_schema.ExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense and update the balances of users involved."""
    # Validate split method
    if expense.split_method not in ["equal", "exact", "percentage"]:
        raise HTTPException(status_code=400, detail="Invalid split method")

    # Initialize amounts owed dictionary
    amounts_owed = {}

    # Handle splitting logic
    if expense.split_method == "equal":
        split_amount = expense.amount / len(expense.user_ids)
        amounts_owed = {user_id: split_amount for user_id in expense.user_ids}

    elif expense.split_method == "exact":
        if not expense.exact_splits or sum(expense.exact_splits.values()) != expense.amount:
            raise HTTPException(status_code=400, detail="Exact splits must sum to the total amount")
        amounts_owed = expense.exact_splits

    elif expense.split_method == "percentage":
        if not expense.percentage_splits or sum(expense.percentage_splits.values()) != 100:
            raise HTTPException(status_code=400, detail="Percentage splits must sum to 100%")
        amounts_owed = {user_id: (expense.amount * (percentage / 100)) for user_id, percentage in expense.percentage_splits.items()}

    # Create the expense record
    db_expense = models.Expense(
        amount=expense.amount,
        description=expense.description,
        paid_by=expense.paid_by,  # Use the paid_by from the request
        split_method=expense.split_method,
        user_ids=",".join(map(str, expense.user_ids))
    )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    # Update the balance table
    for user_id, amount in amounts_owed.items():
        user_expense = db.query(models.Balance).filter(
            models.Balance.user_id == user_id,
            # models.Balance.expense_id == db_expense.id
        ).first()

        if user_expense:
            # Update the existing record with the new amount owed
            user_expense.amount_owed += amount  # Update the amount owed
        else:
            # Create a new record if it doesn't exist
            user_expense = models.Balance(
                user_id=user_id,
                user_name=db.query(models.User).filter(models.User.id == user_id).first().name,  # Fetch user name
                # expense_id=db_expense.id,
                amount_owed=amount
            )
            db.add(user_expense)

    db.commit()  # Commit the changes to the balance table after all updates/creates

    return db_expense
    # return {
    #     "id": db_expense.id,
    #     "amount": db_expense.amount,
    #     "description": db_expense.description,
    #     "user_ids": db_expense.user_ids.split(','),  # Convert back to list
    #     "split_method": db_expense.split_method,
    #     "paid_by": db_expense.paid_by,
    # }


# Get individual expenses.
@router.get("/expenses/{user_id}")
def get_expenses(user_id: int, db: Session = Depends(get_db)):
    """Retrieve all expenses for a specific user."""
    expenses = db.query(models.Expense).filter(models.Expense.payer.has(id=user_id)).all()  # Use has() for relationship comparison
    return expenses

# Get all expenses
@router.get("/expenses/")
def get_all_expenses(db: Session = Depends(get_db)):
    """Retrieve all expenses."""
    expenses = db.query(models.Expense).all()
    return expenses