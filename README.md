# Hospital Management System

A beginner-friendly Flask web app for managing basic hospital records with CSV files. It includes an admin login, dashboard, patient registration, patient lookup, doctor availability, test results, prescriptions, and blood bank stock.

## Features

- Clean responsive dashboard with quick hospital stats.
- Add new patient records to `data/patients.csv`.
- Search patients, doctors, test results, and prescriptions by name.
- View blood bank inventory from `data/blood_bank.csv`.
- Simple session-based admin login and logout.
- CSV storage, so no database setup is required.

## Tech Stack

- Python 3
- Flask
- HTML templates with Jinja
- CSS
- CSV files for data storage

## Project Structure

```text
Hospital-Management-System/
├── app.py
├── data/
│   ├── blood_bank.csv
│   ├── doctors.csv
│   ├── patients.csv
│   ├── prescription_data.csv
│   └── test_result.csv
├── static/
│   ├── images/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── ...
├── requirements.txt
└── README.md
```

## Getting Started

1. Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Run the app.

```bash
python app.py
```

4. Open the app in your browser.

```text
http://127.0.0.1:5000
```

## Demo Login

```text
Username: admin
Password: password
```

You can override these values with environment variables:

```bash
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD="strong-password"
export SECRET_KEY="change-this-secret"
```

## CSV Data

The app reads and writes CSV files from the `data/` folder. Keep the header row in each CSV file because the Flask routes use those column names.

## Future Improvements

- Add edit and delete actions for patients.
- Add form validation with better error messages.
- Replace CSV files with SQLite when learning databases.
- Add automated tests for routes and CSV helpers.
- Add user roles for admin, receptionist, and doctor.
