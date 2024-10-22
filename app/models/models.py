from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    """User model representing a user in the system."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    mobile = Column(String, unique=True)


class Expense(Base):
    """Expense model representing an expense record."""
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    paid_by = Column(Integer, ForeignKey('users.id'))  # Reference to the user who paid
    split_method = Column(String)
    user_ids = Column(String)  # Store user IDs as a comma-separated string

    # Relationship to get the user who paid
    payer = relationship("User", backref="expenses")


class Balance(Base):
    """Balance model representing a user's balance record."""
    __tablename__ = 'balance'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Reference to the user
    user_name = Column(String)  # Store user name directly
    # expense_id = Column(Integer, ForeignKey('expenses.id'))  # Reference to the expense
    amount_owed = Column(Float)

    # Relationships
    user = relationship("User", backref="balance")
    # expense = relationship("Expense", backref="balance")
