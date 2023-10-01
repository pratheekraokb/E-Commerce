from django import forms
from .models import Product
from .models import Category, Subcategory, Company, ProductImage
from multiupload.fields import MultiFileField

class ProductForm(forms.Form):
    product_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'id' : "productTitle",
            'class': 'form-control',
            'placeholder': 'eg:- Asus TUFF Lap',
            'name': 'productTitle',
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate choices dynamically from the database when the form is instantiated
        self.fields['categorySelect'].choices += [(category.category_id, category.name) for category in Category.objects.all()]
        self.fields['subcategorySelect'].choices += [(subcategory.subcategory_id, subcategory.name) for subcategory in Subcategory.objects.all()]
        self.fields['companySelect'].choices += [(company.company_id, company.name) for company in Company.objects.all()]
    
   
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 13,
            'cols': 100,
            'placeholder': 'Enter your Product Description here',
            'name': 'productDesc',
            'id': 'productDescription',
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


# class ProductForm(forms.Form):
#     pass
class ProductImageForm(forms.Form):
    additional_images = MultiFileField(
        min_num=1,
        max_num=10,
        max_file_size=1024*1024*5,
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'custom-file-upload',
            'accept': 'image/*',
            'id': 'additionalImages',  # Add the id attribute
            'name': 'additionalImages',  # Add the name attribute
            
            # 'style': 'display: none;',  # Your additional styling
        })
    )


class UserForm(forms.Form):
    first_name = forms.CharField(
        max_length=255,
        label='First Name *',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg:- Virat', 'required': True})
    )
    last_name = forms.CharField(
        max_length=255,
        label='Last Name *',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg:- Kohli', 'required': True})
    )
    email = forms.EmailField(
        label='E-Mail *',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'eg:- viratkohli@gmail.com', 'required': True})
    )
    username = forms.CharField(
        max_length=255,
        label='Username *',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg:- viratkohli', 'required': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'eg:- Viratkohli@18', 'required': True}),
        label='Password *'
    )
    confirmpassword = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'eg:- Viratkohli@18', 'required': True}),
        label='Confirm Password *'
    )
    contact_number = forms.CharField(
        max_length=20,
        required=False,
        label='Contact Number',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg:- 8547120204'})
    )
    dateofbirth = forms.DateField(
        required=False,
        label='Date of Birth',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    admin = forms.ChoiceField(
        choices=[('1', 'Yes'), ('0', 'No')],
        widget=forms.RadioSelect(attrs={'class': 'custom-radio'}),
        label='Are you Admin?',
        initial='0'  # Set an initial value if needed
    )
    profile_image = forms.FileField(
        required=False,
        label='Profile Image',
        widget=forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'})
    )

    # Custom validation for password match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmpassword = cleaned_data.get('confirmpassword')

        if password != confirmpassword:
            self.add_error('confirmpassword', 'Passwords do not match.')
