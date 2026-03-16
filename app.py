
from flask import Flask, render_template, request, redirect, send_file
from database import query, execute
from reports import tax_export
from config import Config

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)

@app.route("/")
def dashboard():
    income = query("SELECT SUM(amount) total FROM transactions WHERE type='income'")
    expenses = query("SELECT SUM(amount) total FROM transactions WHERE type='expense'")

    income = income[0]["total"] if income and income[0]["total"] else 0
    expenses = expenses[0]["total"] if expenses and expenses[0]["total"] else 0
    profit = income - expenses

    return render_template("dashboard.html",income=income,expenses=expenses,profit=profit)

@app.route("/properties",methods=["GET","POST"])
def properties():
    if request.method=="POST":
        execute("INSERT INTO properties(name,address) VALUES (?,?)",
        (request.form["name"],request.form["address"]))

    properties=query("SELECT * FROM properties")
    return render_template("properties.html",properties=properties)

@app.route("/units/<pid>",methods=["GET","POST"])
def units(pid):
    if request.method=="POST":
        execute("INSERT INTO units(property_id,name,rent) VALUES (?,?,?)",
        (pid,request.form["name"],request.form["rent"]))

    units=query("SELECT * FROM units WHERE property_id=?",(pid,))
    return render_template("units.html",units=units,pid=pid)

@app.route("/transactions")
def transactions():
    data=query("""
    SELECT
    t.*,p.name property,u.name unit
    FROM transactions t
    LEFT JOIN properties p ON p.id=t.property_id
    LEFT JOIN units u ON u.id=t.unit_id
    ORDER BY date DESC
    """)
    return render_template("transactions.html",transactions=data)

@app.route("/add",methods=["GET","POST"])
def add():
    if request.method=="POST":
        execute("""
        INSERT INTO transactions
        (property_id,unit_id,date,type,category,amount,notes)
        VALUES (?,?,?,?,?,?,?)
        """,(
        request.form["property"],
        request.form["unit"],
        request.form["date"],
        request.form["type"],
        request.form["category"],
        request.form["amount"],
        request.form["notes"]
        ))
        return redirect("/transactions")

    properties=query("SELECT * FROM properties")
    units=query("SELECT * FROM units")

    return render_template("add_transaction.html",properties=properties,units=units)

@app.route("/export")
def export():
    file=tax_export()
    return send_file(file,as_attachment=True)

if __name__ == "__main__":
    app.run()
