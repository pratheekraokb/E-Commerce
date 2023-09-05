from django import forms
from .models import Product
from .models import Category, Subcategory, Company
class ProductForm(forms.Form):
    product_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'eg:- Asus TUFF Lap',
        })
    )
    mrp = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'eg:- 60000',  # Placeholder for MRP
        })
    )
    sell_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'eg:- 55000',  # Placeholder for Selling Price
        })
    )
    stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'eg:- 5',  # Placeholder for Stock
        })
    )

    categorySelect = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=[('', 'Select a Category')] + [(category.category_id, category.name) for category in Category.objects.all()]
    )

    subcategorySelect = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=[('', 'Select a Sub-Category')] + [(subcategory.subcategory_id, subcategory.name) for subcategory in Subcategory.objects.all()]
    )

    companySelect = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=[('', 'Select a Company')] + [(company.company_id, company.name) for company in Company.objects.all()]
    )
    
   
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 13,
            'cols': 100,
            'placeholder': 'Enter your Product Description here'
        })
    )
    textInput = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tag and press Enter',  # Placeholder for Text Input
        })
    )
    file = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'custom-file-upload',
            'accept': 'image/*',
            
        })
    )
