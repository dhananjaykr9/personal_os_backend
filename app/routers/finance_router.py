from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from ..database import get_db
from ..schemas.finance_schema import (
    Transaction, TransactionCreate, 
    Budget, BudgetCreate, 
    Price, PriceCreate,
    Category, CategoryCreate,
    Loan, LoanCreate
)
from ..services.finance_service import FinanceService
from ..models import finance_model

router = APIRouter()

# --- Transactions ---
@router.post("/transactions", response_model=Transaction)
def add_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return FinanceService.add_transaction(db, transaction)

@router.get("/transactions", response_model=List[Transaction])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(finance_model.TransactionModel).order_by(finance_model.TransactionModel.timestamp.desc()).all()

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: UUID, db: Session = Depends(get_db)):
    db_transaction = db.query(finance_model.TransactionModel).filter(finance_model.TransactionModel.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return {"status": "deleted"}

@router.get("/summary")
def get_summary(period: str = "daily", db: Session = Depends(get_db)):
    return FinanceService.get_summary(db, period)

# --- Categories ---
@router.get("/categories", response_model=List[Category])
def get_categories(db: Session = Depends(get_db)):
    return FinanceService.get_categories(db)

@router.post("/categories", response_model=Category)
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return FinanceService.add_category(db, category)

# --- Budgets ---
@router.post("/budgets", response_model=Budget)
def set_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    return FinanceService.set_budget(db, budget)

@router.get("/budgets/{category}/check")
def check_budget(category: str, db: Session = Depends(get_db)):
    result = FinanceService.check_budget_limit(db, category)
    if not result:
        raise HTTPException(status_code=404, detail="No budget set for this category")
    return result

# --- Loans ---
@router.get("/loans", response_model=List[Loan])
def get_loans(status: str = "pending", db: Session = Depends(get_db)):
    return FinanceService.get_loans(db, status)

@router.post("/loans", response_model=Loan)
def add_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    return FinanceService.add_loan(db, loan)

@router.patch("/loans/{loan_id}", response_model=Loan)
def update_loan_status(loan_id: UUID, status: str, db: Session = Depends(get_db)):
    loan = FinanceService.update_loan_status(db, loan_id, status)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan entry not found")
    return loan

# --- Prices ---
@router.post("/prices", response_model=Price)
def add_price(price: PriceCreate, db: Session = Depends(get_db)):
    return FinanceService.add_price(db, price)

@router.get("/prices/{item_name}/trend", response_model=List[Price])
def get_price_trend(item_name: str, db: Session = Depends(get_db)):
    return FinanceService.get_price_trend(db, item_name)
