from pydantic import BaseModel, field_validator
from typing import List, Optional

class ExpenseCreate(BaseModel):
    """Schema for creating a new expense."""
    amount: float
    description: str
    split_method: str
    exact_splits: Optional[dict] = None
    percentage_splits: Optional[dict] = None
    user_ids: List[int]
    paid_by: int
