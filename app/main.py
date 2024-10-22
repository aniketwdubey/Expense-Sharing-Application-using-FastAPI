from fastapi import FastAPI
from app.api import balance, users, expenses
import app.models.models as models
from app.core.database import engine

app = FastAPI()

app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(balance.router)

models.Base.metadata.create_all(bind=engine)
