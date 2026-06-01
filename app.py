
from flask import Flask, render_template, request, redirect
import sqlite3
import re
import requests
from datetime import datetime

app = Flask(__name__)






# Create database table
def init_db():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            dob TEXT,
            email TEXT,
            glucose REAL,
            haemoglobin REAL,
            cholesterol REAL,
            remarks TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Home page
@app.route('/')
def index():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    conn.close()

    return render_template('index.html', patients=patients)

# Add patient

@app.route('/add', methods=['GET', 'POST'])
def add_patient():

    if request.method == 'POST':

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']

        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        # Email validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):
            return "Invalid Email Address"

        # Date validation
        today = datetime.today().date()
        birth_date = datetime.strptime(dob, "%Y-%m-%d").date()

        if birth_date > today:
            return "Date of birth cannot be future date"

        # Number validation
        if glucose < 0 or haemoglobin < 0 or cholesterol < 0:
            return "Blood values must be positive"

        # AI prediction
        remarks = predict_health(glucose, haemoglobin, cholesterol)

        conn = sqlite3.connect('patients.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO patients
            (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            full_name,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add.html')



# Edit patient
 
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']

        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        # Email validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):
            return "Invalid Email Address"

        # Date validation
        today = datetime.today().date()
        birth_date = datetime.strptime(dob, "%Y-%m-%d").date()

        if birth_date > today:
            return "Date of birth cannot be future date"

        # Number validation
        if glucose < 0 or haemoglobin < 0 or cholesterol < 0:
            return "Blood values must be positive"

        # AI Prediction
        remarks = predict_health(glucose, haemoglobin, cholesterol)

        cursor.execute('''
            UPDATE patients
            SET full_name=?,
                dob=?,
                email=?,
                glucose=?,
                haemoglobin=?,
                cholesterol=?,
                remarks=?
            WHERE id=?
        ''', (
            full_name,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks,
            id
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    cursor.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = cursor.fetchone()

    conn.close()

    return render_template('edit.html', patient=patient)



# Delete patient
@app.route('/delete/<int:id>')
def delete_patient(id):

    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')

# Prediction Function


def predict_health(glucose, haemoglobin, cholesterol):

    try:

        response = requests.get(
            "https://api.github.com"
        )

        if response.status_code == 200:

            if glucose > 200 and cholesterol > 240:
                return "High risk of diabetes and heart disease"

            elif haemoglobin < 10:
                return "Possible anaemia detected"

            elif cholesterol > 240:
                return "High cholesterol risk"

            else:
                return "Health condition appears normal"

        else:
            return "API connection failed"

    except Exception as e:
        print(e)
        return "Unable to connect to external API"

# Start app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

