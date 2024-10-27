from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import users as user_schema
from sqlalchemy.orm import Session
from app.models import models
from app.core.database import get_db
import re

router = APIRouter()

@router.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    
    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Validate mobile number (example: must be 10 digits)
    if not re.match(r"^\d{10}$", user.mobile):
        raise HTTPException(status_code=400, detail="Mobile number must be 10 digits")
    
    # Check for existing user with the same email
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the user
    db_user = models.User(name=user.name, email=user.email, mobile=user.mobile)
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the user")
    
    return db_user

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a user by user ID."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    """Retrieve all users."""
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users