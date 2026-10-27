
# ============================================================
# ACCOUNTS VIEWS
# Web-based Stock, Inventory and Sales Management System
#
# Features:
# - User login, signup and logout
# - Role-based dashboard access
# - Admin dashboard statistics and charts
# - Manager dashboard statistics and charts
# - Salesman dashboard statistics
# - Low-stock product filtering
# - Recent sales
# - Admin creates Manager and Salesman accounts
# - MySQL database backup and download
#
# Date handling:
# - Uses MySQL YEAR() and MONTH() for monthly sales charts
# - Uses datetime ranges instead of SaleDate__date
# - Does not use TruncMonth(), TruncDate(), or other Trunc functions
# ============================================================

import json
import calendar
import os
import shutil
import subprocess

from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import DecimalField, ExpressionWrapper, F, Func, IntegerField, Sum
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from inventory.models import (
    Product,
    Sale,
    Customer,
    Supplier,
    StockEntryDetail,
    SaleDetail,
)

User = get_user_model()


# ============================================================
# MYSQL DATE FUNCTIONS
# ============================================================

class MySQLMonth(Func):
    function = "MONTH"
    output_field = IntegerField()


class MySQLYear(Func):
    function = "YEAR"
    output_field = IntegerField()


# ============================================================
# ROLE CHECKS
# ============================================================

def is_admin(user):
    return (
        user.is_authenticated
        and getattr(user, "role", None) == "ADMIN"
    )


def is_manager(user):
    return (
        user.is_authenticated
        and getattr(user, "role", None) == "MANAGER"
    )


def is_salesman(user):
    return (
        user.is_authenticated
        and getattr(user, "role", None) == "SALESMAN"
    )


# ============================================================
# ROLE-BASED REDIRECTION
# ============================================================

def redirect_by_role(user):
    role = getattr(user, "role", None)

    if role == "ADMIN":
        return redirect("admin_dashboard")

    if role == "MANAGER":
        return redirect("manager_dashboard")

    if role == "SALESMAN":
        return redirect("salesman_dashboard")

    return redirect("login")


# ============================================================
# DATETIME HELPERS
# ============================================================

def get_local_day_range(day):
    """
    Return the start and end-exclusive datetime values for a local day.

    This avoids SaleDate__date, which can trigger date truncation
    and timezone conversion in some database configurations.
    """

    start = datetime.combine(day, datetime.min.time())
    end = datetime.combine(day + timedelta(days=1), datetime.min.time())

    if settings.USE_TZ:
        start = timezone.make_aware(start, timezone.get_current_timezone())
        end = timezone.make_aware(end, timezone.get_current_timezone())

    return start, end


# ============================================================
# MONTHLY SALES CHART HELPER
# ============================================================

def get_monthly_sales_data(current_year):
    """
    Return Jan-Dec labels and monthly sales totals for the selected year.

    Uses MySQL YEAR() and MONTH() instead of TruncMonth().
    """

    month_labels = list(calendar.month_abbr)[1:]
    monthly_sales_values = [0.0] * 12

    monthly_sales = (
        Sale.objects
        .annotate(
            sale_year=MySQLYear(F("SaleDate")),
            sale_month=MySQLMonth(F("SaleDate")),
        )
        .filter(sale_year=current_year)
        .values("sale_month")
        .annotate(monthly_total=Sum("TotalAmount"))
        .order_by("sale_month")
    )

    for item in monthly_sales:
        month_number = item["sale_month"]

        if month_number is not None and 1 <= month_number <= 12:
            monthly_sales_values[month_number - 1] = float(
                item["monthly_total"] or 0
            )

    return month_labels, monthly_sales_values


# ============================================================
# LOGIN AND SIGNUP
# ============================================================

def login_view(request):
    """
    Supports:
    - GET ?show_signup=1
    - POST action=login
    - POST action=signup

    Public signup permits Manager and Salesman accounts only.
    """

    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    error_message = None
    show_signup = request.GET.get("show_signup") == "1"

    if request.method == "POST":
        action = request.POST.get("action", "login").strip().lower()

        # ----------------------------------------------------
        # SIGNUP
        # ----------------------------------------------------
        if action == "signup":
            show_signup = True

            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "")
            confirm_password = request.POST.get("confirm_password", "")
            role = request.POST.get("role", "SALESMAN").strip().upper()

            if not username:
                error_message = "Username is required."

            elif not password:
                error_message = "Password is required."

            elif password != confirm_password:
                error_message = "Passwords do not match."

            elif role not in ("MANAGER", "SALESMAN"):
                error_message = (
                    "You can register only a Manager or Salesman account."
                )

            elif User.objects.filter(username__iexact=username).exists():
                error_message = "This username is already registered."

            else:
                new_user = User(username=username, role=role)

                try:
                    validate_password(password, user=new_user)

                except ValidationError as error:
                    error_message = " ".join(error.messages)

                if error_message is None:
                    try:
                        new_user.set_password(password)
                        new_user.save()

                        messages.success(
                            request,
                            "Account created successfully. You can now log in.",
                        )
                        return redirect("login")

                    except IntegrityError:
                        error_message = (
                            "This account could not be created. "
                            "The username may already exist."
                        )

        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------
        else:
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
        {
            "error_message": error_message,
            "show_signup": show_signup,
        },
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required(login_url="/")
def logout_view(request):
    logout(request)
    return redirect("login")


# ============================================================
# ADMIN CREATE USER
# ============================================================

@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
def admin_create_user(request):
    """
    Create Manager or Salesman accounts from the Admin Dashboard popup.
    """

    if request.method != "POST":
        return redirect("admin_dashboard")

    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    role = request.POST.get("role", "SALESMAN").strip().upper()
    password = request.POST.get("password", "")
    confirm_password = request.POST.get("confirm_password", "")

    if not username:
        messages.error(request, "Username is required.")

    elif User.objects.filter(username__iexact=username).exists():
        messages.error(request, "This username is already taken.")

    elif role not in ("MANAGER", "SALESMAN"):
        messages.error(
            request,
            "Only Manager and Salesman accounts can be created.",
        )

    elif not password:
        messages.error(request, "Password is required.")

    elif password != confirm_password:
        messages.error(request, "Passwords do not match.")

    else:
        new_user = User(
            username=username,
            email=email,
            role=role,
        )

        try:
            validate_password(password, user=new_user)

            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
            )

            messages.success(
                request,
                f"{role.title()} account '{username}' was created successfully.",
            )

        except ValidationError as error:
            messages.error(request, " ".join(error.messages))

        except IntegrityError:
            messages.error(
                request,
                "The account could not be created. "
                "The username may already exist.",
            )

    return redirect("admin_dashboard")


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
def admin_dashboard(request):
    """Calculate Admin Dashboard statistics and chart data."""

    current_year = timezone.localdate().year

    # Product statistics
    total_products = Product.objects.count()

    available_stock = (
        Product.objects.aggregate(
            total=Sum("CurrentStock")
        )["total"]
        or 0
    )

    # Sales statistics
    total_sales = (
        Sale.objects.aggregate(
            total=Sum("TotalAmount")
        )["total"]
        or Decimal("0.00")
    )

    # Customer, supplier, and user statistics
    total_users = User.objects.count()
    total_customers = Customer.objects.count()
    total_suppliers = Supplier.objects.count()

    # Low-stock products: five or fewer
    low_stock_products = (
        Product.objects
        .filter(CurrentStock__lte=5)
        .order_by("CurrentStock", "Name")[:10]
    )

    # All-time Stock In / Stock Out quantities
    stock_in_total = (
        StockEntryDetail.objects.aggregate(
            total=Sum("Quantity")
        )["total"]
        or 0
    )

    stock_out_total = (
        SaleDetail.objects.aggregate(
            total=Sum("Quantity")
        )["total"]
        or 0
    )

    # Monthly sales chart
    month_labels, monthly_sales_values = get_monthly_sales_data(
        current_year
    )

    # Sales by category chart
    category_field = Product._meta.get_field("CT_Id")
    category_model = category_field.related_model

    category_name_field = next(
        (
            field.name
            for field in category_model._meta.fields
            if field.name in (
                "Name",
                "CT_Name",
                "CategoryName",
                "Category_Name",
            )
        ),
        None,
    )

    if category_name_field:
        sales_category_key = (
            f"Product__CT_Id__{category_name_field}"
        )
    else:
        sales_category_key = "Product__CT_Id"

    sales_by_category = (
        SaleDetail.objects
        .values(sales_category_key)
        .annotate(
            category_sales=Sum(
                ExpressionWrapper(
                    F("Quantity") * F("SellingPrice"),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                )
            )
        )
        .order_by(sales_category_key)
    )

    sales_category_labels = []
    sales_category_values = []

    for item in sales_by_category:
        value = item.get(sales_category_key)

        if category_name_field:
            label = str(value or "Uncategorized")
        else:
            label = f"Category {value}"

        sales_category_labels.append(label)
        sales_category_values.append(
            float(item["category_sales"] or 0)
        )

    # Inventory status chart
    active_products = Product.objects.filter(Status="Active")

    inventory_status_labels = [
        "In Stock",
        "Low Stock",
        "Out of Stock",
    ]

    inventory_status_values = [
        active_products.filter(CurrentStock__gt=5).count(),
        active_products.filter(
            CurrentStock__gt=0,
            CurrentStock__lte=5,
        ).count(),
        active_products.filter(CurrentStock__lte=0).count(),
    ]

    # Inventory valuation report
    if category_name_field:
        inventory_category_key = f"CT_Id__{category_name_field}"
    else:
        inventory_category_key = "CT_Id"

    inventory_report = (
        Product.objects
        .values(inventory_category_key)
        .annotate(
            stock_value=Sum(
                ExpressionWrapper(
                    F("CurrentStock") * F("CostPrice"),
                    output_field=DecimalField(
                        max_digits=18,
                        decimal_places=2,
                    ),
                )
            )
        )
        .order_by(inventory_category_key)
    )

    inventory_report_labels = []
    inventory_report_values = []

    for item in inventory_report:
        value = item.get(inventory_category_key)

        if category_name_field:
            label = str(value or "Uncategorized")
        else:
            label = f"Category {value}"

        inventory_report_labels.append(label)
        inventory_report_values.append(
            float(item["stock_value"] or 0)
        )

    context = {
        "total_products": total_products,
        "available_stock": available_stock,
        "total_sales": total_sales,
        "total_users": total_users,
        "total_customers": total_customers,
        "total_suppliers": total_suppliers,
        "low_stock_products": low_stock_products,
        "stock_in_total": stock_in_total,
        "stock_out_total": stock_out_total,
        "current_year": current_year,
        "month_labels": month_labels,
        "monthly_sales_values": monthly_sales_values,
        "sales_category_labels": sales_category_labels,
        "sales_category_values": sales_category_values,
        "inventory_status_labels": inventory_status_labels,
        "inventory_status_values": inventory_status_values,
        "inventory_report_labels": inventory_report_labels,
        "inventory_report_values": inventory_report_values,
    }

    return render(
        request,
        "accounts/admin_dashboard.html",
        context,
    )


# ============================================================
# MANAGER DASHBOARD
# ============================================================

@login_required(login_url="/")
@user_passes_test(is_manager, login_url="/")
def manager_dashboard(request):
    """
    Display Manager Dashboard statistics, charts, low-stock products,
    and the three most recent sales.

    No TruncMonth(), TruncDate(), SaleDate__date, or other
    date-truncation operations are used here.
    """

    today = timezone.localdate()
    current_year = today.year

    # Product statistics
    total_products = Product.objects.count()

    low_stock_queryset = Product.objects.filter(
        CurrentStock__lte=5
    )

    low_stock_count = low_stock_queryset.count()

    low_stock_products = (
        low_stock_queryset
        .order_by("CurrentStock", "Name")[:10]
    )

    # Today's sales: use a datetime range, not SaleDate__date
    today_start, tomorrow_start = get_local_day_range(today)

    today_sales = Sale.objects.filter(
        SaleDate__gte=today_start,
        SaleDate__lt=tomorrow_start,
    )

    today_sales_count = today_sales.count()

    today_revenue = (
        today_sales.aggregate(
            total=Sum("TotalAmount")
        )["total"]
        or Decimal("0.00")
    )

    # All-time Stock In / Stock Out quantities
    stock_in_total = (
        StockEntryDetail.objects.aggregate(
            total=Sum("Quantity")
        )["total"]
        or 0
    )

    stock_out_total = (
        SaleDetail.objects.aggregate(
            total=Sum("Quantity")
        )["total"]
        or 0
    )

    # Monthly sales chart: all twelve months
    month_labels, monthly_sales_values = get_monthly_sales_data(
        current_year
    )

    # Three most recent sales
    recent_sales = (
        Sale.objects
        .select_related("Customer")
        .order_by("-SaleDate", "-SaleId")[:3]
    )

    context = {
        "dashboard_date": today,
        "current_year": current_year,
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "low_stock_products": low_stock_products,
        "today_sales_count": today_sales_count,
        "today_revenue": today_revenue,
        "stock_in_total": stock_in_total,
        "stock_out_total": stock_out_total,
        "month_labels": month_labels,
        "monthly_sales_values": monthly_sales_values,
        "recent_sales": recent_sales,
    }

    return render(
        request,
        "accounts/manager_dashboard.html",
        context,
    )


# ============================================================
# SALESMAN DASHBOARD
# Weekly Sales Overview + Product Stock Status
# ============================================================

@login_required(login_url="/")
@user_passes_test(is_salesman, login_url="/")
def salesman_dashboard(request):
    """
    Display the Salesman Dashboard with:
    - Total products
    - Today's sales and revenue
    - Total invoices
    - Weekly sales revenue (Monday to Sunday)
    - Product stock status doughnut chart
    - Recent sales
    - Available products

    Uses datetime ranges instead of SaleDate__date.
    """

    today = timezone.localdate()

    # --------------------------------------------------------
    # PRODUCT STATISTICS
    # --------------------------------------------------------

    total_products = Product.objects.count()

    # --------------------------------------------------------
    # TODAY'S SALES AND REVENUE
    # --------------------------------------------------------

    today_start, tomorrow_start = get_local_day_range(today)

    today_sales = Sale.objects.filter(
        SaleDate__gte=today_start,
        SaleDate__lt=tomorrow_start,
    )

    today_sales_count = today_sales.count()

    today_revenue = (
        today_sales.aggregate(
            total=Sum("TotalAmount")
        )["total"]
        or Decimal("0.00")
    )

    # Each Sale record represents one invoice.
    total_invoices = Sale.objects.count()

    # --------------------------------------------------------
    # WEEKLY SALES OVERVIEW
    # Monday through Sunday, including days with no sales.
    # --------------------------------------------------------

    week_start = today - timedelta(days=today.weekday())

    weekly_sales_labels = []
    weekly_sales_values = []

    for day_offset in range(7):
        sale_day = week_start + timedelta(days=day_offset)

        day_start, next_day_start = get_local_day_range(sale_day)

        daily_sales = Sale.objects.filter(
            SaleDate__gte=day_start,
            SaleDate__lt=next_day_start,
        )

        daily_revenue = (
            daily_sales.aggregate(
                total=Sum("TotalAmount")
            )["total"]
            or Decimal("0.00")
        )

        weekly_sales_labels.append(sale_day.strftime("%a"))
        weekly_sales_values.append(float(daily_revenue))

    # Convert chart data to valid JSON for JavaScript.
    weekly_sales_labels_json = json.dumps(weekly_sales_labels)
    weekly_sales_values_json = json.dumps(weekly_sales_values)

    # --------------------------------------------------------
    # PRODUCT STOCK STATUS
    #
    # In Stock:    CurrentStock > 5
    # Low Stock:   CurrentStock from 1 to 5
    # Out of Stock: CurrentStock <= 0
    #
    # Only active products are included in the chart.
    # --------------------------------------------------------

    active_products = Product.objects.filter(
        Status="Active"
    )

    in_stock_count = active_products.filter(
        CurrentStock__gt=5
    ).count()

    low_stock_count = active_products.filter(
        CurrentStock__gt=0,
        CurrentStock__lte=5,
    ).count()

    out_of_stock_count = active_products.filter(
        CurrentStock__lte=0
    ).count()

    inventory_status_labels = [
        "In Stock",
        "Low Stock",
        "Out of Stock",
    ]

    inventory_status_values = [
        in_stock_count,
        low_stock_count,
        out_of_stock_count,
    ]

    inventory_status_labels_json = json.dumps(
        inventory_status_labels
    )

    inventory_status_values_json = json.dumps(
        inventory_status_values
    )

    # --------------------------------------------------------
    # RECENT SALES
    # --------------------------------------------------------

    recent_sales = (
        Sale.objects
        .select_related("Customer")
        .order_by("-SaleDate", "-SaleId")[:3]
    )

    # --------------------------------------------------------
    # AVAILABLE PRODUCTS
    # --------------------------------------------------------

    available_products = (
        Product.objects
        .filter(CurrentStock__gt=0)
        .order_by("Name")[:3]
    )

    # --------------------------------------------------------
    # TEMPLATE CONTEXT
    # --------------------------------------------------------

    context = {
        # Dashboard statistics
        "dashboard_date": today,
        "total_products": total_products,
        "today_sales_count": today_sales_count,
        "today_revenue": today_revenue,
        "total_invoices": total_invoices,

        # Weekly sales chart
        "weekly_sales_labels_json": weekly_sales_labels_json,
        "weekly_sales_values_json": weekly_sales_values_json,

        # Product stock-status chart
        "inventory_status_labels_json": inventory_status_labels_json,
        "inventory_status_values_json": inventory_status_values_json,

        # Individual stock counts for dashboard labels
        "in_stock_count": in_stock_count,
        "low_stock_count": low_stock_count,
        "out_of_stock_count": out_of_stock_count,

        # Existing dashboard sections
        "recent_sales": recent_sales,
        "available_products": available_products,
    }

    return render(
        request,
        "accounts/salesman_dashboard.html",
        context,
    )


# ============================================================
# ADMIN DATABASE BACKUP
# FR10.1 - Data Backup Functionality
# ============================================================

@login_required(login_url="/")
@user_passes_test(is_admin, login_url="/")
def admin_backup(request):
    """
    GET: Display the backup page.
    POST: Create and download a MySQL SQL backup.
    """

    if request.method != "POST":
        return render(
            request,
            "accounts/admin_backup.html",
        )

    database_config = settings.DATABASES["default"]

    if "mysql" not in database_config.get("ENGINE", "").lower():
        messages.error(
            request,
            "Database backup is configured for MySQL databases only.",
        )
        return redirect("accounts:admin_backup_page")

    # Find mysqldump
    mysqldump = shutil.which("mysqldump")

    if not mysqldump:
        possible_paths = [
            r"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqldump.exe",
            r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
            r"C:\Program Files\MySQL\MySQL Server 9.0\bin\mysqldump.exe",
            r"C:\xampp\mysql\bin\mysqldump.exe",
            r"C:\wamp64\bin\mysql\mysql8.0.31\bin\mysqldump.exe",
        ]

        mysqldump = next(
            (
                path
                for path in possible_paths
                if Path(path).is_file()
            ),
            None,
        )

    if not mysqldump:
        messages.error(
            request,
            "mysqldump was not found. Add the MySQL bin directory "
            "to your Windows PATH.",
        )
        return redirect("accounts:admin_backup_page")

    database_name = database_config.get("NAME")
    database_user = database_config.get("USER")
    database_password = database_config.get("PASSWORD", "")
    database_host = database_config.get("HOST") or "localhost"
    database_port = str(database_config.get("PORT") or "3306")

    if not database_name or not database_user:
        messages.error(
            request,
            "The MySQL database name or username is missing in settings.py.",
        )
        return redirect("accounts:admin_backup_page")

    backup_directory = Path(settings.BASE_DIR) / "backups"
    backup_directory.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{database_name}_{timestamp}.sql"
    backup_path = backup_directory / backup_filename

    command = [
        mysqldump,
        "--host", database_host,
        "--port", database_port,
        "--user", database_user,
        "--result-file", str(backup_path),
        database_name,
    ]

    environment = os.environ.copy()

    if database_password:
        environment["MYSQL_PWD"] = database_password

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            env=environment,
            shell=False,
        )

        if result.returncode != 0:
            backup_path.unlink(missing_ok=True)
            print("mysqldump error:", result.stderr)

            messages.error(
                request,
                "Backup failed. Check MySQL credentials and permissions.",
            )
            return redirect("accounts:admin_backup_page")

        return FileResponse(
            open(backup_path, "rb"),
            as_attachment=True,
            filename=backup_filename,
            content_type="application/sql",
        )

    except (OSError, subprocess.SubprocessError) as error:
        backup_path.unlink(missing_ok=True)
        print("Database backup error:", error)

        messages.error(
            request,
            "An error occurred while creating the database backup.",
        )
        return redirect("accounts:admin_backup_page")
