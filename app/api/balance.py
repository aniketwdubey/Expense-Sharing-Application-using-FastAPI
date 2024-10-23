import csv
from tempfile import NamedTemporaryFile
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
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

@router.get("/download", response_class=FileResponse)
def download_balance_sheet(db: Session = Depends(get_db)):
    balances = db.query(models.Balance).all()
    
    if not balances:
        raise HTTPException(status_code=404, detail="No balances found")

    # Create a temporary CSV file for the balance sheet
    with NamedTemporaryFile(delete=False, mode='w', newline='') as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(['User ID', 'User Name', 'Amount Owed'])  # CSV header

        # Write each balance to the CSV file
        for balance in balances:
            writer.writerow([balance.user_id, balance.user_name, balance.amount_owed])

        # Get the file path
        temp_file_path = temp_file.name

    # Serve the CSV file as a downloadable file
    return FileResponse(
        path=temp_file_path,
        media_type='application/octet-stream',
        filename='balance_sheet.csv',
        headers={'Content-Disposition': 'attachment; filename=balance_sheet.csv'}
    )
