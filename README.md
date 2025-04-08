# 📊 Django Excel File Analyzer

This is a Django-based web application that allows users to upload Excel files, validate their contents, store validated records into the database, and visualize uploaded data in a responsive dashboard with Material UI components.

---

## 🚀 Features

- ✅ Upload `.xlsx` Excel files
- 🧪 Validate data with custom business rules
- 🛑 View and download detailed error reports
- 🗃️ Store validated data in a relational database
- 📈 Dashboard showing gender distribution
- 📄 View list of uploaded files and associated records
- 🎨 Material UI responsive design with collapsible sidebar and top navigation

---

## Technologies Used
- Python 3.10+
- Django 5.2+
- Pandas (for Excel parsing & validation)
- SQLite (default DB)
- Materialize CSS (Material UI frontend framework)
- JavaScript (for toggle sidebar behavior)

## 📦 Project Structure

templates/ ├── base.html ├── header.html ├── sidebar.html └── uploader/ ├── upload.html ├── upload_list.html ├── upload_data.html ├── validation_errors.html └── dashboard.html

uploader/ ├── models.py ├── views.py ├── forms.py ├── urls.py └── static/ └── (Materialize CSS & custom styles)


---

## ✅ Data Validation Rules

### Required Columns:
- `Sno` (string, unique with FirstName)
- `FirstName` (string, required, max 50)
- `LastName` (string, required, max 50)
- `Gender` (must be 'M', 'F', or 'O')
- `DateofBirth` (format: YYYY-MM-DD, must be past date)

### Constraints:
- Combination of `Sno` + `FirstName` must be unique
- On re-upload, if duplicate found → update instead of insert

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

git clone https://github.com/your-username/django-excel-file-analyzer.git
cd django-excel-file-analyzer

### 2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Apply Migrations
python manage.py makemigrations
python manage.py migrate

### 5. Run The Server
python manage.py runserver

Visit: http://127.0.0.1:8000/

## Upload File Sample Format
Ensure Excel file has these exact columns:

Sno	FirstName	LastName	Gender	DateofBirth
001	Alice	Smith	F	1990-05-12
002	Bob	Johnson	M	1985-11-23

## UI Features
Collapsible sidebar (hidden by default on small screens)
Material UI styling via Materialize CSS
Sidebar navigation links:
Upload Excel
View Uploads
Dashboard
Right-aligned avatar/user icon in header

## File Upload Flow
Upload .xlsx file.
Backend validates every row.
If errors → show them in table with row/column info & download error report.
If valid → data is inserted (or updated if already exists).
User is redirected to upload list.

## Dashboard
Gender-wise user count visualization
Age calculation based on Date of Birth

## Error Handling
Custom error messages rendered for:
Missing or invalid columns
Validation rule violations
File format issues
Downloadable validation error report
Safe handling of unique constraint violations

## Developer
Amol Bhasme
Python Full Stack Developer | Workflow Automation | Django + React Developer
