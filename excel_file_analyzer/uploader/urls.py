from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload'),
    path('uploads/', views.view_uploads, name='uploads'),
    path('uploads/<int:upload_id>/', views.view_upload_data, name='upload_data'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
