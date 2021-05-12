from flask import Flask, render_template, json, request, redirect, flash

import database.db_connector as db

import os

# Configuration

app = Flask(__name__)

db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")


# Employees
@app.route('/employees')
def Employees():
    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return render_template("Employees.j2", Employees=results)

@app.route('/create-employee',  methods = ('GET', 'POST'))
def createEmployee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        title = request.form['title']
        date_of_hire = request.form['date_of_hire']
        date_of_termination = request.form['date_of_termination']
        phone = request.form['phone']
        email = request.form['email']
        
        query = "INSERT INTO Employees (first_name, last_name, title, date_of_hire, date_of_termination, phone, email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, title, date_of_hire, date_of_termination, phone, email))
        results = cursor.fetchall()
        return redirect('/employees')

    return render_template("createEmployee.j2")



def get_employee(id):
    query = "SELECT employee_id, first_name, last_name, title, date_of_hire, date_of_termination, phone, email FROM Employees WHERE employee_id =" + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    employee = cursor.fetchone()

    return employee

@app.route('/<int:id>/delete', methods=('GET', 'POST'))
def deleteEmployee(id):
    employee = get_employee(id)

    query = "DELETE FROM Employees WHERE employee_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return redirect('/employees')


@app.route('/<int:id>/update-employee', methods = ('GET', 'POST'))
def updateEmployee(id):

    employee = get_employee(id)

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        title = request.form['title']
        date_of_hire = request.form['date_of_hire']
        date_of_termination = request.form['date_of_termination']
        phone = request.form['phone']
        email = request.form['email']
        
        query = "UPDATE Employees SET first_name=%s, last_name=%s, title=%s, date_of_hire=%s, date_of_termination=%s, phone=%s, email=%s WHERE employee_id=" + str(id)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, title, date_of_hire, date_of_termination, phone, email))
        results = cursor.fetchall()
        return redirect('/employees')

    return render_template("updateEmployee.j2", employee=employee)


# Customers
@app.route('/customers')
def Customers():
    return render_template("Customers.j2")

@app.route('/create-customer')
def createCustomer():
    return render_template("createCustomer.j2")

@app.route('/update-customer')
def updateCustomer():
    return render_template("updateCustomer.j2")


# Vehicles
@app.route('/vehicles')
def Vehicles():
    return render_template("Vehicles.j2")

@app.route('/create-vehicle')
def createVehicle():
    return render_template("createVehicle.j2")

@app.route('/update-vehicle')
def updateVehicle():
    return render_template("updateVehicle.j2")


# Sales
@app.route('/sales')
def Sales():
    return render_template("Sales.j2")

@app.route('/create-sale')
def createSale():
    return render_template("createSale.j2")

@app.route('/update-sale')
def updateSale():
    return render_template("updateSale.j2")


# Employees_Customers_Map (Assign Salesperson)
@app.route('/assign-salesperson')
def Employees_Customers_Map():
    return render_template("Employees_Customers_Map.j2")


# Listener 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8532))
    app.run(port=port, debug=True) 


