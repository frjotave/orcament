from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            port=7306,

            database="rack_management"
        )
        print("Database connection successful.")
        if connection is not None:
            print("Connection object is valid.")

        print(f"Connected to database: {database}")

    except Error as e:
        print(f"The error '{e}' occurred")
    if connection is None:
        print("Connection object is None.")
        raise Exception("Database connection failed.")


        raise Exception("Database connection failed.")
    return connection

db = create_connection()

app = Flask(__name__)

@app.route('/')
def index():
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM equipment")
        equipments = cursor.fetchall()
        total_value = sum(equipment['quantity'] * equipment['value'] for equipment in equipments)
    return render_template('index.html', equipments=equipments, total_value=total_value)

@app.route('/add', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':
        equipment = {
            'name': request.form['name'],
            'description': request.form['description'],
            'model': request.form['model'],
            'quantity': int(request.form['quantity']),
            'unit': request.form['unit'],
            'value': float(request.form['value']),
            'research_link': request.form['research_link']
        }
        with db.cursor() as cursor:
            cursor.execute("INSERT INTO equipment (name, description, model, quantity, unit, value, research_link) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                           (equipment['name'], equipment['description'], equipment['model'], equipment['quantity'], equipment['unit'], equipment['value'], equipment['research_link']))
            db.commit()
        return redirect(url_for('index'))
    return render_template('add_equipment.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):
    with db.cursor(dictionary=True) as cursor:
        if request.method == 'POST':
            equipment = {
                'name': request.form['name'],
                'description': request.form['description'],
                'model': request.form['model'],
                'quantity': int(request.form['quantity']),
                'unit': request.form['unit'],
                'value': float(request.form['value']),
                'research_link': request.form['research_link']
            }
            cursor.execute("UPDATE equipment SET name = %s, description = %s, model = %s, quantity = %s, unit = %s, value = %s, research_link = %s WHERE id = %s",
                           (equipment['name'], equipment['description'], equipment['model'], equipment['quantity'], equipment['unit'], equipment['value'], equipment['research_link'], id))
            db.commit()
            return redirect(url_for('index'))
        cursor.execute("SELECT * FROM equipment WHERE id = %s", (id,))
        equipment = cursor.fetchone()
    return render_template('edit_equipment.html', equipment=equipment)

@app.route('/delete/<int:id>')
def delete_equipment(id):
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM equipment WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)
