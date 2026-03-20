from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from uuid import UUID
from ..models.finance_model import TransactionModel, BudgetModel, PriceModel, CategoryModel, LoanModel
from ..schemas.finance_schema import TransactionCreate, BudgetCreate, PriceCreate, CategoryCreate, LoanCreate

class FinanceService:
    @staticmethod
    def add_transaction(db: Session, transaction: TransactionCreate):
        data = transaction.model_dump()
        if not data.get('timestamp'):
            data['timestamp'] = datetime.utcnow()
        db_transaction = TransactionModel(**data)
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    @staticmethod
    def get_summary(db: Session, period: str = "daily"):
        now = datetime.utcnow()
        if period == "daily":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "weekly":
            from datetime import timedelta
            start_date = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        query = db.query(
            TransactionModel.type,
            func.sum(TransactionModel.amount).label("total")
        ).filter(TransactionModel.timestamp >= start_date).group_by(TransactionModel.type)
        
        results = query.all()
        summary_map = {r.type: float(r.total) for r in results}
        return {
            "expense": summary_map.get("expense", 0),
            "income": summary_map.get("income", 0)
        }

    @staticmethod
    def set_budget(db: Session, budget: BudgetCreate):
        # Update if exists for same month/year/category
        existing = db.query(BudgetModel).filter(
            BudgetModel.category == budget.category,
            BudgetModel.month == budget.month,
            BudgetModel.year == budget.year
        ).first()
        
        if existing:
            existing.limit_amount = budget.limit_amount
            db.commit()
            db.refresh(existing)
            return existing
        
        db_budget = BudgetModel(**budget.model_dump())
        db.add(db_budget)
        db.commit()
        db.refresh(db_budget)
        return db_budget

    @staticmethod
    def check_budget_limit(db: Session, category: str):
        now = datetime.utcnow()
        budget = db.query(BudgetModel).filter(
            BudgetModel.category == category,
            BudgetModel.month == now.month,
            BudgetModel.year == now.year
        ).first()
        
        if not budget:
            return None
        
        total_spent = db.query(func.sum(TransactionModel.amount)).filter(
            TransactionModel.category == category,
            TransactionModel.type == "expense",
            TransactionModel.timestamp >= now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        ).scalar() or 0
        
        percentage = (total_spent / budget.limit_amount) * 100
        return {
            "limit": budget.limit_amount,
            "spent": total_spent,
            "percentage": percentage,
            "breached": percentage >= 100
        }

    @staticmethod
    def add_price(db: Session, price: PriceCreate):
        db_price = PriceModel(**price.model_dump())
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return db_price

    @staticmethod
    def get_price_trend(db: Session, item_name: str):
        prices = db.query(PriceModel).filter(
            PriceModel.item_name.ilike(f"%{item_name}%")
        ).order_by(PriceModel.timestamp.desc()).limit(10).all()
        return prices

    # --- Category Management ---
    @staticmethod
    def get_categories(db: Session):
        categories = db.query(CategoryModel).all()
        if not categories:
            # Seed defaults if empty
            defaults = [
                ("Personal", "User"), ("Travel", "Plane"), ("Food", "Zap"),
                ("Bills", "CreditCard"), ("Room/Rent", "Home"), ("Loan Given", "ArrowUpRight"),
                ("Loan Taken", "ArrowDownRight"), ("Health", "Activity"), ("Shopping", "Tag"), ("Misc", "Layout")
            ]
            for name, icon in defaults:
                db_cat = CategoryModel(name=name, icon=icon, is_default=True)
                db.add(db_cat)
            db.commit()
            categories = db.query(CategoryModel).all()
        return categories

    @staticmethod
    def add_category(db: Session, category: CategoryCreate):
        db_category = CategoryModel(**category.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    # --- Loan Management ---
    @staticmethod
    def add_loan(db: Session, loan: LoanCreate):
        data = loan.model_dump()
        if not data.get('timestamp'):
            data['timestamp'] = datetime.utcnow()
        db_loan = LoanModel(**data)
        db.add(db_loan)
        db.commit()
        db.refresh(db_loan)
        
        # Also record as a transaction for balance tracking
        trans_type = "expense" if loan.type == "given" else "income"
        FinanceService.add_transaction(db, TransactionCreate(
            amount=loan.amount,
            type=trans_type,
            category=loan.type.replace('_', ' ').title(),
            note=f"Loan to/from {loan.person}: {loan.note or ''}",
            timestamp=data['timestamp']
        ))
        
        return db_loan

    @staticmethod
    def get_loans(db: Session, status: str = "pending"):
        return db.query(LoanModel).filter(LoanModel.status == status).order_by(LoanModel.timestamp.desc()).all()

    @staticmethod
    def update_loan_status(db: Session, loan_id: UUID, status: str):
        db_loan = db.query(LoanModel).filter(LoanModel.id == loan_id).first()
        if db_loan:
            # If returning a loan, record the reverse transaction
            if db_loan.status == "pending" and status == "returned":
                trans_type = "income" if db_loan.type == "given" else "expense"
                FinanceService.add_transaction(db, TransactionCreate(
                    amount=db_loan.amount,
                    type=trans_type,
                    category="Loan Returned",
                    note=f"Return of loan from/to {db_loan.person}",
                    timestamp=datetime.utcnow()
                ))
            
            db_loan.status = status
            db.commit()
            db.refresh(db_loan)
        return db_loan
