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
    query = "SELECT * FROM Customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Employees = cursor.fetchall()

    return render_template("Customers.j2", Customers=results, Employees=Employees)


@app.route('/create-customer', methods=('GET', 'POST'))
def createCustomer():
    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Employees = cursor.fetchall()

    if request.method == 'POST':
        customer_first_name = request.form['customer_first_name']
        customer_last_name = request.form['customer_last_name']
        customer_street = request.form['customer_street']
        customer_city = request.form['customer_city']
        customer_state = request.form['customer_state']
        customer_zip = request.form['customer_zip']
        favorite_employee = request.form['favorite_employee']
        
        query = "INSERT INTO Customers (customer_first_name, customer_last_name, customer_street, customer_city, customer_state, customer_zip, favorite_employee) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(customer_first_name, customer_last_name, customer_street, customer_city, customer_state, customer_zip, favorite_employee))
        results = cursor.fetchall()
        return redirect('/customers')

    return render_template("createCustomer.j2", Employees=Employees)


def get_customer(id):
    query = "SELECT customer_id, customer_first_name, customer_last_name, customer_street, customer_city, customer_state, customer_zip, favorite_employee FROM Customers WHERE customer_id =" + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    customer = cursor.fetchone()

    return customer

@app.route('/<int:id>/deleteCustomer', methods=('GET', 'POST'))
def deleteCustomer(id):
    customer = get_customer(id)
    
    query = "DELETE FROM Customers WHERE customer_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return redirect('/customers')


@app.route('/<int:id>/update-customer', methods=('GET', 'POST'))
def updateCustomer(id):

    customer = get_customer(id)

    if request.method == 'POST':
        customer_first_name = request.form['customer_first_name']
        customer_last_name = request.form['customer_last_name']
        customer_street = request.form['customer_street']
        customer_city = request.form['customer_city']
        customer_state = request.form['customer_state']
        customer_zip = request.form['customer_zip']
        favorite_employee = request.form['favorite_employee']
        
        query = "UPDATE Customers SET customer_first_name=%s, customer_last_name=%s, customer_street=%s, customer_city=%s, customer_state=%s, customer_zip=%s, favorite_employee=%s WHERE customer_id=" + str(id)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(customer_first_name, customer_last_name, customer_street, customer_city, customer_state, customer_zip, favorite_employee))
        results = cursor.fetchall()
        return redirect('/customers')

    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Employees = cursor.fetchall()


    return render_template("updateCustomer.j2", customer=customer, Employees=Employees)


# Vehicles
@app.route('/vehicles')
def Vehicles():
    query = "SELECT * FROM Vehicles;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("Vehicles.j2", Vehicles=results)

@app.route('/create-vehicle', methods=('GET', 'POST'))
def createVehicle():

    if request.method == 'POST':
        vin = request.form['vin']
        vehicle_type = request.form['vehicle_type']
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        color = request.form['color']
        msrp = request.form['msrp']

        if request.form.get("is_preowned") == None:
            is_preowned = 0
        else: 
            is_preowned = 1
        
        if request.form.get("is_for_sale") == None: 
            is_for_sale = 0
        else: 
            is_for_sale = 1

            
        query = "INSERT INTO Vehicles (vin, vehicle_type, make, model, year, color, is_preowned, is_for_sale, msrp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(vin, vehicle_type, make, model, year, color, is_preowned, is_for_sale, msrp))
        results = cursor.fetchall()
        return redirect('/vehicles')

    return render_template("createVehicle.j2")

def get_vehicle(id):

    query = "SELECT vin, vehicle_type, make, model, year, color, is_preowned, is_for_sale, msrp FROM Vehicles WHERE vin=" + ('"%s"' % id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    vehicle = cursor.fetchone()

    return vehicle

@app.route('/<string:id>/deleteVehicle', methods=('GET', 'POST'))
def deleteVehicle(id):

    vehicle = get_vehicle(id)

    query = "DELETE FROM Vehicles WHERE vin=" + ('"%s"' % id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return redirect('/vehicles')


@app.route('/<string:id>/update-vehicle', methods=('GET', 'POST'))
def updateVehicle(id):
    
    vehicle = get_vehicle(id)

    if request.method == 'POST':
        vehicle_type = request.form['vehicle_type']
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        color = request.form['color']
        msrp = request.form['msrp']

        if request.form.get("is_preowned") == None:
            is_preowned = 0
        else: 
            is_preowned = 1
        
        if request.form.get("is_for_sale") == None: 
            is_for_sale = 0
        else: 
            is_for_sale = 1
            
        query = "UPDATE Vehicles SET vehicle_type=%s, make=%s, model=%s, year=%s, color=%s, is_preowned=%s, is_for_sale=%s, msrp=%s WHERE vin=" + ('"{}"'.format(id))
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(vehicle_type, make, model, year, color, is_preowned, is_for_sale, msrp))
        results = cursor.fetchall()
        return redirect('/vehicles')


    return render_template("updateVehicle.j2", vehicle=vehicle)


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
    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Employees = cursor.fetchall()

    query = "SELECT * FROM Customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Customers = cursor.fetchall()


    return render_template("Employees_Customers_Map.j2", Employees=Employees, Customers=Customers)


# Listener 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8530))
    app.run(port=port, debug=True) 


