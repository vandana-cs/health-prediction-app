
from flask import Flask, render_template, request, redirect
import sqlite3
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def call_ai_api(prompt):

    import requests
    import os

    API_KEY = os.getenv("HF_API_KEY")

    url = "https://api-inference.huggingface.co/models/google/flan-t5-base"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    return requests.post(
        url,
        headers=headers,
        json={"inputs": prompt},
        timeout=5
    )




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
            flash("Invalid Email Address")
            return redirect('/add')
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


import os
import requests

API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def fallback_health(glucose, haemoglobin, cholesterol):

    if glucose > 200 and cholesterol > 240:
        return "High risk of diabetes and heart disease"

    elif haemoglobin < 10:
        return "Possible anaemia detected"

    elif cholesterol > 240:
        return "High cholesterol risk"

    else:
        return "Health condition appears normal"


def predict_health(glucose, haemoglobin, cholesterol):

    prompt = f"""
    Analyze the following patient medical report and provide a short health risk summary.

    Glucose: {glucose}
    Haemoglobin: {haemoglobin}
    Cholesterol: {cholesterol}
    """

    try:

        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=10
        )

        data = response.json()

        # Hugging Face successful response
        if isinstance(data, list):

            if "generated_text" in data[0]:
                return data[0]["generated_text"]

        # fallback if API format changes
        return fallback_health(glucose, haemoglobin, cholesterol)

    except Exception:
        # fallback if no internet / API failure
        return fallback_health(glucose, haemoglobin, cholesterol)
# Start app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

