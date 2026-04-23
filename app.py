import csv
import os
from functools import wraps
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# Beginner-friendly defaults. Override these with environment variables in production.
USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "password")

# File paths for data
BASE_DIR = Path(__file__).resolve().parent
data_folder = BASE_DIR / "data"
patients_file = data_folder / "patients.csv"
doctors_file = data_folder / "doctors.csv"
test_results_file = data_folder / "test_result.csv"
blood_bank_file = data_folder / "blood_bank.csv"
prescription_file = data_folder / "prescription_data.csv"

# Ensure the data directory exists
data_folder.mkdir(exist_ok=True)

PATIENT_FIELDS = [
    "id",
    "name",
    "age",
    "gender",
    "address",
    "emergency_contact",
    "medical_conditions",
    "allergies",
    "blood_group",
    "doctor_allotted",
    "date_visited",
]

NAV_ITEMS = [
    ("dashboard", "Dashboard"),
    ("add_patient", "Add Patient"),
    ("get_patient_info", "Patient Info"),
    ("check_doctor_availability", "Doctor Availability"),
    ("get_test_results", "Test Results"),
    ("blood_bank", "Blood Bank"),
    ("get_prescription", "Prescription"),
]


@app.context_processor
def inject_navigation():
    return {"nav_items": NAV_ITEMS}


def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please log in to continue.", "error")
            return redirect(url_for("login"))
        return view_function(*args, **kwargs)

    return wrapper


def read_csv(file_path):
    """Read a CSV file and return rows as dictionaries."""
    if not file_path.exists():
        flash(f"Data file '{file_path.name}' was not found.", "error")
        return []

    with file_path.open(mode="r", newline="", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)


def append_csv_row(file_path, fieldnames, row):
    """Append a row and create the header if the CSV is empty."""
    file_exists = file_path.exists() and file_path.stat().st_size > 0

    with file_path.open(mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def search_csv(file_path, column, search_text):
    """Case-insensitive exact search for simple CSV lookup pages."""
    normalized_search = (search_text or "").strip().lower()
    return [
        row
        for row in read_csv(file_path)
        if row.get(column, "").strip().lower() == normalized_search
    ]


@app.route('/')
def home():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    patients = read_csv(patients_file)
    doctors = read_csv(doctors_file)
    test_results = read_csv(test_results_file)
    blood_bank_data = read_csv(blood_bank_file)

    stats = {
        "patients": len(patients),
        "doctors": len(doctors),
        "tests": len(test_results),
        "blood_groups": len(blood_bank_data),
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        recent_patients=patients[-4:],
        blood_bank_data=blood_bank_data,
    )


@app.route("/add_patient", methods=["GET", "POST"])
@login_required
def add_patient():
    if request.method == "POST":
        patient = {field: request.form.get(field, "").strip() for field in PATIENT_FIELDS}

        missing_fields = [field.replace("_", " ").title() for field, value in patient.items() if not value]
        if missing_fields:
            flash(f"Please fill: {', '.join(missing_fields)}.", "error")
            return render_template("add_patient.html"), 400

        existing_patient_ids = {row.get("id", "").strip() for row in read_csv(patients_file)}
        if patient["id"] in existing_patient_ids:
            flash(f'Patient ID "{patient["id"]}" already exists.', "error")
            return render_template("add_patient.html"), 400

        append_csv_row(patients_file, PATIENT_FIELDS, patient)
        flash(f'Patient "{patient["name"]}" added successfully.', "success")
        return redirect(url_for("add_patient"))

    return render_template("add_patient.html")


@app.route("/get_patient_info", methods=["GET", "POST"])
@login_required
def get_patient_info():
    patient_data = None
    if request.method == "POST":
        patient_name = request.form.get("patient_name", "")
        patient_data = search_csv(patients_file, "name", patient_name)
        if not patient_data:
            flash(f'Patient "{patient_name}" not found.', "error")

    return render_template("get_patient_info.html", patient_data=patient_data)


@app.route("/check_doctor_availability", methods=["GET", "POST"])
@login_required
def check_doctor_availability():
    doctor_data = None
    if request.method == "POST":
        doctor_name = request.form.get("doctor_name", "")
        doctor_data = search_csv(doctors_file, "name", doctor_name)
        if not doctor_data:
            flash(f'Doctor "{doctor_name}" not found.', "error")

    return render_template("check_doctor_availability.html", doctor_data=doctor_data)


@app.route("/get_test_results", methods=["GET", "POST"])
@login_required
def get_test_results():
    test_results_data = None
    if request.method == "POST":
        patient_name = request.form.get("patient_name", "")
        test_results_data = search_csv(test_results_file, "name", patient_name)
        if not test_results_data:
            flash(f'Test results not found for patient "{patient_name}".', "error")

    return render_template("get_test_results.html", test_results_data=test_results_data)


@app.route("/blood_bank")
@login_required
def blood_bank():
    blood_bank_data = read_csv(blood_bank_file)
    return render_template("blood_bank.html", blood_bank_data=blood_bank_data)


@app.route("/get_prescription", methods=["GET", "POST"])
@login_required
def get_prescription():
    prescription_data = None
    if request.method == "POST":
        patient_name = request.form.get("patient_name", "")
        prescription_data = search_csv(prescription_file, "name", patient_name)
        if not prescription_data:
            flash(f'Prescription not found for patient "{patient_name}".', "error")

    return render_template("get_prescription.html", prescription_data=prescription_data)


if __name__ == "__main__":
    app.run(debug=True)
