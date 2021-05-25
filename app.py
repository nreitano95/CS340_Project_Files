from flask import Flask, render_template, json, request, redirect, flash

import database.db_connector as db

import os

import MySQLdb

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
    searchTerm = request.args.get('searchTerm')

    query = "SELECT * FROM Employees ORDER BY last_name;"
    if searchTerm:
        query = f'SELECT * FROM Employees WHERE first_name LIKE "%%{searchTerm}%%" OR last_name LIKE "%%{searchTerm}%%" ORDER BY last_name;'

    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    cursor.close()
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
    cursor.close()

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
    query = "SELECT * FROM Customers ORDER BY customer_last_name;"

    searchTerm = request.args.get('searchTerm')
    if searchTerm:
        query = f'SELECT * FROM Customers WHERE customer_first_name LIKE "%%{searchTerm}%%" OR customer_last_name LIKE "%%{searchTerm}%%" ORDER BY customer_last_name;'

    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    cursor.close()

    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Employees = cursor.fetchall()
    cursor.close()

    return render_template("Customers.j2", Customers=results, Employees=Employees)


@app.route('/create-customer', methods=('GET', 'POST'))
def createCustomer():
    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Employees = cursor.fetchall()
    cursor.close()


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
    cursor.close()

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
    cursor.close()

    return render_template("updateCustomer.j2", customer=customer, Employees=Employees)


# Vehicles
@app.route('/vehicles')
def Vehicles():
    query = "SELECT * FROM Vehicles ORDER BY make;"
    searchTerm = request.args.get('searchTerm')
    if searchTerm:
        query = f'SELECT * FROM Vehicles WHERE vehicle_type LIKE "%%{searchTerm}%%" OR make LIKE "%%{searchTerm}%%" OR model LIKE "%%{searchTerm}%%" or year LIKE "%%{searchTerm}%%" ORDER BY make;'

    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    cursor.close()

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
    cursor.close()

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
    query = "SELECT * FROM Sales;"
    searchTerm = request.args.get('searchTerm')
    if searchTerm:
        query = f'SELECT * FROM Sales WHERE vin LIKE "%%{searchTerm}%%";'
        
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    cursor.close()

    return render_template("Sales.j2", Sales=results)

@app.route('/create-sale', methods=('GET', 'POST'))
def createSale():

    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Employees = cursor.fetchall()
    cursor.close()

    query = "SELECT * FROM Customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Customers = cursor.fetchall()
    cursor.close()

    query = "SELECT * FROM Vehicles;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Vehicles = cursor.fetchall()
    cursor.close()


    if request.method == 'POST':
        
        employee = request.form['employee']
        customer = request.form['customer']
        vehicle = request.form['vehicle']
        sale_price = request.form['sale_price']
        sale_date = request.form['sale_date']
        if request.form.get("has_customer_paid") == None:
            has_customer_paid = 0
        else: 
            has_customer_paid = 1

        # Get the VIN based on dropdown input
        query = "SELECT * FROM Vehicles WHERE vin=" + ('"{}"'.format(vehicle))
        cursor = db.execute_query(db_connection=db_connection, query=query)
        vin = cursor.fetchone()

        vin = vin['vin']

        cursor.close()

        # Get the employee_id based on dropdown input
        query = "SELECT * FROM Employees WHERE employee_id=" + employee
        cursor = db.execute_query(db_connection=db_connection, query=query)
        employee_id = cursor.fetchone()

        employee_id = employee_id['employee_id']

        cursor.close()

        # Get the customer_id based on dropdown input
        query = "SELECT * FROM Customers WHERE customer_id=" + customer
        cursor = db.execute_query(db_connection=db_connection, query=query)
        customer_id = cursor.fetchone()
        
        customer_id = customer_id['customer_id']

        cursor.close()

        try: 
            # Get the employee_customer_id based on employee and customer dropdown
            query = "SELECT * FROM Employees_Customers_Map WHERE employee_id = " + str(employee_id) + " AND customer_id = " + str(customer_id)
            cursor = db.execute_query(db_connection=db_connection, query=query)
            employee_customer_id = cursor.fetchone()

            employee_customer_id = employee_customer_id['employee_customer_id']

            cursor.close()

        except: 
            query = "INSERT INTO Employees_Customers_Map (employee_id, customer_id) VALUES (%s, %s)"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(employee_id, customer_id))
            results = cursor.fetchall()

            # Get the employee_customer_id based on employee and customer dropdown
            query = "SELECT * FROM Employees_Customers_Map WHERE employee_id = " + str(employee_id) + " AND customer_id = " + str(customer_id)
            cursor = db.execute_query(db_connection=db_connection, query=query)
            employee_customer_id = cursor.fetchone()

            employee_customer_id = employee_customer_id['employee_customer_id']

            cursor.close()

        
        # Add the sale with form inputs
        query = "INSERT INTO Sales (vin, employee_customer_id, sale_price, sale_date, has_customer_paid) VALUES (%s, %s, %s, %s, %s)"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(vin, employee_customer_id, sale_price, sale_date, has_customer_paid))
        results = cursor.fetchall()

        return redirect('/sales')

    return render_template("createSale.j2", Employees=Employees, Customers=Customers, Vehicles=Vehicles)


def get_sale(id):

    query = "SELECT sale_id, vin, employee_customer_id, sale_price, sale_date, has_customer_paid FROM Sales WHERE sale_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    sale = cursor.fetchone()
    cursor.close()

    return sale

@app.route('/<int:id>/deleteSale', methods=('GET', 'POST'))
def deleteSale(id):

    sale = get_sale(id)

    query = "DELETE FROM Sales WHERE sale_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return redirect('/sales')


@app.route('/<int:id>/update-sale', methods=('GET', 'POST'))
def updateSale(id):

    sale = get_sale(id)

    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Employees = cursor.fetchall()
    cursor.close()

    query = "SELECT * FROM Customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Customers = cursor.fetchall()
    cursor.close()

    query = "SELECT * FROM Vehicles;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Vehicles = cursor.fetchall()
    cursor.close()


    if request.method == 'POST':
        
        employee = request.form['employee']
        customer = request.form['customer']
        vehicle = request.form['vehicle']
        sale_price = request.form['sale_price']
        sale_date = request.form['sale_date']
        if request.form.get("has_customer_paid") == None:
            has_customer_paid = 0
        else: 
            has_customer_paid = 1

        # Get the VIN based on dropdown input
        query = "SELECT * FROM Vehicles WHERE vin=" + ('"{}"'.format(vehicle))
        cursor = db.execute_query(db_connection=db_connection, query=query)
        vin = cursor.fetchone()

        vin = vin['vin']

        cursor.close()

        # Get the employee_id based on dropdown input
        query = "SELECT * FROM Employees WHERE employee_id=" + employee
        cursor = db.execute_query(db_connection=db_connection, query=query)
        employee_id = cursor.fetchone()

        employee_id = employee_id['employee_id']

        cursor.close()

        # Get the customer_id based on dropdown input
        query = "SELECT * FROM Customers WHERE customer_id=" + customer
        cursor = db.execute_query(db_connection=db_connection, query=query)
        customer_id = cursor.fetchone()
        
        customer_id = customer_id['customer_id']

        cursor.close()

        try:
            # Get the employee_customer_id based on employee and customer dropdown
            query = "SELECT * FROM Employees_Customers_Map WHERE employee_id = " + str(employee_id) + " AND customer_id = " + str(customer_id)
            cursor = db.execute_query(db_connection=db_connection, query=query)
            employee_customer_id = cursor.fetchone()

            employee_customer_id = employee_customer_id['employee_customer_id']

            cursor.close()
            
        except: 
            query = "INSERT INTO Employees_Customers_Map (employee_id, customer_id) VALUES (%s, %s)"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(employee_id, customer_id))
            results = cursor.fetchall()

            # Get the employee_customer_id based on employee and customer dropdown
            query = "SELECT * FROM Employees_Customers_Map WHERE employee_id = " + str(employee_id) + " AND customer_id = " + str(customer_id)
            cursor = db.execute_query(db_connection=db_connection, query=query)
            employee_customer_id = cursor.fetchone()

            employee_customer_id = employee_customer_id['employee_customer_id']

            cursor.close()
        
        query = "UPDATE Sales SET vin=%s, employee_customer_id=%s, sale_price=%s, sale_date=%s, has_customer_paid=%s WHERE sale_id = " + str(id)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(vin, employee_customer_id, sale_price, sale_date, has_customer_paid))
        results = cursor.fetchall()

        return redirect('/sales')

    return render_template("updateSale.j2", Employees=Employees, Customers=Customers, Vehicles=Vehicles, sale=sale)


# Employees_Customers_Map (Assign Salesperson)
@app.route('/assign-salesperson', methods=('GET', 'POST'))
def Employees_Customers_Map():
    query = "SELECT * FROM Employees;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Employees = cursor.fetchall()
    cursor.close()

    query = "SELECT * FROM Customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    Customers = cursor.fetchall()
    cursor.close()

    query = "SELECT * FROM Employees_Customers_Map;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    cursor.close()


    if request.method == 'POST':
        employee_id = request.form['employee_id']
        customer_id = request.form['customer_id']

        query = "INSERT INTO Employees_Customers_Map (employee_id, customer_id) VALUES (%s, %s)"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(employee_id, customer_id))
        results = cursor.fetchall()
        
        return redirect('/assign-salesperson')

    return render_template("Employees_Customers_Map.j2", Employees=Employees, Customers=Customers, Employees_Customers_Map=results)

def get_employee_customer(id):

    query = "SELECT * FROM Employees_Customers_Map WHERE employee_customer_id =" + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    employee_customer = cursor.fetchone()
    cursor.close()

    return employee_customer

@app.route('/<int:id>/deleteEmployeeCustomer', methods=('GET', 'POST'))
def deleteEmployeeCustomer(id):

    employee_customer = get_employee_customer(id)

    query = "DELETE FROM Employees_Customers_Map WHERE employee_customer_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    return redirect('/assign-salesperson')

# Listener 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8534))
    app.run(port=port, debug=True) 


