
from django.contrib import admin
from django.urls import path, include

from accounts.views import (
    login_view,
    admin_dashboard,
    manager_dashboard,
    salesman_dashboard,
    logout_view,
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Login
    path('', login_view, name='login'),

    # Accounts: backup and other account URLs
    path('accounts/', include('accounts.urls')),

    # Inventory Management
    path('inventory/', include('inventory.urls')),

    # Role-Based Dashboards
    path(
        'admin-dashboard/',
        admin_dashboard,
        name='admin_dashboard',
    ),
    path(
        'manager-dashboard/',
        manager_dashboard,
        name='manager_dashboard',
    ),
    path(
        'salesman-dashboard/',
        salesman_dashboard,
        name='salesman_dashboard',
    ),

    # Logout
    path('logout/', logout_view, name='logout'),
]
