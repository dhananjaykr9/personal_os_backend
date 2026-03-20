from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class TransactionBase(BaseModel):
    amount: float
    type: str
    category: str
    note: Optional[str] = None

class TransactionCreate(TransactionBase):
    timestamp: Optional[datetime] = None

class Transaction(TransactionBase):
    id: UUID
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class CategoryBase(BaseModel):
    name: str
    icon: Optional[str] = "Activity"
    is_default: bool = False

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class BudgetBase(BaseModel):
    category: str
    limit_amount: float
    month: int
    year: int

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class LoanBase(BaseModel):
    type: str # given, taken
    person: str
    amount: float
    due_date: Optional[datetime] = None
    note: Optional[str] = None
    status: str = "pending"

class LoanCreate(LoanBase):
    timestamp: Optional[datetime] = None

class Loan(LoanBase):
    id: UUID
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class PriceBase(BaseModel):
    item_name: str
    price: float

class PriceCreate(PriceBase):
    pass

class Price(PriceBase):
    id: UUID
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
