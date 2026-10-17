# ============================================================
#   - User login and logout
#   - Role-based dashboard access
#   - Admin dashboard statistics
#   - Monthly sales chart data
#   - Low-stock product filtering (5 or fewer)
#   - Recent sales
#   - MySQL database backup and download
# ============================================================
from django.db.models import Sum, Func, IntegerField
import calendar
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from inventory.models import Product, Sale, Customer, Supplier


# Support a custom Django user model.
User = get_user_model()


# ============================================================
# ROLE CHECKS
# ============================================================

def is_admin(user):
    """Check whether the user has the ADMIN role."""
    return user.is_authenticated and getattr(user, "role", None) == "ADMIN"


def is_manager(user):
    """Check whether the user has the MANAGER role."""
    return user.is_authenticated and getattr(user, "role", None) == "MANAGER"


def is_salesman(user):
    """Check whether the user has the SALESMAN role."""
    return user.is_authenticated and getattr(user, "role", None) == "SALESMAN"


# ============================================================
# ROLE-BASED REDIRECTION
# ============================================================

def redirect_by_role(user):
    """Redirect an authenticated user to their role dashboard."""

    role = getattr(user, "role", None)

    if role == "ADMIN":
        return redirect("admin_dashboard")

    if role == "MANAGER":
        return redirect("manager_dashboard")

    if role == "SALESMAN":
        return redirect("salesman_dashboard")

    # Unknown or unsupported role.
    return redirect("login")


# ============================================================
# LOGIN
# ============================================================

def login_view(request):
    """
    Authenticate a user and redirect according to their role.

    Expected POST fields:
        username
        password
    """

    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    error_message = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            error_message = "Invalid username or password."

        elif getattr(user, "role", None) not in (
            "ADMIN",
            "MANAGER",
            "SALESMAN",
        ):
            error_message = "Your account does not have a valid role."

        else:
            login(request, user)
            return redirect_by_role(user)

    return render(
        request,
        "accounts/login.html",
        {"error_message": error_message},
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required
def logout_view(request):
    """Log out the current user."""
    logout(request)
    return redirect("login")


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Calculate admin dashboard statistics and monthly sales data."""

    # Current local calendar year.
    current_year = timezone.localdate().year

    # --------------------------------------------------------
    # Product statistics
    # --------------------------------------------------------

    total_products = Product.objects.count()

    available_stock = (
        Product.objects.aggregate(
            total=Sum("CurrentStock")
        )["total"] or 0
    )

    # --------------------------------------------------------
    # Sales statistics
    # --------------------------------------------------------

    total_sales = (
        Sale.objects.aggregate(
            total=Sum("TotalAmount")
        )["total"] or Decimal("0.00")
    )

    # --------------------------------------------------------
    # Customer, supplier, and user statistics
    # --------------------------------------------------------

    total_users = User.objects.count()
    total_customers = Customer.objects.count()
    total_suppliers = Supplier.objects.count()

    # --------------------------------------------------------
    # Low-stock products
    # Show products whose stock is 5 or less.
    # --------------------------------------------------------

    low_stock_products = (
        Product.objects
        .filter(CurrentStock__lte=5)
        .order_by("CurrentStock")[:10]
    )

    # --------------------------------------------------------
    # Recent sales
    # Show the 10 most recent sales.
    # --------------------------------------------------------

    recent_sales = (
        Sale.objects
        .select_related("Customer")
        .order_by("-SaleDate")[:3]
    )

 
    # --------------------------------------------------------
    # Monthly sales chart
    # Uses MySQL YEAR() and MONTH() functions directly.
    # --------------------------------------------------------

    month_labels = list(calendar.month_name)[1:]
    monthly_sales_values = [0.0] * 12

    class MySQLMonth(Func):
        function = "MONTH"
        output_field = IntegerField()

    class MySQLYear(Func):
        function = "YEAR"
        output_field = IntegerField()

    monthly_sales = (
        Sale.objects
        .annotate(
            sale_year=MySQLYear("SaleDate"),
            month_number=MySQLMonth("SaleDate"),
        )
        .filter(sale_year=current_year)
        .values("month_number")
        .annotate(monthly_total=Sum("TotalAmount"))
        .order_by("month_number")
    )

    for item in monthly_sales:
        month_number = item["month_number"]
        monthly_total = item["monthly_total"] or 0

        if month_number is not None and 1 <= month_number <= 12:
            monthly_sales_values[month_number - 1] = float(monthly_total)

    print("Dashboard chart year:", current_year)
    print("Dashboard chart values:", monthly_sales_values)


    # --------------------------------------------------------
    # Dashboard template context
    # --------------------------------------------------------

    context = {
        "total_products": total_products,
        "available_stock": available_stock,
        "total_sales": total_sales,
        "total_users": total_users,
        "total_customers": total_customers,
        "total_suppliers": total_suppliers,
        "low_stock_products": low_stock_products,
        "recent_sales": recent_sales,
        "current_year": current_year,
        "month_labels": month_labels,
        "monthly_sales_values": monthly_sales_values,
    }

    return render(
        request,
        "accounts/admin_dashboard.html",
        context,
    )


# ============================================================
# MANAGER DASHBOARD
# ============================================================

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    """Display the manager dashboard to managers only."""

    return render(
        request,
        "accounts/manager_dashboard.html",
    )


# ============================================================
# SALESMAN DASHBOARD
# ============================================================

@login_required
@user_passes_test(is_salesman)
def salesman_dashboard(request):
    """Display the salesman dashboard to salesmen only."""

    return render(
        request,
        "accounts/salesman_dashboard.html",
    )


# ============================================================
# DATABASE BACKUP
# ============================================================

@login_required
@user_passes_test(is_admin)
def admin_backup(request):
    """
    GET:
        Display the backup page.

    POST:
        Create a MySQL SQL backup and download it.
    """

    if request.method != "POST":
        return render(
            request,
            "accounts/admin_backup.html",
        )

    database_config = settings.DATABASES["default"]

    # This backup implementation supports MySQL only.
    if database_config.get("ENGINE") != "django.db.backends.mysql":
        messages.error(
            request,
            "Database backup is configured for MySQL databases only.",
        )
        return redirect("accounts:admin_backup_page")

    # First, search for mysqldump in the system PATH.
    mysqldump = shutil.which("mysqldump")

    # Check common Windows MySQL installation locations.
    if not mysqldump:
        possible_paths = [
            r"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqldump.exe",
            r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
            r"C:\xampp\mysql\bin\mysqldump.exe",
            r"C:\laragon\bin\mysql\mysql-8.0\bin\mysqldump.exe",
        ]

        mysqldump = next(
            (
                path for path in possible_paths
                if Path(path).is_file()
            ),
            None,
        )

    if not mysqldump:
        messages.error(
            request,
            "mysqldump was not found. Add the MySQL bin directory to PATH.",
        )
        return redirect("accounts:admin_backup_page")

    # Database connection settings.
    database_name = database_config["NAME"]
    database_user = database_config["USER"]
    database_password = database_config.get("PASSWORD", "")
    database_host = database_config.get("HOST") or "localhost"
    database_port = str(database_config.get("PORT") or "3306")

    # Create a backups directory in the project folder.
    backup_directory = Path(settings.BASE_DIR) / "backups"
    backup_directory.mkdir(parents=True, exist_ok=True)

    # Create a unique backup filename.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{database_name}_{timestamp}.sql"
    backup_path = backup_directory / backup_filename

    # Construct the mysqldump command.
    command = [
        mysqldump,
        "--host", database_host,
        "--port", database_port,
        "--user", database_user,
        "--result-file", str(backup_path),
        database_name,
    ]

    try:
        # Pass the password through the environment rather than
        # placing it directly in the command arguments.
        environment = os.environ.copy()

        if database_password:
            environment["MYSQL_PWD"] = database_password

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            env=environment,
        )

        # Handle backup errors.
        if result.returncode != 0:
            backup_path.unlink(missing_ok=True)

            # Technical details go to the development terminal.
            print("mysqldump error:", result.stderr)

            messages.error(
                request,
                "Backup failed. Check MySQL credentials and permissions.",
            )
            return redirect("accounts:admin_backup_page")

        # Send the SQL backup to the browser.
        return FileResponse(
            open(backup_path, "rb"),
            as_attachment=True,
            filename=backup_filename,
            content_type="application/sql",
        )

    except (OSError, subprocess.SubprocessError) as error:
        # Remove any incomplete backup.
        backup_path.unlink(missing_ok=True)

        print("Database backup error:", error)

        messages.error(
            request,
            "An error occurred while creating the database backup.",
        )
        return redirect("accounts:admin_backup_page")