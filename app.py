
from flask import Flask, render_template, request, redirect, send_file
from config import Config
from models import db, Property, Unit, Tenant, Transaction
from analytics import financial_summary
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def dashboard():
    income, expenses, profit = financial_summary(db)
    properties = Property.query.all()
    return render_template('dashboard.html', income=income, expenses=expenses, profit=profit, properties=properties)

@app.route('/properties', methods=['GET','POST'])
def properties():
    if request.method == 'POST':
        p = Property(name=request.form['name'], address=request.form['address'], purchase_price=request.form['price'])
        db.session.add(p)
        db.session.commit()
        return redirect('/properties')
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

@app.route('/units/<pid>', methods=['GET','POST'])
def units(pid):
    if request.method == 'POST':
        u = Unit(property_id=pid, unit_number=request.form['unit'], rent=request.form['rent'], status='vacant')
        db.session.add(u)
        db.session.commit()
    units = Unit.query.filter_by(property_id=pid).all()
    return render_template('units.html', units=units, pid=pid)

@app.route('/tenants', methods=['GET','POST'])
def tenants():
    if request.method == 'POST':
        t = Tenant(first_name=request.form['first'], last_name=request.form['last'], email=request.form['email'], phone=request.form['phone'])
        db.session.add(t)
        db.session.commit()
    tenants = Tenant.query.all()
    return render_template('tenants.html', tenants=tenants)

@app.route('/transactions', methods=['GET','POST'])
def transactions():
    if request.method == 'POST':
        t = Transaction(property_id=request.form['property'], unit_id=request.form['unit'], category=request.form['category'], amount=request.form['amount'], type=request.form['type'], notes=request.form['notes'], date=request.form['date'])
        db.session.add(t)
        db.session.commit()
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', transactions=transactions)

@app.route('/export')
def export():
    data = Transaction.query.all()
    df = pd.DataFrame([{
        'date':t.date,
        'category':t.category,
        'amount':t.amount,
        'type':t.type,
        'notes':t.notes
    } for t in data])
    path = 'tax_export.csv'
    df.to_csv(path, index=False)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run()
