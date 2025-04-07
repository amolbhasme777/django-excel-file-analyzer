import pandas as pd
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import messages
from .models import FileUpload, UserData
from .forms import ExcelUploadForm
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import Count
from datetime import date

REQUIRED_COLUMNS = ['Sno', 'FirstName', 'LastName', 'Gender', 'DateofBirth']

def validate_excel(df):
    errors = []
    if list(df.columns) != REQUIRED_COLUMNS:
        return ["Invalid columns. Required: " + ", ".join(REQUIRED_COLUMNS)]
    
    seen = set()
    for i, row in df.iterrows():
        row_errors = []
        sno = str(row['Sno']).strip()
        fname = str(row['FirstName']).strip()
        lname = str(row['LastName']).strip()
        gender = row['Gender']
        dob = row['DateofBirth']
        
        if not sno:
            row_errors.append("Sno is empty")
        if not fname or len(fname) > 50:
            row_errors.append("Invalid FirstName")
        if not lname or len(lname) > 50:
            row_errors.append("Invalid LastName")
        if gender not in ['M', 'F', 'O']:
            row_errors.append("Invalid Gender")
        try:
            dob = pd.to_datetime(dob).date()
            if dob >= now().date():
                row_errors.append("DateofBirth must be in the past")
        except Exception:
            row_errors.append("Invalid DateofBirth format")

        unique_key = (sno, fname)
        if unique_key in seen:
            row_errors.append("Duplicate Sno + FirstName")
        seen.add(unique_key)

        if row_errors:
            errors.append(f"Row {i+2}: {', '.join(row_errors)}")
    return errors

def upload_file(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if not file.name.endswith('.xlsx'):
                messages.error(request, "Only .xlsx files are allowed")
                return redirect('upload')

            df = pd.read_excel(file)
            errors = validate_excel(df)

            if errors:
                return render(request, 'uploader/validation_errors.html', {'errors': errors})

            # Create new file upload entry
            upload = FileUpload.objects.create(file_name=file.name, row_count=len(df))

            for _, row in df.iterrows():
                sno = str(row['Sno']).strip()
                first_name = row['FirstName']
                last_name = row['LastName']
                gender = row['Gender']
                date_of_birth = pd.to_datetime(row['DateofBirth']).date()

                # Update if exists else create new
                UserData.objects.update_or_create(
                    sno=sno,
                    first_name=first_name,
                    last_name=last_name,
                    defaults={
                        'file': upload,
                        'gender': gender,
                        'date_of_birth': date_of_birth
                    }
                )

            messages.success(request, "File uploaded successfully. Existing records were updated where necessary.")
            return redirect('uploads')
    else:
        form = ExcelUploadForm()

    return render(request, 'uploader/upload.html', {'form': form})

def view_uploads(request):
    uploads = FileUpload.objects.all().order_by('-uploaded_at')
    return render(request, 'uploader/upload_list.html', {'uploads': uploads})

def view_upload_data(request, upload_id):
    data = UserData.objects.filter(file_id=upload_id).order_by('sno')
    paginator = Paginator(data, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'uploader/upload_data.html', {'page_obj': page_obj})

def dashboard(request):
    today = date.today()
    data = UserData.objects.all()
    age_gender = {'M': [], 'F': [], 'O': []}

    for user in data:
        age = today.year - user.date_of_birth.year - ((today.month, today.day) < (user.date_of_birth.month, user.date_of_birth.day))
        age_gender[user.gender].append(age)

    context = {
        'gender_counts': {g: len(ages) for g, ages in age_gender.items()}
    }
    return render(request, 'uploader/dashboard.html', context)