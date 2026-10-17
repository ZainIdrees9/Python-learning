import os
import shutil
import subprocess
import tempfile

from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from .models import Product


from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Sum, Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from datetime import datetime, time, timedelta
import calendar

from .models import (
    Category,
    Product,
    Supplier,
    StockEntry,
    StockEntryDetail,
    Customer,
    Sale,
    SaleDetail,
    SaleReturn,
    SaleReturnDetail,
    ActivityLog,
)

from .forms import (
    ProductForm,
    SupplierForm,
    StockEntryForm,
    StockEntryDetailForm,
    CustomerForm,
    SaleForm,
    SaleDetailFormSet,
)

from .utils import log_activity


# ============================================================
# ROLE FUNCTIONS
# ============================================================

def is_management(user):

    return (
        user.is_authenticated
        and getattr(user, 'role', None)
        in ['ADMIN', 'MANAGER']
    )


def is_salesman(user):

    return (
        user.is_authenticated
        and getattr(user, 'role', None)
        == 'SALESMAN'
    )


def is_sales_access(user):

    return (
        user.is_authenticated
        and getattr(user, 'role', None)
        in [
            'ADMIN',
            'MANAGER',
            'SALESMAN'
        ]
    )


def is_product_access(user):

    return (
        user.is_authenticated
        and getattr(user, 'role', None)
        in [
            'ADMIN',
            'MANAGER',
            'SALESMAN'
        ]
    )


# ============================================================
# PRODUCT MODULE
# ADMIN + MANAGER + SALESMAN
# SALESMAN = VIEW ONLY
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_product_access, login_url='/')
def product_list(request):

    categories = Category.objects.order_by('Name')

    products = (
        Product.objects
        .filter(Status='Active')
        .select_related('Category')
        .order_by('Name')
    )

    search_query = request.GET.get(
        'q',
        ''
    ).strip()

    category_query = request.GET.get(
        'category',
        ''
    ).strip()

    if request.GET.get('search') == '1':

        if search_query:

            products = products.filter(
                Q(Name__icontains=search_query)
            )

        if category_query:

            try:

                category_id = int(
                    category_query
                )

                products = products.filter(
                    Category__CT_Id=category_id
                )

            except (ValueError, TypeError):

                category_query = ''

    return render(
        request,
        'inventory/product_list.html',
        {
            'products': products,
            'categories': categories,
            'search_query': search_query,
            'category_query': category_query,
            'is_salesman': is_salesman(
                request.user
            ),
            'is_management': is_management(
                request.user
            ),
        }
    )


# ============================================================
# PRODUCT CREATE
# FR10.3 ACTIVITY LOG
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def product_create(request):

    if request.method == 'POST':

        form = ProductForm(
            request.POST
        )

        if form.is_valid():

            product = form.save()

            log_activity(
                request,
                action='Product Added',
                module='Inventory',
                description=(
                    f'Product "{product.Name}" '
                    f'was added.'
                )
            )

            return redirect(
                'inventory:product_list'
            )

    else:

        form = ProductForm()

    return render(
        request,
        'inventory/product_form.html',
        {
            'form': form,
            'title': 'Add Product',
            'edit_mode': False,
        }
    )


# ============================================================
# PRODUCT EDIT
# FR10.3 ACTIVITY LOG
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def product_edit(request, ProductId):

    product = get_object_or_404(
        Product,
        ProductId=ProductId
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():

            product = form.save()

            log_activity(
                request,
                action='Product Updated',
                module='Inventory',
                description=(
                    f'Product "{product.Name}" '
                    f'was updated.'
                )
            )

            return redirect(
                'inventory:product_list'
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'inventory/product_form.html',
        {
            'form': form,
            'title': 'Edit Product',
            'product': product,
            'edit_mode': True,
        }
    )


# ============================================================
# PRODUCT DELETE
# SOFT DELETE
# FR10.3 ACTIVITY LOG
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def product_delete(request, ProductId):

    product = get_object_or_404(
        Product,
        ProductId=ProductId
    )

    if request.method == 'POST':

        product_name = product.Name

        product.Status = 'Inactive'

        product.save(
            update_fields=[
                'Status'
            ]
        )

        log_activity(
            request,
            action='Product Deleted',
            module='Inventory',
            description=(
                f'Product "{product_name}" '
                f'was marked as inactive.'
            )
        )

        return redirect(
            'inventory:product_list'
        )

    return render(
        request,
        'inventory/product_confirm_delete.html',
        {
            'product': product
        }
    )


# ============================================================
# SUPPLIER MODULE
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def supplier_list(request):

    suppliers = Supplier.objects.order_by(
        'Name'
    )

    return render(
        request,
        'inventory/supplier_list.html',
        {
            'suppliers': suppliers
        }
    )


# ============================================================
# SUPPLIER CREATE
# FR10.3 ACTIVITY LOG
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def supplier_create(request):

    if request.method == 'POST':

        form = SupplierForm(
            request.POST
        )

        if form.is_valid():

            supplier = form.save()

            log_activity(
                request,
                action='Supplier Added',
                module='Supplier Management',
                description=(
                    f'Supplier "{supplier.Name}" '
                    f'was added.'
                )
            )

            return redirect(
                'inventory:supplier_list'
            )

    else:

        form = SupplierForm()

    return render(
        request,
        'inventory/supplier_form.html',
        {
            'form': form,
            'title': 'Add Supplier'
        }
    )


# ============================================================
# STOCK MODULE
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def stock_entry_list(request):

    stock_entries = (
        StockEntry.objects
        .select_related('Supplier')
        .prefetch_related('details__Product')
        .order_by('-EntryDate')
    )

    return render(
        request,
        'inventory/stock_entry_list.html',
        {
            'stock_entries': stock_entries
        }
    )


# ============================================================
# STOCK CREATE
# FR10.3 ACTIVITY LOG
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def stock_entry_create(request):

    if request.method == 'POST':

        stock_form = StockEntryForm(
            request.POST
        )

        detail_form = StockEntryDetailForm(
            request.POST
        )

        if (
            stock_form.is_valid()
            and detail_form.is_valid()
        ):

            selected_product = (
                detail_form.cleaned_data['Product']
            )

            quantity = (
                detail_form.cleaned_data['Quantity']
            )

            purchase_price = (
                detail_form.cleaned_data[
                    'PurchasePrice'
                ]
            )

            with transaction.atomic():

                product = (
                    Product.objects
                    .select_for_update()
                    .get(
                        ProductId=(
                            selected_product.ProductId
                        )
                    )
                )

                stock_entry = (
                    stock_form.save()
                )

                stock_detail = (
                    detail_form.save(
                        commit=False
                    )
                )

                stock_detail.StockEntry = (
                    stock_entry
                )

                stock_detail.save()

                stock_entry.Cost = (
                    quantity
                    * purchase_price
                )

                stock_entry.save(
                    update_fields=[
                        'Cost'
                    ]
                )

                product.CurrentStock += (
                    quantity
                )

                product.CostPrice = (
                    purchase_price
                )

                product.save(
                    update_fields=[
                        'CurrentStock',
                        'CostPrice'
                    ]
                )

            log_activity(
                request,
                action='Stock Added',
                module='Stock Management',
                description=(
                    f'Stock entry '
                    f'#{stock_entry.SE_Id} '
                    f'was created for '
                    f'{product.Name}. '
                    f'Quantity: {quantity}.'
                )
            )

            return redirect(
                'inventory:stock_entry_list'
            )

    else:

        stock_form = StockEntryForm()
        detail_form = StockEntryDetailForm()

    return render(
        request,
        'inventory/stock_entry_form.html',
        {
            'stock_form': stock_form,
            'detail_form': detail_form,
            'title': 'Add Stock'
        }
    )


# ============================================================
# STOCK HISTORY / STOCK IN-OUT LOG
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def stock_history(request):

    stock_in = (
        StockEntryDetail.objects
        .select_related(
            'StockEntry',
            'StockEntry__Supplier',
            'Product'
        )
        .order_by(
            '-StockEntry__EntryDate'
        )
    )

    stock_out = (
        SaleDetail.objects
        .select_related(
            'Sale',
            'Sale__Customer',
            'Product'
        )
        .order_by(
            '-Sale__SaleDate'
        )
    )

    history = []

    # ========================================================
    # STOCK IN
    # ========================================================

    for entry in stock_in:

        history.append({
            'date': entry.StockEntry.EntryDate,
            'product': entry.Product,
            'type': 'Stock In',
            'quantity': entry.Quantity,
            'reference': (
                f'Purchase #'
                f'{entry.StockEntry.SE_Id}'
            ),
            'party': (
                entry.StockEntry.Supplier.Name
            ),
        })

    # ========================================================
    # STOCK OUT
    # ========================================================

    for detail in stock_out:

        history.append({
            'date': detail.Sale.SaleDate,
            'product': detail.Product,
            'type': 'Stock Out',
            'quantity': detail.Quantity,
            'reference': (
                f'Sale #'
                f'{detail.Sale.SaleId}'
            ),
            'party': (
                detail.Sale.Customer.Name
            ),
        })

    # ========================================================
    # SORT NEWEST FIRST
    # ========================================================

    history.sort(
        key=lambda item: item['date'],
        reverse=True
    )

    return render(
        request,
        'inventory/stock_history.html',
        {
            'history': history
        }
    )


# ============================================================
# CUSTOMER MODULE
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def customer_list(request):

    customers = Customer.objects.order_by(
        'Name'
    )

    return render(
        request,
        'inventory/customer_list.html',
        {
            'customers': customers
        }
    )


# ============================================================
# CUSTOMER CREATE
# FR10.3 ACTIVITY LOG
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def customer_create(request):

    if request.method == 'POST':

        form = CustomerForm(
            request.POST
        )

        if form.is_valid():

            customer = form.save()

            log_activity(
                request,
                action='Customer Added',
                module='Customer Management',
                description=(
                    f'Customer "{customer.Name}" '
                    f'was added.'
                )
            )

            return redirect(
                'inventory:customer_list'
            )

    else:

        form = CustomerForm()

    return render(
        request,
        'inventory/customer_form.html',
        {
            'form': form,
            'title': 'Add Customer'
        }
    )


# ============================================================
# CUSTOMER EDIT
# FR10.3 ACTIVITY LOG
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def customer_edit(request, CustomerId):

    customer = get_object_or_404(
        Customer,
        CustomerId=CustomerId
    )

    if request.method == 'POST':

        form = CustomerForm(
            request.POST,
            instance=customer
        )

        if form.is_valid():

            customer = form.save()

            log_activity(
                request,
                action='Customer Updated',
                module='Customer Management',
                description=(
                    f'Customer "{customer.Name}" '
                    f'was updated.'
                )
            )

            return redirect(
                'inventory:customer_list'
            )

    else:

        form = CustomerForm(
            instance=customer
        )

    return render(
        request,
        'inventory/customer_form.html',
        {
            'form': form,
            'title': 'Edit Customer',
            'customer': customer
        }
    )


# ============================================================
# CUSTOMER DELETE
# FR10.3 ACTIVITY LOG
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def customer_delete(request, CustomerId):

    customer = get_object_or_404(
        Customer,
        CustomerId=CustomerId
    )

    if request.method == 'POST':

        if customer.sales.exists():

            return render(
                request,
                'inventory/customer_confirm_delete.html',
                {
                    'customer': customer,
                    'error': (
                        'This customer cannot be deleted '
                        'because they have existing '
                        'sales records.'
                    )
                }
            )

        customer_name = customer.Name

        customer.delete()

        log_activity(
            request,
            action='Customer Deleted',
            module='Customer Management',
            description=(
                f'Customer "{customer_name}" '
                f'was deleted.'
            )
        )

        return redirect(
            'inventory:customer_list'
        )

    return render(
        request,
        'inventory/customer_confirm_delete.html',
        {
            'customer': customer
        }
    )


# ============================================================
# CUSTOMER TRANSACTION HISTORY
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def customer_transaction_history(
    request,
    CustomerId
):

    customer = get_object_or_404(
        Customer,
        CustomerId=CustomerId
    )

    sales = (
        Sale.objects
        .filter(
            Customer=customer
        )
        .prefetch_related(
            'details__Product'
        )
        .order_by('-SaleDate')
    )

    returns = (
        SaleReturn.objects
        .filter(
            Sale__Customer=customer
        )
        .select_related(
            'Sale'
        )
        .prefetch_related(
            'details__SaleDetail__Product'
        )
        .order_by('-ReturnDate')
    )

    transactions = []

    total_sales = 0
    total_returns = 0

    # ========================================================
    # SALES
    # ========================================================

    for sale in sales:

        amount = (
            sale.TotalAmount
            or 0
        )

        total_sales += amount

        transactions.append({
            'date': sale.SaleDate,
            'type': 'Sale',
            'reference': (
                f'Invoice #{sale.SaleId}'
            ),
            'amount': amount,
            'sale_id': sale.SaleId,
        })

    # ========================================================
    # RETURNS
    # ========================================================

    for sale_return in returns:

        amount = (
            sale_return.TotalAmount
            or 0
        )

        total_returns += amount

        transactions.append({
            'date': sale_return.ReturnDate,
            'type': 'Return',
            'reference': (
                f'Return #{sale_return.ReturnId}'
            ),
            'amount': amount,
            'return_id': sale_return.ReturnId,
        })

    # ========================================================
    # SORT NEWEST FIRST
    # ========================================================

    transactions.sort(
        key=lambda item: item['date'],
        reverse=True
    )

    # ========================================================
    # NET AMOUNT
    # ========================================================

    net_amount = (
        total_sales
        - total_returns
    )

    return render(
        request,
        'inventory/customer_transaction_history.html',
        {
            'customer': customer,
            'transactions': transactions,
            'total_sales': total_sales,
            'total_returns': total_returns,
            'net_amount': net_amount,
        }
    )


# ============================================================
# SUPPLIER TRANSACTION HISTORY
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def supplier_transaction_history(
    request,
    SupplierId
):

    supplier = get_object_or_404(
        Supplier,
        SupplierId=SupplierId
    )

    stock_entries = (
        StockEntry.objects
        .filter(
            Supplier=supplier
        )
        .prefetch_related(
            'details__Product'
        )
        .order_by('-EntryDate')
    )

    total_purchases = (
        stock_entries.aggregate(
            total=Sum('Cost')
        ).get('total')
        or 0
    )

    return render(
        request,
        'inventory/supplier_transaction_history.html',
        {
            'supplier': supplier,
            'stock_entries': stock_entries,
            'total_purchases': total_purchases,
        }
    )


# ============================================================
# SALES MODULE
# ADMIN + MANAGER + SALESMAN
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_sales_access, login_url='/')
def sale_list(request):

    sales = (
        Sale.objects
        .select_related('Customer')
        .prefetch_related('details__Product')
        .order_by('-SaleDate')
    )

    # ========================================================
    # GET FILTER VALUES
    # ========================================================

    from_date = request.GET.get(
        'from_date',
        ''
    ).strip()

    to_date = request.GET.get(
        'to_date',
        ''
    ).strip()

    customer_id = request.GET.get(
        'customer',
        ''
    ).strip()

    product_id = request.GET.get(
        'product',
        ''
    ).strip()

    # ========================================================
    # DATE FILTER
    # ========================================================

    if from_date:

        sales = sales.filter(
            SaleDate__gte=(
                f'{from_date} 00:00:00'
            )
        )

    if to_date:

        sales = sales.filter(
            SaleDate__lte=(
                f'{to_date} 23:59:59'
            )
        )

    # ========================================================
    # CUSTOMER FILTER
    # ========================================================

    if customer_id:

        sales = sales.filter(
            Customer__CustomerId=customer_id
        )

    # ========================================================
    # PRODUCT FILTER
    # ========================================================

    if product_id:

        sales = sales.filter(
            details__Product__ProductId=product_id
        )

    # ========================================================
    # REMOVE DUPLICATE SALES
    # ========================================================

    sales = sales.distinct()

    customers = (
        Customer.objects
        .all()
        .order_by('Name')
    )

    products = (
        Product.objects
        .all()
        .order_by('Name')
    )

    context = {

        'sales': sales,

        'customers': customers,

        'products': products,

        'from_date': from_date,

        'to_date': to_date,

        'selected_customer': customer_id,

        'selected_product': product_id,

    }

    return render(
        request,
        'inventory/sale_list.html',
        context
    )


# ============================================================
# SALE CREATE
# AUTO-FETCH SELLING PRICE
# STOCK VALIDATION
# FR10.3 ACTIVITY LOG
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_sales_access, login_url='/')
def sale_create(request):

    if request.method == 'POST':

        post_data = request.POST.copy()

        # Get the actual formset prefix instead of assuming
        # it is always "details".
        formset_prefix = SaleDetailFormSet.get_default_prefix()

        # Automatically populate selling prices before
        # validating the detail formset.
        try:
            total_forms = int(
                post_data.get(
                    f'{formset_prefix}-TOTAL_FORMS',
                    0
                )
            )
        except (ValueError, TypeError):
            total_forms = 0

        for i in range(total_forms):

            product_id = post_data.get(
                f'{formset_prefix}-{i}-Product'
            )

            if not product_id:
                continue

            product = Product.objects.filter(
                ProductId=product_id,
                Status='Active'
            ).first()

            if product:
                post_data[
                    f'{formset_prefix}-{i}-SellingPrice'
                ] = str(product.UnitPrice)

        # Validate forms using the updated POST data.
        sale_form = SaleForm(post_data)

        detail_formset = SaleDetailFormSet(
            post_data,
            prefix=formset_prefix
        )

        if (
            sale_form.is_valid()
            and detail_formset.is_valid()
        ):

            detail_forms = []

            # Keep only rows with a selected product.
            for form in detail_formset:

                if not form.cleaned_data:
                    continue

                if form.cleaned_data.get('DELETE', False):
                    continue

                if not form.cleaned_data.get('Product'):
                    continue

                detail_forms.append(form)

            if not detail_forms:

                if detail_formset.forms:
                    detail_formset.forms[0].add_error(
                        None,
                        'Please add at least one product to the sale.'
                    )

            else:

                stock_error = False

                try:

                    with transaction.atomic():

                        products = {}

                        # ------------------------------------
                        # LOCK PRODUCTS
                        # ------------------------------------

                        for form in detail_forms:

                            selected_product = (
                                form.cleaned_data['Product']
                            )

                            product_id = (
                                selected_product.ProductId
                            )

                            if product_id not in products:

                                product = (
                                    Product.objects
                                    .select_for_update()
                                    .get(
                                        ProductId=product_id,
                                        Status='Active'
                                    )
                                )

                                products[product_id] = product

                        # ------------------------------------
                        # COMBINE QUANTITIES FOR EACH PRODUCT
                        # ------------------------------------

                        requested_quantities = {}

                        for form in detail_forms:

                            selected_product = (
                                form.cleaned_data['Product']
                            )

                            product_id = (
                                selected_product.ProductId
                            )

                            quantity = (
                                form.cleaned_data['Quantity']
                            )

                            requested_quantities[product_id] = (
                                requested_quantities.get(
                                    product_id,
                                    0
                                ) + quantity
                            )

                        # ------------------------------------
                        # VALIDATE AVAILABLE STOCK
                        # ------------------------------------

                        for (
                            product_id,
                            requested_quantity
                        ) in requested_quantities.items():

                            product = products[product_id]

                            if requested_quantity > product.CurrentStock:

                                stock_error = True

                                for form in detail_forms:

                                    form_product = (
                                        form.cleaned_data['Product']
                                    )

                                    if (
                                        form_product.ProductId
                                        == product_id
                                    ):

                                        form.add_error(
                                            'Quantity',
                                            (
                                                f'Only {product.CurrentStock} '
                                                f'units of {product.Name} '
                                                f'are available in stock.'
                                            )
                                        )

                        if stock_error:

                            # Leave the atomic block without saving.
                            # The form will be displayed again below.
                            pass

                        else:

                            # --------------------------------
                            # CREATE SALE
                            # --------------------------------

                            sale = sale_form.save(
                                commit=True
                            )

                            total_amount = 0

                            for form in detail_forms:

                                sale_detail = form.save(
                                    commit=False
                                )

                                sale_detail.Sale = sale

                                quantity = (
                                    form.cleaned_data['Quantity']
                                )

                                # Always use the current product price
                                # rather than trusting submitted data.
                                selected_product = (
                                    form.cleaned_data['Product']
                                )

                                selling_price = (
                                    products[
                                        selected_product.ProductId
                                    ].UnitPrice
                                )

                                sale_detail.SellingPrice = (
                                    selling_price
                                )

                                line_total = (
                                    quantity * selling_price
                                )

                                sale_detail.Total = line_total

                                sale_detail.save()

                                total_amount += line_total

                            # --------------------------------
                            # UPDATE SALE TOTAL
                            # --------------------------------

                            sale.TotalAmount = total_amount

                            sale.save(
                                update_fields=['TotalAmount']
                            )

                            # --------------------------------
                            # REDUCE STOCK
                            # --------------------------------

                            for (
                                product_id,
                                quantity
                            ) in requested_quantities.items():

                                product = products[product_id]

                                product.CurrentStock -= quantity

                                product.save(
                                    update_fields=['CurrentStock']
                                )

                            # --------------------------------
                            # FR10.3 ACTIVITY LOG
                            # --------------------------------

                            log_activity(
                                request,
                                action='Sale Created',
                                module='Sales',
                                description=(
                                    f'Sale #{sale.SaleId} was created. '
                                    f'Total amount: {sale.TotalAmount}.'
                                )
                            )

                            return redirect(
                                'inventory:sale_detail',
                                SaleId=sale.SaleId
                            )

                except Product.DoesNotExist:

                    # A product may have become inactive or been
                    # removed while the sale was being submitted.
                    sale_form.add_error(
                        None,
                        (
                            'One of the selected products is no longer '
                            'available. Please refresh the page and try again.'
                        )
                    )

    else:

        sale_form = SaleForm()

        detail_formset = SaleDetailFormSet()

    return render(
        request,
        'inventory/sale_form.html',
        {
            'sale_form': sale_form,
            'detail_formset': detail_formset,
            'title': 'Create Sale',
            'is_salesman': is_salesman(request.user),
            'is_management': is_management(request.user),
        }
    )


# ============================================================
# SALE DETAIL
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_sales_access, login_url='/')
def sale_detail(request, SaleId):

    sale = get_object_or_404(
        Sale.objects
        .select_related('Customer')
        .prefetch_related(
            'details__Product'
        ),
        SaleId=SaleId
    )

    details = sale.details.all()

    return render(
        request,
        'inventory/sale_detail.html',
        {
            'sale': sale,
            'details': details,
            'is_salesman': is_salesman(
                request.user
            ),
            'is_management': is_management(
                request.user
            ),
        }
    )


# ============================================================
# SALE INVOICE
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_sales_access, login_url='/')
def sale_invoice(request, SaleId):

    sale = get_object_or_404(
        Sale.objects
        .select_related('Customer')
        .prefetch_related(
            'details__Product'
        ),
        SaleId=SaleId
    )

    details = sale.details.all()

    return render(
        request,
        'inventory/sale_invoice.html',
        {
            'sale': sale,
            'details': details,
            'is_salesman': is_salesman(
                request.user
            ),
            'is_management': is_management(
                request.user
            ),
        }
    )


# ============================================================
# FR9.3 - QUICK INVOICE LOOKUP
# ADMIN + MANAGER + SALESMAN
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_sales_access, login_url='/')
def invoice_lookup(request):

    invoice_id = request.GET.get(
        'invoice_id',
        ''
    ).strip()

    if not invoice_id:

        return render(
            request,
            'inventory/invoice_lookup.html',
            {
                'invoice_id': invoice_id,
            }
        )

    try:

        invoice_id = int(
            invoice_id
        )

    except (ValueError, TypeError):

        return render(
            request,
            'inventory/invoice_lookup.html',
            {
                'invoice_id': invoice_id,
                'error': (
                    'Please enter a valid '
                    'invoice number.'
                ),
            }
        )

    sale = (
        Sale.objects
        .select_related('Customer')
        .prefetch_related(
            'details__Product'
        )
        .filter(
            SaleId=invoice_id
        )
        .first()
    )

    if not sale:

        return render(
            request,
            'inventory/invoice_lookup.html',
            {
                'invoice_id': invoice_id,
                'error': (
                    f'Invoice #{invoice_id} '
                    f'was not found.'
                ),
            }
        )

    return redirect(
        'inventory:sale_invoice',
        SaleId=sale.SaleId
    )


# ============================================================
# DOWNLOAD SALE INVOICE AS PDF
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_sales_access, login_url='/')
def sale_invoice_download(
    request,
    SaleId
):

    sale = get_object_or_404(
        Sale.objects
        .select_related('Customer')
        .prefetch_related(
            'details__Product'
        ),
        SaleId=SaleId
    )

    details = sale.details.all()

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        f'attachment; '
        f'filename="Invoice-{sale.SaleId}.pdf"'
    )

    document = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            '<b>YOUR STORE</b>',
            styles['Title']
        )
    )

    story.append(
        Paragraph(
            'Sales Invoice',
            styles['Normal']
        )
    )

    story.append(
        Spacer(1, 10)
    )

    invoice_date = sale.SaleDate.strftime(
        '%d %b %Y, %I:%M %p'
    )

    invoice_information = [
        [
            Paragraph(
                '<b>Invoice #:</b>',
                styles['Normal']
            ),
            str(sale.SaleId)
        ],
        [
            Paragraph(
                '<b>Date:</b>',
                styles['Normal']
            ),
            invoice_date
        ],
    ]

    invoice_table = Table(
        invoice_information,
        colWidths=[
            35 * mm,
            45 * mm
        ]
    )

    invoice_table.setStyle(
        TableStyle([
            (
                'VALIGN',
                (0, 0),
                (-1, -1),
                'TOP'
            ),
            (
                'ALIGN',
                (0, 0),
                (-1, -1),
                'LEFT'
            ),
        ])
    )

    story.append(
        invoice_table
    )

    story.append(
        Spacer(1, 15)
    )

    customer_name = 'Walk-in Customer'
    customer_phone = ''
    customer_email = ''
    customer_address = ''

    if sale.Customer:

        customer_name = (
            sale.Customer.Name
        )

        if sale.Customer.Phone:
            customer_phone = (
                sale.Customer.Phone
            )

        if sale.Customer.Email:
            customer_email = (
                sale.Customer.Email
            )

        if sale.Customer.Address:
            customer_address = (
                sale.Customer.Address
            )

    customer_data = [
        [
            Paragraph(
                '<b>Bill To</b>',
                styles['Heading4']
            ),
            ''
        ],
        [
            'Customer:',
            customer_name
        ],
    ]

    if customer_phone:

        customer_data.append(
            [
                'Phone:',
                customer_phone
            ]
        )

    if customer_email:

        customer_data.append(
            [
                'Email:',
                customer_email
            ]
        )

    if customer_address:

        customer_data.append(
            [
                'Address:',
                customer_address
            ]
        )

    customer_table = Table(
        customer_data,
        colWidths=[
            35 * mm,
            130 * mm
        ]
    )

    customer_table.setStyle(
        TableStyle([
            (
                'VALIGN',
                (0, 0),
                (-1, -1),
                'TOP'
            ),
            (
                'SPAN',
                (0, 0),
                (-1, 0)
            ),
            (
                'BOTTOMPADDING',
                (0, 0),
                (-1, 0),
                8
            ),
        ])
    )

    story.append(
        customer_table
    )

    story.append(
        Spacer(1, 15)
    )

    table_data = [
        [
            '#',
            'Product',
            'Quantity',
            'Unit Price',
            'Total'
        ]
    ]

    for index, detail in enumerate(
        details,
        start=1
    ):

        table_data.append(
            [
                str(index),
                detail.Product.Name,
                str(detail.Quantity),
                f'{detail.SellingPrice:.2f}',
                f'{detail.Total:.2f}',
            ]
        )

    table_data.append(
        [
            '',
            '',
            '',
            Paragraph(
                '<b>Grand Total</b>',
                styles['Normal']
            ),
            Paragraph(
                f'<b>{sale.TotalAmount:.2f}</b>',
                styles['Normal']
            ),
        ]
    )

    products_table = Table(
        table_data,
        colWidths=[
            10 * mm,
            75 * mm,
            25 * mm,
            30 * mm,
            30 * mm,
        ],
        repeatRows=1
    )

    products_table.setStyle(
        TableStyle([
            (
                'BACKGROUND',
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                'TEXTCOLOR',
                (0, 0),
                (-1, 0),
                colors.black
            ),
            (
                'GRID',
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                'ALIGN',
                (0, 0),
                (0, -1),
                'CENTER'
            ),
            (
                'ALIGN',
                (2, 1),
                (-1, -1),
                'RIGHT'
            ),
            (
                'VALIGN',
                (0, 0),
                (-1, -1),
                'MIDDLE'
            ),
            (
                'BACKGROUND',
                (0, -1),
                (-1, -1),
                colors.whitesmoke
            ),
            (
                'FONTNAME',
                (0, 0),
                (-1, 0),
                'Helvetica-Bold'
            ),
            (
                'BOTTOMPADDING',
                (0, 0),
                (-1, -1),
                6
            ),
            (
                'TOPPADDING',
                (0, 0),
                (-1, -1),
                6
            ),
        ])
    )

    story.append(
        products_table
    )

    if sale.Remarks:

        story.append(
            Spacer(1, 15)
        )

        story.append(
            Paragraph(
                '<b>Remarks</b>',
                styles['Heading4']
            )
        )

        story.append(
            Paragraph(
                str(sale.Remarks),
                styles['Normal']
            )
        )

    story.append(
        Spacer(1, 30)
    )

    story.append(
        Paragraph(
            '<b>Thank you for your business!</b>',
            styles['Normal']
        )
    )

    story.append(
        Spacer(1, 5)
    )

    story.append(
        Paragraph(
            'Please keep this invoice for your records.',
            styles['Normal']
        )
    )

    document.build(
        story
    )

    return response


# ============================================================
# SALES RETURN MODULE
# ADMIN + MANAGER + SALESMAN
# FR10.3 ACTIVITY LOG
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_sales_access, login_url='/')
def sale_return_create(
    request,
    SaleId
):

    sale = get_object_or_404(
        Sale.objects
        .select_related('Customer')
        .prefetch_related(
            'details__Product',
            'details__return_details'
        ),
        SaleId=SaleId
    )

    details = sale.details.all()

    return_data = []

    for detail in details:

        returned_quantity = (
            detail.return_details
            .aggregate(
                total=Sum('Quantity')
            )
            .get('total')
            or 0
        )

        remaining_quantity = (
            detail.Quantity
            - returned_quantity
        )

        return_data.append({
            'detail': detail,
            'sold_quantity': detail.Quantity,
            'returned_quantity': returned_quantity,
            'remaining_quantity': remaining_quantity,
            'selling_price': detail.SellingPrice,
        })

    if request.method == 'POST':

        remarks = request.POST.get(
            'Remarks',
            ''
        ).strip()

        selected_items = []

        for item in return_data:

            detail = item['detail']

            quantity_value = request.POST.get(
                f'quantity_{detail.SaleDetailId}',
                '0'
            )

            try:

                quantity = int(
                    quantity_value
                )

            except (ValueError, TypeError):

                quantity = 0

            if quantity < 0:

                quantity = 0

            if (
                quantity
                > item['remaining_quantity']
            ):

                return render(
                    request,
                    'inventory/sale_return_form.html',
                    {
                        'sale': sale,
                        'return_data': return_data,
                        'error': (
                            f'You cannot return more than '
                            f'{item["remaining_quantity"]} '
                            f'units of '
                            f'{detail.Product.Name}.'
                        )
                    }
                )

            if quantity > 0:

                selected_items.append({
                    'detail': detail,
                    'quantity': quantity,
                })

        if not selected_items:

            return render(
                request,
                'inventory/sale_return_form.html',
                {
                    'sale': sale,
                    'return_data': return_data,
                    'error': (
                        'Please select at least one '
                        'product to return.'
                    )
                }
            )

        with transaction.atomic():

            locked_products = {}

            for item in selected_items:

                product_id = (
                    item[
                        'detail'
                    ].Product.ProductId
                )

                if (
                    product_id
                    not in locked_products
                ):

                    locked_products[
                        product_id
                    ] = (
                        Product.objects
                        .select_for_update()
                        .get(
                            ProductId=product_id
                        )
                    )

            sale_return = (
                SaleReturn.objects.create(
                    Sale=sale,
                    Remarks=remarks,
                    TotalAmount=0
                )
            )

            total_refund = 0

            for item in selected_items:

                detail = item['detail']

                quantity = item['quantity']

                refund_amount = (
                    quantity
                    * detail.SellingPrice
                )

                SaleReturnDetail.objects.create(
                    SaleReturn=sale_return,
                    SaleDetail=detail,
                    Quantity=quantity,
                    RefundAmount=refund_amount
                )

                total_refund += (
                    refund_amount
                )

                product = locked_products[
                    detail.Product.ProductId
                ]

                product.CurrentStock += (
                    quantity
                )

                product.save(
                    update_fields=[
                        'CurrentStock'
                    ]
                )

            sale_return.TotalAmount = (
                total_refund
            )

            sale_return.save(
                update_fields=[
                    'TotalAmount'
                ]
            )

        # ====================================================
        # FR10.3 ACTIVITY LOG
        # ====================================================

        log_activity(
            request,
            action='Sale Return Created',
            module='Sales Return',
            description=(
                f'Sale return '
                f'#{sale_return.ReturnId} '
                f'was created for sale '
                f'#{sale.SaleId}. '
                f'Refund amount: '
                f'{sale_return.TotalAmount}.'
            )
        )

        return redirect(
            'inventory:sale_return_detail',
            ReturnId=sale_return.ReturnId
        )

    return render(
        request,
        'inventory/sale_return_form.html',
        {
            'sale': sale,
            'return_data': return_data,
        }
    )


# ============================================================
# RETURN DETAIL
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_sales_access, login_url='/')
def sale_return_detail(
    request,
    ReturnId
):

    sale_return = get_object_or_404(
        SaleReturn.objects
        .select_related(
            'Sale',
            'Sale__Customer'
        )
        .prefetch_related(
            'details__SaleDetail__Product'
        ),
        ReturnId=ReturnId
    )

    details = sale_return.details.all()

    return render(
        request,
        'inventory/sale_return_detail.html',
        {
            'sale_return': sale_return,
            'details': details,
        }
    )


# ============================================================
# RETURN HISTORY
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def sale_return_list(request):

    returns = (
        SaleReturn.objects
        .select_related(
            'Sale',
            'Sale__Customer'
        )
        .prefetch_related(
            'details__SaleDetail__Product'
        )
        .order_by('-ReturnDate')
    )

    return render(
        request,
        'inventory/sale_return_list.html',
        {
            'returns': returns
        }
    )


# ============================================================
# DAILY SALES REPORT
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def daily_sales_report(request):

    selected_date = request.GET.get(
        'date'
    )

    if selected_date:

        try:

            report_date = datetime.strptime(
                selected_date,
                '%Y-%m-%d'
            ).date()

        except ValueError:

            report_date = timezone.localdate()

    else:

        report_date = timezone.localdate()

    start_datetime = timezone.make_aware(
        datetime.combine(
            report_date,
            time.min
        )
    )

    end_datetime = (
        start_datetime
        + timedelta(days=1)
    )

    sales = (
        Sale.objects
        .filter(
            SaleDate__gte=start_datetime,
            SaleDate__lt=end_datetime
        )
        .select_related('Customer')
        .prefetch_related(
            'details__Product'
        )
        .order_by('SaleDate')
    )

    summary = sales.aggregate(
        total_sales=Sum('TotalAmount'),
        total_invoices=Count('SaleId')
    )

    total_items = (
        SaleDetail.objects
        .filter(
            Sale__SaleDate__gte=start_datetime,
            Sale__SaleDate__lt=end_datetime
        )
        .aggregate(
            total_items=Sum('Quantity')
        )
        .get('total_items')
        or 0
    )

    return render(
        request,
        'inventory/daily_sales_report.html',
        {
            'sales': sales,
            'report_date': report_date,
            'total_sales': (
                summary.get(
                    'total_sales'
                )
                or 0
            ),
            'total_invoices': (
                summary.get(
                    'total_invoices'
                )
                or 0
            ),
            'total_items': total_items,
        }
    )


# ============================================================
# MONTHLY SALES REPORT
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def monthly_sales_report(request):

    current_date = timezone.localdate()

    try:

        year = int(
            request.GET.get(
                'year',
                current_date.year
            )
        )

        month = int(
            request.GET.get(
                'month',
                current_date.month
            )
        )

        if month < 1 or month > 12:

            raise ValueError

    except (ValueError, TypeError):

        year = current_date.year
        month = current_date.month

    start_datetime = timezone.make_aware(
        datetime(
            year,
            month,
            1,
            0,
            0,
            0
        )
    )

    if month == 12:

        end_datetime = timezone.make_aware(
            datetime(
                year + 1,
                1,
                1,
                0,
                0,
                0
            )
        )

    else:

        end_datetime = timezone.make_aware(
            datetime(
                year,
                month + 1,
                1,
                0,
                0,
                0
            )
        )

    sales = (
        Sale.objects
        .filter(
            SaleDate__gte=start_datetime,
            SaleDate__lt=end_datetime
        )
        .select_related('Customer')
        .prefetch_related(
            'details__Product'
        )
        .order_by('SaleDate')
    )

    summary = sales.aggregate(
        total_sales=Sum('TotalAmount'),
        total_invoices=Count('SaleId')
    )

    total_items = (
        SaleDetail.objects
        .filter(
            Sale__SaleDate__gte=start_datetime,
            Sale__SaleDate__lt=end_datetime
        )
        .aggregate(
            total_items=Sum('Quantity')
        )
        .get('total_items')
        or 0
    )

    daily_breakdown = (
        sales
        .values('SaleDate__date')
        .annotate(
            invoice_count=Count('SaleId'),
            sales_amount=Sum('TotalAmount')
        )
        .order_by('SaleDate__date')
    )

    return render(
        request,
        'inventory/monthly_sales_report.html',
        {
            'sales': sales,
            'daily_breakdown': daily_breakdown,
            'year': year,
            'month': month,
            'month_name': calendar.month_name[
                month
            ],
            'total_sales': (
                summary.get(
                    'total_sales'
                )
                or 0
            ),
            'total_invoices': (
                summary.get(
                    'total_invoices'
                )
                or 0
            ),
            'total_items': total_items,
        }
    )


# ============================================================
# YEARLY SALES REPORT
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def yearly_sales_report(request):

    current_year = (
        timezone.localdate().year
    )

    try:

        year = int(
            request.GET.get(
                'year',
                current_year
            )
        )

    except (ValueError, TypeError):

        year = current_year

    sales = (
        Sale.objects
        .filter(
            SaleDate__year=year
        )
        .select_related('Customer')
        .prefetch_related(
            'details__Product'
        )
        .order_by('SaleDate')
    )

    summary = sales.aggregate(
        total_sales=Sum('TotalAmount'),
        total_invoices=Count('SaleId')
    )

    total_items = (
        SaleDetail.objects
        .filter(
            Sale__SaleDate__year=year
        )
        .aggregate(
            total_items=Sum('Quantity')
        )
        .get('total_items')
        or 0
    )

    monthly_breakdown = (
        sales
        .values(
            'SaleDate__year',
            'SaleDate__month'
        )
        .annotate(
            invoice_count=Count('SaleId'),
            sales_amount=Sum('TotalAmount')
        )
        .order_by('SaleDate__month')
    )

    return render(
        request,
        'inventory/yearly_sales_report.html',
        {
            'sales': sales,
            'monthly_breakdown': monthly_breakdown,
            'year': year,
            'total_sales': (
                summary.get(
                    'total_sales'
                )
                or 0
            ),
            'total_invoices': (
                summary.get(
                    'total_invoices'
                )
                or 0
            ),
            'total_items': total_items,
        }
    )


# ============================================================
# INVENTORY REPORT
# FR7.4
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def inventory_report(request):

    products = list(
        Product.objects
        .filter(Status='Active')
        .select_related('Category')
        .order_by('Name')
    )

    # --------------------------------------------------------
    # STOCK VALUE
    # --------------------------------------------------------

    for product in products:

        product.StockValue = (
            (product.CostPrice or 0)
            * product.CurrentStock
        )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    total_products = len(
        products
    )

    total_stock_quantity = sum(
        product.CurrentStock
        for product in products
    )

    total_inventory_cost = sum(
        product.StockValue
        for product in products
    )

    total_inventory_sales_value = sum(
        (product.UnitPrice or 0)
        * product.CurrentStock
        for product in products
    )

    # --------------------------------------------------------
    # LOW STOCK PRODUCTS
    # --------------------------------------------------------

    low_stock_products = [
        product
        for product in products
        if product.CurrentStock <= 5
    ]

    return render(
        request,
        'inventory/inventory_report.html',
        {
            'products': products,
            'total_products': total_products,
            'total_stock_quantity': (
                total_stock_quantity
            ),
            'total_inventory_cost': (
                total_inventory_cost
            ),
            'total_inventory_sales_value': (
                total_inventory_sales_value
            ),
            'low_stock_products': (
                low_stock_products
            ),
        }
    )


# ============================================================
# PROFIT / LOSS REPORT
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def profit_loss_report(request):

    # --------------------------------------------------------
    # SELECT YEAR
    # --------------------------------------------------------

    current_year = (
        timezone.now().year
    )

    try:

        selected_year = int(
            request.GET.get(
                'year',
                current_year
            )
        )

    except (TypeError, ValueError):

        selected_year = current_year

    # --------------------------------------------------------
    # SALES
    # --------------------------------------------------------

    sales = (
        Sale.objects
        .filter(
            SaleDate__year=selected_year
        )
        .prefetch_related(
            'details__Product'
        )
    )

    total_sales_revenue = 0
    total_cost_of_goods_sold = 0

    for sale in sales:

        for detail in sale.details.all():

            selling_total = (
                detail.Total
                or 0
            )

            cost_total = (
                (detail.Product.CostPrice or 0)
                * detail.Quantity
            )

            total_sales_revenue += (
                selling_total
            )

            total_cost_of_goods_sold += (
                cost_total
            )

    # --------------------------------------------------------
    # RETURNS
    # --------------------------------------------------------

    sale_returns = (
        SaleReturn.objects
        .filter(
            ReturnDate__year=selected_year
        )
        .prefetch_related(
            'details__SaleDetail__Product'
        )
    )

    total_returns = 0
    returned_cost = 0

    for sale_return in sale_returns:

        for detail in sale_return.details.all():

            total_returns += (
                detail.RefundAmount
                or 0
            )

            returned_cost += (
                (
                    detail.SaleDetail.Product.CostPrice
                    or 0
                )
                * detail.Quantity
            )

    # --------------------------------------------------------
    # NET VALUES
    # --------------------------------------------------------

    net_sales = (
        total_sales_revenue
        - total_returns
    )

    net_cost_of_goods_sold = (
        total_cost_of_goods_sold
        - returned_cost
    )

    gross_profit = (
        net_sales
        - net_cost_of_goods_sold
    )

    # --------------------------------------------------------
    # PROFIT MARGIN
    # --------------------------------------------------------

    if net_sales > 0:

        profit_margin = (
            gross_profit
            / net_sales
        ) * 100

    else:

        profit_margin = 0

    return render(
        request,
        'inventory/profit_loss_report.html',
        {
            'selected_year': selected_year,
            'total_sales_revenue': (
                total_sales_revenue
            ),
            'total_cost_of_goods_sold': (
                total_cost_of_goods_sold
            ),
            'total_returns': total_returns,
            'returned_cost': returned_cost,
            'net_sales': net_sales,
            'net_cost_of_goods_sold': (
                net_cost_of_goods_sold
            ),
            'gross_profit': gross_profit,
            'profit_margin': profit_margin,
        }
    )


# ============================================================
# FR10.3 - ACTIVITY LOG LIST
# ADMIN + MANAGER
# ============================================================

@login_required(login_url='/')
@user_passes_test(is_management, login_url='/')
def activity_log_list(request):

    logs = (
        ActivityLog.objects
        .select_related('User')
        .order_by('-CreatedAt')
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        logs = logs.filter(
            Q(User__username__icontains=search)
            |
            Q(Action__icontains=search)
            |
            Q(Module__icontains=search)
            |
            Q(Description__icontains=search)
        )

    action = request.GET.get(
        'action',
        ''
    ).strip()

    if action:

        logs = logs.filter(
            Action=action
        )

    module = request.GET.get(
        'module',
        ''
    ).strip()

    if module:

        logs = logs.filter(
            Module=module
        )

    actions = (
        ActivityLog.objects
        .values_list(
            'Action',
            flat=True
        )
        .distinct()
        .order_by('Action')
    )

    modules = (
        ActivityLog.objects
        .exclude(
            Module=''
        )
        .values_list(
            'Module',
            flat=True
        )
        .distinct()
        .order_by('Module')
    )

    context = {
        'logs': logs,
        'actions': actions,
        'modules': modules,
        'search': search,
        'selected_action': action,
        'selected_module': module,
    }

    return render(
        request,
        'inventory/activity_log.html',
        context
    )


# selling value fetch view

@login_required(login_url='/')
@user_passes_test(is_product_access, login_url='/')
def product_price(request):
    product_id = request.GET.get('product_id')

    product = get_object_or_404(
        Product,
        ProductId=product_id,
        Status='Active'
    )

    return JsonResponse({
        'price': str(product.UnitPrice)
    })




# ============================================================
# DATABASE BACKUP PAGE
# ADMIN ONLY
# Template is located in the accounts app.
# ============================================================

@login_required(login_url='/')
@user_passes_test(
    lambda user: (
        user.is_authenticated
        and getattr(user, 'role', None) == 'ADMIN'
    ),
    login_url='/'
)
def backup_page(request):
    return render(
        request,
        'accounts/admin-backup.html'
    )


# ============================================================
# DATABASE BACKUP DOWNLOAD
# ADMIN ONLY
# Downloads a MySQL database backup as an SQL file.
# ============================================================

@login_required(login_url='/')
@user_passes_test(
    lambda user: (
        user.is_authenticated
        and getattr(user, 'role', None) == 'ADMIN'
    ),
    login_url='/'
)
def admin_backup(request):

    from django.http import HttpResponseNotAllowed

    # Allow downloads only through the backup form.
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    db_settings = settings.DATABASES['default']

    # Confirm that the configured database is MySQL.
    if 'mysql' not in db_settings.get('ENGINE', '').lower():
        return HttpResponse(
            'Database backup is configured for MySQL only.',
            status=400
        )

    database_name = db_settings.get('NAME')

    if not database_name:
        return HttpResponse(
            'The MySQL database name is not configured.',
            status=500
        )

    mysqldump_path = shutil.which('mysqldump')

    if not mysqldump_path:
        return HttpResponse(
            'mysqldump was not found. Add the MySQL Server bin '
            'directory to your Windows PATH.',
            status=503
        )

    def option_value(value):
        value = str(value or '')
        return value.replace('\\', '\\\\').replace('"', '\\"')

    backup_config = None

    try:
        # Create a temporary configuration file for MySQL credentials.
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            suffix='.cnf',
            delete=False
        ) as config_file:

            backup_config = config_file.name

            config_file.write('[client]\n')
            config_file.write(
                f'user="{option_value(db_settings.get("USER"))}"\n'
            )
            config_file.write(
                f'password="{option_value(db_settings.get("PASSWORD"))}"\n'
            )
            config_file.write(
                f'host="{option_value(db_settings.get("HOST") or "localhost")}"\n'
            )

            port = db_settings.get('PORT')

            if port:
                config_file.write(
                    f'port="{option_value(port)}"\n'
                )

        # Generate the SQL backup.
        result = subprocess.run(
            [
                mysqldump_path,
                f'--defaults-extra-file={backup_config}',
                '--single-transaction',
                '--routines',
                '--triggers',
                '--databases',
                str(database_name),
            ],
            capture_output=True,
            timeout=300
        )

        if result.returncode != 0:
            return HttpResponse(
                'Database backup failed. Check the MySQL credentials, '
                'permissions, and mysqldump version.',
                status=500
            )

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        response = HttpResponse(
            result.stdout,
            content_type='application/sql'
        )

        response['Content-Disposition'] = (
            f'attachment; filename="admin_backup_{timestamp}.sql"'
        )
        response['Cache-Control'] = 'no-store'

        return response

    except subprocess.TimeoutExpired:
        return HttpResponse(
            'The backup took too long. Check the database size and try again.',
            status=504
        )

    except OSError:
        return HttpResponse(
            'Unable to run mysqldump. Check your MySQL installation.',
            status=500
        )

    finally:
        if backup_config and os.path.exists(backup_config):
            try:
                os.remove(backup_config)
            except OSError:
                pass
