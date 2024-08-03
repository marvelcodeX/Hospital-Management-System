from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Replace these with the actual username and password
USERNAME = "admin"
PASSWORD = "password"

# File paths for data
data_folder = os.path.join(os.path.dirname(__file__), 'data')
patients_file = os.path.join(data_folder, 'patients.csv')
doctors_file = os.path.join(data_folder, 'doctors.csv')
test_results_file = os.path.join(data_folder, 'test_results.csv')
blood_bank_file = os.path.join(data_folder, 'blood_bank.csv')
prescription_file = os.path.join(data_folder, 'prescription_data.csv')

# Ensure the data directory exists
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Function to read CSV file
def read_csv(file_path):
    if not os.path.exists(file_path):
        flash(f"File '{file_path}' not found.", 'error')
        return []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)
    return data

# Route to handle login
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

# Route for dashboard
@app.route('/dashboard')
def dashboard():
    logo_path = url_for('static', filename='images/logo.png')
    return render_template('dashboard.html',logo_path=logo_path)
    

# Route to add a new patient
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    avatar_path = url_for('static', filename='images/admin.png')
    if request.method == 'POST':
        # Handle form submission logic
        patient_id = request.form.get('id')
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        address = request.form.get('address')
        emergency_contact = request.form.get('emergency_contact')
        medical_conditions = request.form.get('medical_conditions')
        allergies = request.form.get('allergies')
        blood_group = request.form.get('blood_group')
        doctor_allotted = request.form.get('doctor_allotted')

        # Append new patient to CSV file
        with open(patients_file, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'name', 'age', 'gender', 'address', 'emergency_contact',
                          'medical_conditions', 'allergies', 'blood_group', 'doctor_allotted']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({
                'id': patient_id,
                'name': name,
                'age': age,
                'gender': gender,
                'address': address,
                'emergency_contact': emergency_contact,
                'medical_conditions': medical_conditions,
                'allergies': allergies,
                'blood_group': blood_group,
                'doctor_allotted': doctor_allotted
            })
        
        flash(f'Patient "{name}" added successfully.', 'success')

        return redirect(url_for('add_patient',avatar_path=avatar_path))
    
    return render_template('add_patient.html')

# Route to get patient information
@app.route('/get_patient_info', methods=['GET', 'POST'])
def get_patient_info():
    avatar_path = url_for('static', filename='images/admin.png')
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        patient_data = [row for row in read_csv(patients_file) if row.get('name') == patient_name]
        if not patient_data:
            flash(f'Patient "{patient_name}" not found.', 'error')
        return render_template('get_patient_info.html', patient_data=patient_data,avatar_path=avatar_path)
    return render_template('get_patient_info.html')

# Route to check doctor availability
@app.route('/check_doctor_availability', methods=['GET', 'POST'])
def check_doctor_availability():
    avatar_path = url_for('static', filename='images/admin.png')
    if request.method == 'POST':
        doctor_name = request.form.get('doctor_name')
        doctor_data = [row for row in read_csv(doctors_file) if row.get('name') == doctor_name]
        if not doctor_data:
            flash(f'Doctor "{doctor_name}" not found.', 'error')
        return render_template('check_doctor_availability.html', doctor_data=doctor_data,avatar_path=avatar_path)
    return render_template('check_doctor_availability.html')

# Route to get test results
@app.route('/get_test_results', methods=['GET', 'POST'])
def get_test_results():
    avatar_path = url_for('static', filename='images/admin.png')
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        test_results_data = [row for row in read_csv(test_results_file) if row.get('name') == patient_name]
        if not test_results_data:
            flash(f'Test results not found for patient "{patient_name}".', 'error')
        return render_template('get_test_results.html', test_results_data=test_results_data,avatar_path=avatar_path)
    return render_template('get_test_results.html')

# Route to display blood bank information
@app.route('/blood_bank')
def blood_bank():
    avatar_path = url_for('static', filename='images/admin.png')
    blood_bank_data = read_csv(blood_bank_file)
    return render_template('blood_bank.html', blood_bank_data=blood_bank_data,avatar_path=avatar_path)

# Route to get prescription information
@app.route('/get_prescription', methods=['GET', 'POST'])
def get_prescription():
    avatar_path = url_for('static', filename='images/admin.png')
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        prescription_data = [row for row in read_csv(prescription_file) if row.get('name') == patient_name]
        if not prescription_data:
            flash(f'Prescription not found for patient "{patient_name}".', 'error')
        return render_template('get_prescription.html', prescription_data=prescription_data,avatar_path=avatar_path)
    return render_template('get_prescription.html')

if __name__ == '__main__':
    app.run(debug=True)
