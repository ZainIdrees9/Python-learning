
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Admin Database Backup Page
    path(
        'admin-backup/',
        views.admin_backup,
        name='admin_backup_page'
    ),

    # Admin Database Backup / Download
    path(
        'admin-backup/download/',
        views.admin_backup,
        name='admin_backup'
    ),
]
