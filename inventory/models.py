from django.db import models
from django.conf import settings

# ============================================================
# CATEGORY
# ============================================================

class Category(models.Model):

    CT_Id = models.AutoField(
        primary_key=True
    )

    Name = models.CharField(
        max_length=100,
        unique=True
    )

    Description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'category'
        ordering = ['Name']

    def __str__(self):
        return self.Name


# ============================================================
# PRODUCT
# ============================================================

class Product(models.Model):

    ProductId = models.AutoField(
        primary_key=True
    )

    Name = models.CharField(
        max_length=150
    )

    Barcode = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )

    CostPrice = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    UnitPrice = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    CurrentStock = models.PositiveIntegerField(
        default=0
    )

    Status = models.CharField(
        max_length=30,
        default='Active'
    )

    Category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )

    class Meta:
        db_table = 'product'
        ordering = ['Name']

    def __str__(self):
        return self.Name


# ============================================================
# SUPPLIER
# ============================================================

class Supplier(models.Model):

    SupplierId = models.AutoField(
        primary_key=True
    )

    Name = models.CharField(
        max_length=150
    )

    Phone = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    Email = models.EmailField(
        blank=True,
        null=True
    )

    Address = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'supplier'
        ordering = ['Name']

    def __str__(self):
        return self.Name


# ============================================================
# STOCK ENTRY
# ============================================================

class StockEntry(models.Model):

    SE_Id = models.AutoField(
        primary_key=True
    )

    Supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='stock_entries'
    )

    EntryDate = models.DateTimeField(
        auto_now_add=True
    )

    Cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    Remarks = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'stock_entry'

    def __str__(self):
        return f"Stock Entry #{self.SE_Id}"


# ============================================================
# STOCK ENTRY DETAIL
# ============================================================

class StockEntryDetail(models.Model):

    SED_Id = models.AutoField(
        primary_key=True
    )

    StockEntry = models.ForeignKey(
        StockEntry,
        on_delete=models.CASCADE,
        related_name='details'
    )

    Product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='stock_entry_details'
    )

    Quantity = models.PositiveIntegerField()

    PurchasePrice = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        db_table = 'stock_entry_detail'

    def __str__(self):
        return f"{self.Product.Name} - {self.Quantity}"


# ============================================================
# CUSTOMER
# ============================================================

class Customer(models.Model):

    CustomerId = models.AutoField(
        primary_key=True
    )

    Name = models.CharField(
        max_length=150
    )

    Phone = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    Email = models.EmailField(
        blank=True,
        null=True
    )

    Address = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'customer'
        ordering = ['Name']

    def __str__(self):
        return self.Name


# ============================================================
# SALE
# ============================================================

class Sale(models.Model):

    SaleId = models.AutoField(
        primary_key=True
    )

    Customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='sales'
    )

    SaleDate = models.DateTimeField(
        auto_now_add=True
    )

    TotalAmount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    Remarks = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'sale'
        ordering = ['-SaleDate']

    def __str__(self):
        return f"Sale #{self.SaleId}"


# ============================================================
# SALE DETAIL
# ============================================================

class SaleDetail(models.Model):

    SaleDetailId = models.AutoField(
        primary_key=True
    )

    Sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='details'
    )

    Product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='sale_details'
    )

    Quantity = models.PositiveIntegerField()

    SellingPrice = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    Total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'sale_detail'

    def __str__(self):
        return f"{self.Product.Name} - {self.Quantity}"


# ============================================================
# SALES RETURN MODULE
# ============================================================

class SaleReturn(models.Model):
    ReturnId = models.AutoField(primary_key=True)

    Sale = models.ForeignKey(
        Sale,
        on_delete=models.PROTECT,
        related_name='returns'
    )

    ReturnDate = models.DateTimeField(
        auto_now_add=True
    )

    TotalAmount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    Remarks = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'sale_return'
        ordering = ['-ReturnDate']

    def __str__(self):
        return f"Return #{self.ReturnId}"


class SaleReturnDetail(models.Model):
    ReturnDetailId = models.AutoField(primary_key=True)

    SaleReturn = models.ForeignKey(
        SaleReturn,
        on_delete=models.CASCADE,
        related_name='details'
    )

    SaleDetail = models.ForeignKey(
        SaleDetail,
        on_delete=models.PROTECT,
        related_name='return_details'
    )

    Quantity = models.PositiveIntegerField()

    RefundAmount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'sale_return_detail'

    def __str__(self):
        return (
            f"{self.SaleDetail.Product.Name} - "
            f"{self.Quantity}"
        )



# ============================================================
# ACTIVITY LOG
# FR10.3 - USER ACTION TRACKING
# ============================================================

class ActivityLog(models.Model):

    LogId = models.AutoField(
        primary_key=True
    )

    User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_logs'
    )

    Action = models.CharField(
        max_length=100
    )

    Module = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    Description = models.TextField(
        blank=True,
        null=True
    )

    IPAddress = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    CreatedAt = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'activity_log'
        ordering = ['-CreatedAt']

    def __str__(self):
        if self.User:
            return f"{self.User.username} - {self.Action}"
        return f"System - {self.Action}"