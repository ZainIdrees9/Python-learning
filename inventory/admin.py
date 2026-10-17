from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'CT_Id',
        'Name',
        'Description',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'ProductId',
        'Name',
        'Barcode',
        'Category',
        'CostPrice',
        'UnitPrice',
        'CurrentStock',
        'Status',
    )

    list_filter = (
        'Category',
        'Status',
    )

    search_fields = (
        'Name',
        'Barcode',
    )