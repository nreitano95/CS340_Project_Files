from flask import Flask, render_template, json

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
    return render_template("Employees.j2")

@app.route('/create-employee')
def createEmployee():
    return render_template("createEmployee.j2")

@app.route('/update-employee')
def updateEmployee():
    return render_template("updateEmployee.j2")


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
    port = int(os.environ.get('PORT', 8531))
    app.run(port=port, debug=True) 


