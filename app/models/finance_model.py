from sqlalchemy import Column, String, Float, DateTime, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from ..database import Base

class TransactionModel(Base):
    __tablename__ = "finance_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False) # expense, income
    category = Column(String, nullable=False)
    note = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class CategoryModel(Base):
    __tablename__ = "finance_categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    icon = Column(String, nullable=True) # Lucide icon name
    is_default = Column(Boolean, default=False)

class BudgetModel(Base):
    __tablename__ = "finance_budgets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String, nullable=False)
    limit_amount = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class LoanModel(Base):
    __tablename__ = "finance_loans"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False) # given, taken
    person = Column(String, nullable=False) 
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    status = Column(String, default="pending") # pending, returned
    note = Column(String, nullable=True)

class PriceModel(Base):
    __tablename__ = "finance_prices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
