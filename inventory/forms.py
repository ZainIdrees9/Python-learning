from django import forms

from .models import (
    Product,
    Supplier,
    StockEntry,
    StockEntryDetail,
    Customer,
    Sale,
    SaleDetail,
)


# ============================================================
# PRODUCT FORM
# ============================================================

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'Name',
            'Barcode',
            'CostPrice',
            'UnitPrice',
            'CurrentStock',
            'Status',
            'Category',
        ]

        widgets = {
            'Name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
            }),

            'Barcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter barcode',
            }),

            'CostPrice': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
            }),

            'UnitPrice': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
            }),

            'CurrentStock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),

            'Status': forms.Select(
                choices=[
                    ('Active', 'Active'),
                    ('Inactive', 'Inactive'),
                ],
                attrs={
                    'class': 'form-select',
                }
            ),

            'Category': forms.Select(attrs={
                'class': 'form-select',
            }),
        }


# ============================================================
# SUPPLIER FORM
# ============================================================

class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier

        fields = [
            'Name',
            'Phone',
            'Email',
            'Address',
        ]

        widgets = {
            'Name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier name',
            }),

            'Phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),

            'Email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
            }),

            'Address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier address',
                'rows': 3,
            }),
        }


# ============================================================
# STOCK ENTRY FORM
# ============================================================

class StockEntryForm(forms.ModelForm):

    class Meta:
        model = StockEntry

        fields = [
            'Supplier',
            'Remarks',
        ]

        widgets = {
            'Supplier': forms.Select(attrs={
                'class': 'form-select',
            }),

            'Remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter remarks (optional)',
                'rows': 3,
            }),
        }


# ============================================================
# STOCK ENTRY DETAIL FORM
# ============================================================

class StockEntryDetailForm(forms.ModelForm):

    class Meta:
        model = StockEntryDetail

        fields = [
            'Product',
            'Quantity',
            'PurchasePrice',
        ]

        widgets = {
            'Product': forms.Select(attrs={
                'class': 'form-select',
            }),

            'Quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Enter quantity',
            }),

            'PurchasePrice': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only active products can receive new stock
        self.fields['Product'].queryset = (
            Product.objects
            .filter(Status='Active')
            .order_by('Name')
        )


# ============================================================
# CUSTOMER FORM
# ============================================================

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

        fields = [
            'Name',
            'Phone',
            'Email',
            'Address',
        ]

        widgets = {
            'Name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer name',
            }),

            'Phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),

            'Email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
            }),

            'Address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter customer address',
            }),
        }


# ============================================================
# SALE FORM
# ============================================================

class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale

        fields = [
            'Customer',
            'Remarks',
        ]

        widgets = {
            'Customer': forms.Select(attrs={
                'class': 'form-select',
            }),

            'Remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter remarks (optional)',
            }),
        }


# ============================================================
# SALE DETAIL FORM
# ============================================================

class SaleDetailForm(forms.ModelForm):

    class Meta:
        model = SaleDetail

        fields = [
            'Product',
            'Quantity',
            'SellingPrice',
        ]

        widgets = {
            'Product': forms.Select(attrs={
                'class': 'form-select',
            }),

            'Quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Enter quantity',
            }),

            'SellingPrice': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only active products can be sold
        self.fields['Product'].queryset = (
            Product.objects
            .filter(Status='Active')
            .order_by('Name')
        )


# ============================================================
# SALE DETAIL FORMSET
# ============================================================

SaleDetailFormSet = forms.inlineformset_factory(
    Sale,
    SaleDetail,
    form=SaleDetailForm,
    extra=1,
    can_delete=True,
)