from django.urls import path
from . import views


app_name = 'inventory'


urlpatterns = [

    # =========================================================
    # PRODUCT URLS
    # =========================================================

    # Product List
    path(
        '',
        views.product_list,
        name='product_list'
    ),

    # Add Product
    path(
        'add/',
        views.product_create,
        name='product_create'
    ),

    # Edit Product
    path(
        'edit/<int:ProductId>/',
        views.product_edit,
        name='product_edit'
    ),

    # Delete Product
    path(
        'delete/<int:ProductId>/',
        views.product_delete,
        name='product_delete'
    ),


    # =========================================================
    # SUPPLIER URLS
    # =========================================================

    # Supplier List
    path(
        'suppliers/',
        views.supplier_list,
        name='supplier_list'
    ),

    # Add Supplier
    path(
        'suppliers/add/',
        views.supplier_create,
        name='supplier_create'
    ),

    # Supplier Transaction History
    path(
        'suppliers/<int:SupplierId>/history/',
        views.supplier_transaction_history,
        name='supplier_transaction_history'
    ),


    # =========================================================
    # STOCK URLS
    # =========================================================

    # Stock Entry List
    path(
        'stock/',
        views.stock_entry_list,
        name='stock_entry_list'
    ),

    # Add Stock Entry
    path(
        'stock/add/',
        views.stock_entry_create,
        name='stock_entry_create'
    ),


    # =========================================================
    # CUSTOMER URLS
    # =========================================================

    # Customer List
    path(
        'customers/',
        views.customer_list,
        name='customer_list'
    ),

    # Add Customer
    path(
        'customers/add/',
        views.customer_create,
        name='customer_create'
    ),

    # Edit Customer
    path(
        'customers/edit/<int:CustomerId>/',
        views.customer_edit,
        name='customer_edit'
    ),

    # Delete Customer
    path(
        'customers/delete/<int:CustomerId>/',
        views.customer_delete,
        name='customer_delete'
    ),

    # Customer Transaction History
    path(
        'customers/<int:CustomerId>/history/',
        views.customer_transaction_history,
        name='customer_transaction_history'
    ),


    # =========================================================
    # SALES URLS
    # =========================================================

    # Sales List
    path(
        'sales/',
        views.sale_list,
        name='sale_list'
    ),

    # Create Sale
    path(
        'sales/add/',
        views.sale_create,
        name='sale_create'
    ),

    # Sale Detail
    path(
        'sales/<int:SaleId>/',
        views.sale_detail,
        name='sale_detail'
    ),

    # Sale Invoice
    path(
        'sales/<int:SaleId>/invoice/',
        views.sale_invoice,
        name='sale_invoice'
    ),

    # Download Sale Invoice
    path(
        'sales/<int:SaleId>/invoice/download/',
        views.sale_invoice_download,
        name='sale_invoice_download'
    ),

    path('product-price/', views.product_price, name='product_price'),

    # =========================================================
    # RETURN URLS
    # =========================================================

    # Create Return
    path(
        'sales/<int:SaleId>/return/',
        views.sale_return_create,
        name='sale_return_create'
    ),

    # Return List
    path(
        'returns/',
        views.sale_return_list,
        name='sale_return_list'
    ),

    # Return Detail
    path(
        'returns/<int:ReturnId>/',
        views.sale_return_detail,
        name='sale_return_detail'
    ),


    # =========================================================
    # REPORT URLS
    # =========================================================

    # Daily Sales Report
    path(
        'reports/daily/',
        views.daily_sales_report,
        name='daily_sales_report'
    ),

    # Monthly Sales Report
    path(
        'reports/monthly/',
        views.monthly_sales_report,
        name='monthly_sales_report'
    ),

    # Yearly Sales Report
    path(
        'reports/yearly/',
        views.yearly_sales_report,
        name='yearly_sales_report'
    ),

    # Inventory Report
    path(
        'reports/inventory/',
        views.inventory_report,
        name='inventory_report'
    ),

    # Profit / Loss Report
    path(
        'reports/profit-loss/',
        views.profit_loss_report,
        name='profit_loss_report'
    ),

    # Invoice Lookup
    path(
        'invoice-lookup/',
        views.invoice_lookup,
        name='invoice_lookup'
    ),


    # =========================================================
    # STOCK HISTORY URL
    # =========================================================

    path(
        'stock-history/',
        views.stock_history,
        name='stock_history'
    ),


    # =========================================================
    # ACTIVITY LOG URL
    # =========================================================

    path(
        'activity-log/',
        views.activity_log_list,
        name='activity_log'
    ),


    path(
        'backup/',
        views.backup_page,
        name='backup_page'
    ),

    path(
        'backup/download/',
        views.admin_backup,
        name='admin_backup'
    ),

]

