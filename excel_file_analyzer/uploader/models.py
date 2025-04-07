from django.db import models

# Create your models here.
from django.db import models

class FileUpload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    row_count = models.IntegerField()

class UserData(models.Model):
    file = models.ForeignKey(FileUpload, on_delete=models.CASCADE)
    sno = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    date_of_birth = models.DateField()

    class Meta:
        unique_together = ('sno', 'first_name')
