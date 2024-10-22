from pydantic import BaseModel

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str
    email: str
    mobile: str