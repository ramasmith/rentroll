
from models import Transaction
from sqlalchemy import func

def financial_summary(db):
    income = db.session.query(func.sum(Transaction.amount)).filter(Transaction.type=='income').scalar() or 0
    expenses = db.session.query(func.sum(Transaction.amount)).filter(Transaction.type=='expense').scalar() or 0
    profit = income - expenses
    return income, expenses, profit
