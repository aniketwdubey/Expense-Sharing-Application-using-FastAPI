from pydantic import BaseModel

class BalanceCreate(BaseModel):
    """Schema for creating a new balance record."""
    user_id: int
    user_name: str
    # expense_id: int
    amount_owed: float

