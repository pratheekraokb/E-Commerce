from django.shortcuts import render, HttpResponse
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json
from .models import CustomUser, Category, Subcategory, Product, Company, Tag, ProductImage, ProductTag
from django.contrib.auth.hashers import make_password
from django.db import connection
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
from .forms import ProductForm, ProductImageForm, UserForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Order, OrderItem
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from .models import OrderItem
from django.db import IntegrityError
from django.http import JsonResponse
from datetime import datetime

from datetime import datetime

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from django.http import HttpResponse
import nltk
from nltk.tokenize import word_tokenize
import re

import os
from dotenv import load_dotenv
import re
import pytesseract
from PIL import Image

import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from itertools import chain
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Order, OrderItem, Product
from twilio.rest import Client

def extract_upi_transaction_id(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        print(text)
        upi_transaction_id = None
        for word in text.split():
            
            if word == 'UPI':
                match = re.search(r'\b\d{12}\b', text)
                if match:
                    upi_transaction_id = match.group()
                    break
        return upi_transaction_id
    except Exception as e:
        return ""




def retrieveData(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def executeQuery(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            # You can commit the changes here if needed: connection.commit()
            return cursor.fetchall()
    except Exception as e:
        # Handle other general exceptions
        print(f"Error: {e}")
        return None

# Create your views here.
    
def authenticate_upi(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        try:
            # Save the image temporarily
            with open('temp_image.jpg', 'wb') as f:
                f.write(image.read())

            # Extract UPI transaction ID
                
            upi_transaction_id = extract_upi_transaction_id('temp_image.jpg')
            print(upi_transaction_id)
            os.remove('temp_image.jpg')

            return JsonResponse({'upi_transaction_id': upi_transaction_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def adminHome(request):

    return render(request, 'admin_pages/home.html')

def adminProducts(request):
    product_form = ProductForm()
    image_form = ProductImageForm()  # Create an instance of ProductImageForm
    return render(request, 'admin_pages/products.html', {'product_form': product_form, 'image_form': image_form})

def adminCompany(request):
    return render(request, 'admin_pages/company.html')

def adminCatSub(request):
    return render(request,'admin_pages/catSubcat.html')

def signUp(request):
    user_form = UserForm()
    return render(request,'auth_pages/signup.html', {'user_form': user_form})

def signIn(request):
    return render(request,'auth_pages/signin.html' )
def check_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': CustomUser.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': CustomUser.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

# GET Requests API


# POST Requests API

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads

        if form.is_valid():
            # Form is valid, process the data
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = make_password(form.cleaned_data['password'])
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['contact_number']
            is_admin = form.cleaned_data['admin']
            date_of_birth = form.cleaned_data['dateofbirth']

            # Check if profile_image is uploaded, use default if not
            profile_image = form.cleaned_data.get('profile_image')

            # Define default image paths
            default_admin_image = 'shop/users_images/default_admin.png'
            default_user_image = 'shop/users_images/default_user.png'
            # profile_image = profile_image or default_user_image
            
            if(profile_image is None):
                profile_image = default_user_image
   
                
                if(int(is_admin) == 1):
                    profile_image = default_admin_image
              
                
                    
            else:
                profile_image = profile_image
         
            # if is_admin:
            #     profile_image = profile_image or default_admin_image
  

            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                is_staff=is_admin,
                date_of_birth=date_of_birth,
                profile_image=profile_image
            )

            # Redirect to the signIn view on successful user creation
            # sign_in_url = reverse('signIn')  # Generate the URL for the signIn view
            # return redirect(sign_in_url)
            return JsonResponse({'message': 'User created successfully'}, status=201)
        else:
            # Form is not valid, return validation errors as JSON response
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)

    return JsonResponse({'message': 'POST method required'}, status=405)


def edit_user(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            
     
            try:
                user = CustomUser.objects.get(username=username, email=email)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            
        
            if 'password' in data:
                user.password = make_password(data['password'])
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'phone_number' in data:
                user.phone_number = data['phone_number']
            if 'is_admin' in data:
                user.is_admin = data['is_admin']
            if 'date_of_birth' in data:
                user.date_of_birth = data['date_of_birth']
            if 'profile_image' in data:
                user.profile_image = data['profile_image']
            
            user.save()
            
            return JsonResponse({'message': 'User updated successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Unsupported method'}, status=405)


def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Unsupported method'}, status=405)



def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
        
            category_id = form.cleaned_data['categorySelect']
            subcategory_id = form.cleaned_data['subcategorySelect']
            company_id = form.cleaned_data['companySelect']

            category = Category.objects.get(pk=category_id)
            subcategory = Subcategory.objects.get(pk=subcategory_id)
            company = Company.objects.get(pk=company_id)
            new_product = Product(
                name=form.cleaned_data['product_name'],
                description=form.cleaned_data['description'],
                mrp_price=form.cleaned_data['mrp'],
                selling_price=form.cleaned_data['sell_price'],
                stock_quantity=form.cleaned_data['stock'],
                category=category,
                subcategory=subcategory,
                company=company,
                image=form.cleaned_data['file']
            )

            print(new_product)
            new_product.save()
            print("Sucess added product")
            # images = request.FILES.getlist('images')
            tags_data = request.POST.get('tagsData')  
            
            if tags_data is not None:
               
            
                tags_dict = json.loads(tags_data)
                tags_array = list(set(tags_dict.get('tags', [])))
                for tag_name in tags_array:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    ProductTag.objects.create(product=new_product, tag=tag)
                    # print(tags_array)

            print("Tags added")

                
            # print(images)
            additional_images = []
            for i in range(0, 20):  # Assuming you have up to 20 additional image inputs
                file_key = f'additional_images_{i}'
                if file_key in request.FILES:
                    uploaded_file = request.FILES[file_key]
                    
                    additional_images.append(uploaded_file)
            for image in additional_images:
                product_image = ProductImage(product=new_product, image=image)
                product_image.save()

            print("Additional images added")
            
            return JsonResponse({'message': 'Product updated successfully'}, status=200)

def update_product(request, product_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)
            
            name = data.get('name', product.name)
            description = data.get('description', product.description)
            mrp_price = data.get('mrp_price', product.mrp_price)
            selling_price = data.get('selling_price', product.selling_price)
            stock_quantity = data.get('stock_quantity', product.stock_quantity)
            category_id = data.get('category_id', product.category_id)
            company_id = data.get('company_id', product.company_id)
            subcategory_id = data.get('subcategory_id', product.subcategory_id)
            tags = data.get('tags', [])
            main_img = data.get('images', {}).get('main_img', product.image)
            other_img_list = data.get('images', {}).get('other_img', [])
            
            try:
                category = Category.objects.get(pk=category_id)
                company = Company.objects.get(pk=company_id)
                subcategory = Subcategory.objects.get(pk=subcategory_id)
                
                product.name = name
                product.description = description
                product.mrp_price = mrp_price
                product.selling_price = selling_price
                product.stock_quantity = stock_quantity
                product.category = category
                product.company = company
                product.subcategory = subcategory
                product.image = main_img
                product.save()
                
                # Update product tags
                product.producttag_set.all().delete()  # Delete existing tags
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    new_product_tag = ProductTag(product=product, tag=tag)
                    new_product_tag.save()
                
                # Update product images
                product.productimage_set.all().delete()  # Delete existing images
                for other_img_url in other_img_list:
                    product_image = ProductImage(product=product, image=other_img_url)
                    product_image.save()
                
                return JsonResponse({'message': 'Product updated successfully'}, status=200)
            
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)
            except Company.DoesNotExist:
                return JsonResponse({'error': 'Company not found'}, status=404)
            except Subcategory.DoesNotExist:
                return JsonResponse({'error': 'Subcategory not found'}, status=404)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return JsonResponse({'message': 'Product deleted successfully'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Unsupported method'}, status=405)

def create_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        existing_category = Category.objects.filter(name=category_name).first()

        try:
            if existing_category is None:
                # If the category doesn't exist, create a new one
                new_category = Category(name=category_name)
                new_category.save()
                
                # return JsonResponse({"msg": "Success! New category is created."})
         
            return redirect('/adminSector/catSubcat')
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        # return 

    return HttpResponse("Invalid Request Method")

def get_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        category_dict = {category.category_id: category.name for category in categories}
        return JsonResponse(category_dict)

def create_subcategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        subcategory_name = request.POST.get('subcategory_name')
        existing_subcategory = Subcategory.objects.filter(name=subcategory_name, category_id=category_id).first()

        if existing_subcategory:
            pass
        else:
            category = Category.objects.get(pk=category_id)
            new_subcategory = Subcategory(name=subcategory_name, category=category)
            new_subcategory.save()
            
        return redirect('/adminSector/catSubcat')
    return HttpResponse("Invalid Request Method")

def create_company(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_location = request.POST.get('company_location')
        company_phone = request.POST.get('company_phone')
        
        
        # Check if a company with the same name already exists
        existing_company = Company.objects.filter(name=company_name).first()

        if existing_company:
            # A company with the same name already exists, handle this case as needed
            # For example, you might want to display an error message or redirect back to the form
            # Add your handling code here
            pass
        else:
            # Create a new company
            new_company = Company(name=company_name, address=company_location, contact_number=company_phone)
            new_company.save()
            
        return redirect('/adminSector/company')
    
    return HttpResponse("Invalid Request Method")

def get_subcategories(request, category_id):
    if request.method == 'GET':
        subcategories = Subcategory.objects.filter(category_id=category_id)
        subcategory_dict = {subcategory.subcategory_id: subcategory.name for subcategory in subcategories}
        return JsonResponse(subcategory_dict)

def get_companies(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        company_dict = {company.company_id: company.name for company in companies}
        return JsonResponse(company_dict)

def get_companies_by_id(request, comp_id):
    if request.method == 'GET':
        try:
            company = Company.objects.get(company_id=comp_id)
            company_data = {
                'company_id': company.company_id,
                'company_name': company.name,
                'company_location': company.address,
                'company_phone': company.contact_number
            }
            return JsonResponse(company_data)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)

    return HttpResponse("Invalid Request Method")

def alter_company(request):
    if request.method == 'POST':
        company_id = request.POST.get('companyAlter_id')
        company_name_alter = request.POST.get('company_name_alter')
        company_location_alter = request.POST.get('company_location_alter')
        company_phone_alter = request.POST.get('company_phone_alter')
        
        try:
            company = Company.objects.get(company_id=company_id)
            
            # Check which fields have changed and update them
            if company_name_alter:
                company.name = company_name_alter
            if company_location_alter:
                company.address = company_location_alter
            if company_phone_alter:
                company.contact_number = company_phone_alter
            
            company.save()
            
            return redirect('/adminSector/company')
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid Request Method'}, status=400)

@login_required
def productsHome(request):
    if(request.method == "GET"):
        query1 = """
            SELECT
                p.product_id AS product_id,
                p.name AS product_name,
                p.description AS description,
                p.mrp_price AS mrp,
                p.selling_price AS selling_price,
                p.stock_quantity AS stock,
                p.image AS product_image,
                p.company_id AS company_id,
                c.name AS company_name,
                cat.category_id AS category_id,
                cat.name AS category_name,
                subcat.name AS subcategory_name,
                JSON_ARRAYAGG(t.name) AS tags,
                JSON_ARRAYAGG(COALESCE(pi.image, NULL)) AS additional_images,
                subcat.subcategory_id AS subcat_id

            FROM Product AS p
            JOIN Company AS c ON p.company_id = c.company_id
            JOIN Category AS cat ON p.category_id = cat.category_id
            JOIN Subcategory AS subcat ON p.subcategory_id = subcat.subcategory_id
            LEFT JOIN ProductTag AS pt ON p.product_id = pt.product_id
            LEFT JOIN Tag AS t ON pt.tag_id = t.tag_id
            LEFT JOIN ProductImage AS pi ON p.product_id = pi.product_id
            GROUP BY subcat.subcategory_id, p.product_id
            ORDER BY subcat.subcategory_id, p.product_id;
        """
        
        results = retrieveData(query1)  

        json_data = []

        current_subcategory_name = None
        current_category_id = None
        current_category_name = None
        current_subcategory_id = None
        subcategory_product_batch = []  
        subcategory_tags = set() 
        companyArray = set()
        for row in results:
            product_json = {
                "product_id": row[0],
                "product_name": row[1],
                "description": row[2],
                "mrp": int(row[3]),
                "selling_price": int(row[4]),
                "stock": int(row[5]),
                "product_image": row[6],
                "company_id": row[7],
                "company_name": row[8],
                "category_id": row[9],
                "category_name": row[10],
                "subcategory_id": row[14],
                "subcategory_name": row[11],
                "tags": json.loads(row[12]), 
                "additional_images": json.loads(row[13]) if row[13] else []  
            }
            companyArray.add(row[8])
            
            
            


            
            subcategory_tags.update(product_json["tags"])
            if row[10] != current_category_name or row[11] != current_subcategory_name:
                if subcategory_product_batch:
             
                    subcategory_tags_list = list(subcategory_tags)
                    json_data.append({
                        "category_id": current_category_id,  
                        "category_name": current_category_name,
                        "subcategory_name": current_subcategory_name,
                        "subcategory_id": current_subcategory_id,
                        
                        "tags": subcategory_tags_list,
                        "product_list": subcategory_product_batch,
                        
                        
                    })
                current_category_id = row[9]
                current_category_name = row[10]
                # print(current_category_name)
                current_subcategory_id = row[14]
                current_subcategory_name = row[11]
                subcategory_product_batch = [product_json]
                subcategory_tags = set(product_json["tags"]) 
                
                
            else:
                subcategory_product_batch.append(product_json)

        if subcategory_product_batch:
            companyArray = list(companyArray)
            subcategory_tags_list = list(subcategory_tags)
            json_data.append({
                "category_id": current_category_id,  
                "category_name": current_category_name,
                "subcategory_name": current_subcategory_name,
                "subcategory_id": current_subcategory_id,
                "tags": subcategory_tags_list,
                "company": companyArray,
                "product_list": subcategory_product_batch,
            })

        
        for subcategory_data in json_data:
            subcategory_data["product_list"] = [subcategory_data["product_list"][i:i + 4] for i in
                                                range(0, len(subcategory_data["product_list"]), 4)]

        user = request.user

        userData = {
            "userid": int(user.user_id),
            "username": user.username,
            "email": user.email,
            "profile": user.profile_image,
            # "firstName": user.first_name,
            # "lastName": user.last_name,
            # "phoneNumber": user.phone_number,
        }
        # print({"data":json_data,"user_data":userData})
        return render(request,'main_pages/product_home.html',{"data":json_data,"user_data":userData})

   


def user_logout(request):
    logout(request)
    return redirect('/')  # Redirect to the home page or any other desired URL after logout


def user_login(request):
    if request.method == 'POST':
        username = request.POST['usernameSignIn']
        password = request.POST['passwordSignIn']
        
        # Authenticate the user using the provided credentials
        user = authenticate(request, username=username, password=password)
  
        
        if user is not None:
            login(request, user)  # Log in the user
            
            if user.is_staff:
                print("Redirecting to adminSector...")
                return redirect('/adminSector')  # Redirect to admin dashboard
            else:
                print("Redirecting to usersHome...")
                return redirect('/')  # Redirect to regular user page
        else:
            messages.error(request, 'Invalid login attempt. Please check your username and password.')

    return render(request, 'auth_pages/signin.html')  # Replace with your actual template name


def aboutus(request):
    return render(request, "main_pages/about.html")


@login_required
def profile(request):
    user = request.user

    name = user.first_name + " " + user.last_name
    userData = {
        "userid": int(user.user_id),
        "username": user.username,
        "email": user.email,
        "profile": user.profile_image,
        "name": name,
        # "phoneNumber": user.phone_number,
    }
    return render(request,'profile_pages/profile-home.html',{"user_data": userData})

@login_required
def profilePersonal(request):
    user = request.user

    name = user.first_name + " " + user.last_name
    userData = {
        "userid": int(user.user_id),
        "username": user.username,
        "email": user.email,
        "profile": user.profile_image,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "name": name,
        "last_login": user.last_login,
        "phone_number": user.phone_number,
        "date_of_birth": user.date_of_birth,

        # "phoneNumber": user.phone_number,
    }
    return render(request,'profile_pages/profile-personal.html', {"user_data": userData} )

def viewSubCategory(request, subcategory_id):
    if request.method == "GET":
        query = f"""
            SELECT
                p.product_id AS product_id,
                p.name AS product_name,
                p.description AS description,
                p.mrp_price AS mrp,
                p.selling_price AS selling_price,
                p.stock_quantity AS stock,
                p.image AS product_image,
                p.company_id AS company_id,
                c.name AS company_name,
                cat.category_id AS category_id,
                cat.name AS category_name,
                subcat.name AS subcategory_name,
                JSON_ARRAYAGG(t.name) AS tags,
                JSON_ARRAYAGG(COALESCE(pi.image, NULL)) AS additional_images,
                subcat.subcategory_id AS subcat_id
            FROM Product AS p
            JOIN Company AS c ON p.company_id = c.company_id
            JOIN Category AS cat ON p.category_id = cat.category_id
            JOIN Subcategory AS subcat ON p.subcategory_id = subcat.subcategory_id
            LEFT JOIN ProductTag AS pt ON p.product_id = pt.product_id
            LEFT JOIN Tag AS t ON pt.tag_id = t.tag_id
            LEFT JOIN ProductImage AS pi ON p.product_id = pi.product_id
            WHERE subcat.subcategory_id = {subcategory_id}
            GROUP BY subcat.subcategory_id, p.product_id
            ORDER BY subcat.subcategory_id, p.product_id;
        """
        results = retrieveData(query)

        json_data = []

        current_subcategory_name = None
        current_category_id = None
        current_category_name = None
        subcategory_product_batch = []  
        subcategory_tags = set()  
        companyArray = set()

        for row in results:
            product_json = {
                "product_id": row[0],
                "product_name": row[1],
                "description": row[2],
                "mrp": int(row[3]),
                "selling_price": int(row[4]),
                "stock": int(row[5]),
                "product_image": row[6],
                "company_id": row[7],
                "company_name": row[8],
                "category_id": row[9],
                "category_name": row[10],
                "subcategory_id": row[14],
                "subcategory_name": row[11],
                "tags": json.loads(row[12]),  
                "additional_images": json.loads(row[13]) if row[13] else []  
            }

            companyArray.add(row[8])

            subcategory_tags.update(product_json["tags"])

            if row[10] != current_category_name or row[11] != current_subcategory_name:
                if subcategory_product_batch:
                    companyArray = list(companyArray)
                    subcategory_tags_list = list(subcategory_tags)
                    json_data.append({
                        "category_id": current_category_id,  
                        "category_name": current_category_name,
                        "subcategory_name": current_subcategory_name,
                        "tags": subcategory_tags_list,
                        "product_list": subcategory_product_batch,
                        "company": companyArray,
                    })
                current_category_id = row[9]
                current_category_name = row[10]
                # print(current_category_name)
                current_subcategory_name = row[11]
                subcategory_product_batch = [product_json]
                subcategory_tags = set(product_json["tags"])  
            else:
                subcategory_product_batch.append(product_json)

        if subcategory_product_batch:

            subcategory_tags_list = list(subcategory_tags)
            json_data.append({
                "category_id": current_category_id,  
                "category_name": current_category_name,
                "subcategory_name": current_subcategory_name,
                "tags": subcategory_tags_list,
                "product_list": subcategory_product_batch,
                "company": companyArray,
            })


        for subcategory_data in json_data:
            subcategory_data["product_list"] = [subcategory_data["product_list"][i:i + 4] for i in
                                                range(0, len(subcategory_data["product_list"]), 4)]


        # return HttpResponse(json_data)
        # return render(request,'main_pages/product_subcategory.html',{"jsondata":json_data})
        # print(json_data)
        user = request.user

        userData = {
            "userid": int(user.user_id),
            "username": user.username,
            "email": user.email,
            "profile": user.profile_image,
            # "firstName": user.first_name,
            # "lastName": user.last_name,
            # "phoneNumber": user.phone_number,
        }
        return render(request, 'main_pages/product_subcategory.html', {'data': json_data, "user_data":userData})


    return HttpResponse("hai")




def MLPredict(request, title, description):
    try:
        if request.method == "GET":
            query = """
                SELECT P.name, P.description, C.name
                FROM Product P, Category C
                WHERE P.category_id = C.category_id;
            """
            data = retrieveData(query)

            nltk.download('stopwords')
            stop_words = set(stopwords.words('english'))

            # Create a TF-IDF vectorizer
            vectorizer = TfidfVectorizer(stop_words='english')

            # Create a DataFrame from the retrieved data
            df = pd.DataFrame(data, columns=['Name', 'Description', 'Category'])

            # Extract the relevant columns
            products = [(row['Name'], row['Description']) for index, row in df.iterrows()]
            categories = df['Category'].tolist()

     

            # Create TF-IDF features
            X = vectorizer.fit_transform([name + " " + desc for name, desc in products])

            # Encode category labels
            label_encoder = LabelEncoder()
            y = label_encoder.fit_transform(categories)

            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train a Multinomial Naive Bayes classifier
            classifier = MultinomialNB()
            classifier.fit(X_train, y_train)

            # Predict the category for the new product
            new_product = (title, description)
            new_product_features = vectorizer.transform([new_product[0] + " " + new_product[1]])
            predicted_category_id = classifier.predict(new_product_features)
            predicted_category = label_encoder.inverse_transform(predicted_category_id)

            # Calculate the model accuracy on the test set
            y_pred = classifier.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            accuracy = accuracy * 100

            result_category_name = predicted_category[0]
            query = f"""
                SELECT category_id
                FROM Category
                WHERE name='{result_category_name}';
            """
            category_id = retrieveData(query)
            try:
                category_id = category_id[0][0]

            except Exception:
                category_id = None

     
            result = {
                "category_id":category_id,
                "subcategory_id": category_id
            }
            

            return JsonResponse(result)
        else:
            raise Exception("Wrong Request Method: Only GET requests are allowed.")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    

@login_required
def product_display(request, product_num):

    user = request.user

    product_query = f"""
        SELECT P.product_id, P.name, P.description, P.mrp_price, P.selling_price, P.stock_quantity, P.image, C.name as category_name, CO.name as company_name, S.name as subcategory_name
        FROM Product as P, Category as C, Company as CO, Subcategory as S
        WHERE product_id = {product_num} AND P.category_id = C.category_id and P.company_id = CO.company_id and P.subcategory_id = S.subcategory_id;

    """
    result = retrieveData(product_query)
    prod_id = result[0][0]
    prod_name = result[0][1]
    prod_desc = result[0][2]
    prod_mrp = result[0][3]
    prod_sell_price = result[0][4]
    prod_stock = result[0][5]
    prod_main_img = result[0][6]
    prod_category = result[0][7]
    prod_company = result[0][8]
    prod_subcategory = result[0][9]
    
    percent_off = (100 * prod_sell_price)/prod_mrp

    jsonDataToSend = {
        "product_data": {
            "id": prod_id,
            "prod_name" : prod_name,
            "desc" : prod_desc,
            "mrp" : prod_mrp,
            "sell_price" : prod_sell_price,
            "stock" : prod_stock,
            "main_img" : prod_main_img,
            "category": prod_category,
            "company" : prod_company,
            "subcategory" : prod_subcategory,
            "offer_percent" : int(100 - percent_off),
        }
    
    }

    addi_img_query = f"""
        SELECT image 
        FROM ProductImage
        WHERE product_id = {product_num};
    """
    img_array = []
    result = retrieveData(addi_img_query)
    for img in result:
        img_array.append(img[0])
    # print(img_array)
        
    recommend_prod_query = f"""
        SELECT category_id, subcategory_id, company_id
        INTO @category_id, @subcategory_id, @company_id
        FROM Product
        WHERE product_id = {product_num};
    """ 
    retrieveData(recommend_prod_query)

    recommend_prod_query = f"""
        SELECT *
        FROM Product
        WHERE (category_id = @category_id OR subcategory_id = @subcategory_id OR company_id = @company_id)
        AND product_id != {product_num}
        ORDER BY RAND()
        LIMIT 8;
    """
    rec_products= retrieveData(recommend_prod_query)
    # print(rec_products)
    rec_products_list = []
    for prod in rec_products:
        rec_product_data = {
            "id": prod[0],
            "name": prod[1],
            "mrp_price": str(prod[3]),
            "selling_price": str(prod[4]),
            "image": prod[6],
          
        }
        rec_products_list.append(rec_product_data)
    

    userData = {
        "userid": user.user_id,
        "username": user.username,
        "email": user.email,
        "profile": user.profile_image,
    }
    
    all_comments = retrieve_comments_recursive(prod_id)


    
    return render(request,'main_pages/product_display.html', { "user_data": userData ,"product_display": jsonDataToSend, "additional_images": img_array, "retrieve_comments": all_comments, "rec_prods": rec_products_list})


def add_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) 
            

            text = data.get('text', '')
            product_id = data.get('product_id', None)
            user_id = data.get('user_id', None)
            parent_cmnt_id = data.get('parent_cmnt_id', None)
            current_timestamp = datetime.now()
            formatted_timestamp = current_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

       

            if text and product_id is not None and user_id is not None and parent_cmnt_id is None:
                insert_query = f"""
                    INSERT INTO Comment(text,product_id,user_id,timestamp)
                    VALUES ("{text}",{product_id},{user_id},"{formatted_timestamp}");
                """
                # print("hai")
                executeQuery(insert_query)
                return JsonResponse({'message': 'Comment saved successfully'})
            elif text and product_id is not None and user_id is not None and parent_cmnt_id is not None:
                insert_query = f"""
                    INSERT INTO Comment(text,product_id,user_id,timestamp, parent_comment_id)
                    VALUES ("{text}",{product_id},{user_id},"{formatted_timestamp}",{parent_cmnt_id});
                """
                # print("hai")
                executeQuery(insert_query)
                return JsonResponse({'message': 'Comment saved successfully'})
            else:
                return JsonResponse({'error': 'Invalid data provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred while saving the comment'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def is_verified_purchase(product_id, user_id):
    return OrderItem.objects.filter(order__user_id=user_id, product_id=product_id).exists()

def retrieve_comments_recursive(product_id, parent_comment_id=None):
    query1 = f"""
        SELECT C.comment_id, C.text, C.timestamp, C.parent_comment_id, C.user_id, U.username AS user_name, U.profile_image, PC.user_id AS parent_user_id, PU.username AS parent_username
        FROM Comment as C
        JOIN User as U ON U.user_id = C.user_id
        LEFT JOIN Comment as PC ON PC.comment_id = C.parent_comment_id
        LEFT JOIN User as PU ON PU.user_id = PC.user_id
        WHERE C.product_id = {product_id} and C.parent_comment_id {'IS NULL' if parent_comment_id is None else f'= {parent_comment_id}'};
    """



    data = retrieveData(query1)
    comments = []

    for row in data:
        comment_id, text, timestamp, parent_comment_id, user_id, user_name, profile_image, parent_user_id, parent_username = row
        is_verified = is_verified_purchase(product_id, user_id)
        comment = {
            "comment_id": comment_id,
            "text": text,
            "timestamp": str(timestamp),
            "user_id": user_id,
            "user_name": user_name,
            "profile_image": profile_image,
            "parent_user_id": parent_user_id,
            "parent_username": parent_username,
            "is_verified_purchase": is_verified,
            "replies": retrieve_comments_recursive(product_id, comment_id)
        }

        comments.append(comment)
        # print(comment)

    return comments

# To retrieve all comments for a product, call the function with product_id and no parent_comment_id.
@login_required
def mycart_page(request):
    user = request.user

    userData = {
        "userid": int(user.user_id),
        "username": user.username,
        "email": user.email,
         "profile": user.profile_image,
    }
    return render(request, 'main_pages/mycart.html', {"user_data": userData})


def myorders(request):
    user = request.user

    name = user.first_name + " " + user.last_name
    userData = {
        "userid": int(user.user_id),
        "username": user.username,
        "email": user.email,
        "profile": user.profile_image,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "name": name,
        "last_login": user.last_login,
        "phone_number": user.phone_number,
        "date_of_birth": user.date_of_birth,
    }
    orders = Order.objects.filter(user=user)
    order_data = []

    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        order_item_data = []
        for order_item in order_items:
            order_item_data.append({
                'product_id': order_item.product.pk,
                'name': order_item.product.name,
                'quantity': order_item.quantity,
                'subtotal': float(order_item.subtotal),
            })

        order_data.append({
            'order_id': order.order_id,
            'order_date': order.order_date,
            'total_amount': float(order.total_amount),
            'status': order.status,
            'transaction_id': order.transaction_id,
            'address': order.address,
            'items': order_item_data,
        })
    # print({"user_data": userData, "order_data": order_data})

    
    return render(request,"profile_pages/profile-orders.html",  {"user_data": userData, "order_data": order_data})

load_dotenv()

def SendSMS(phone_number_to_send, body_Msg):
    try:
        

        account_sid = 'AC6c882f43f1cda8b2248bf7f2a525d7c2'
        auth_token = '7c8a30dc261c6f205dda22668492ca8c'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='+13343784929',
            body=str(body_Msg),
            to=str(f'+91{phone_number_to_send}')
        )
        print(message.body)

        if message.sid:
            print("SMS message sent successfully")
        else:
            print("Failed to send SMS message")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def SendWhatsapp(phone_number,body_msg):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+13343784929',
        body={body_msg},
        to=f'whatsapp:{phone_number}'
    )
    print(message.sid)


@login_required
def billing(request):
    user = request.user

    userData = {
        "userid": int(user.user_id),
        "username": user.username,
        "email": user.email,
        "profile": user.profile_image,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "phoneNumber": user.phone_number,
    }



    return render(request, 'main_pages/billing.html', {"user_data": userData})


@login_required
@csrf_exempt
def submit_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user = request.user
            # Extract the required fields
            transaction_id = data.get('TransactionId')
            address = data.get('Address')
            total_amount = data.get('TotalAmmount')
            status = data.get('Status')
            user_id = data.get('userId')
            purchased_items = data.get('products_details')

            if not (transaction_id and address and total_amount and status and user_id and purchased_items):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'})

            total_amount = int(total_amount)
            current_datetime = timezone.now()

            order = Order.objects.create(
                user=user,
                order_date=current_datetime,
                total_amount=total_amount,
                status=status,
                transaction_id=transaction_id,
                address=address
            )

            for item in purchased_items:
                product_id = item['id']
                price = item['price']
                quantity = item['quantity']
                subtotal = item['total']
                OrderItem.objects.create(
                    order=order,
                    product_id=product_id,
                    quantity=quantity,
                    subtotal=subtotal,
                    order_date=current_datetime
                )
            print("Hai Testing...")
            # return redirect('/')
            return JsonResponse({'status': 'success', 'message': 'Order submitted successfully', 'msgCode': 1})

            # print(msg)

            # try:
            #     user = request.user
            #     phoneNumber = user.phone_number
            #     email = user.email
            #     username = user.username
            #     name = f"{user.first_name} {user.last_name}"
            #     name = name.upper()
            #     print("Hai testing 2....")

            #     print(user, phoneNumber, email, username, name)
                
            #     msg = f"""
            #         Thank you for shopping with ShopEase. This is your order confirmation.

            #         Order Details:
            #         1. Name: {name}
            #         2. Username: {username}
            #         3. E-Mail: {email}
            #         4. Contact Number: {phoneNumber}

            #         5. Order Transaction Id: {transaction_id}
            #         6. Shipment Address:
            #         {address}
            #         7. Total Amount: {total_amount}.00 RS (INR)

            #         Your satisfaction is our priority. If you have any questions or need assistance, feel free to reach out.

            #         We appreciate your business and look forward to serving you again!

            #         Best regards,
            #         The ShopEase Team
            #     """
            #     # print(msg)
            #     # phoneNumber = f"+91{phoneNumber}"


            #     # SendSMS(phoneNumber, msg)
            #     return JsonResponse({'status': 'success', 'message': 'Order submitted successfully', 'msgCode': 1})
            #     # SendWhatsapp(phoneNumber, msg)
            # except Exception as e:
            #     return JsonResponse({'status': 'error', 'message': f'Order placed but error sending messages: {str(e)}'})

            # return JsonResponse({'status': 'success', 'message': 'Order submitted successfully', 'msgCode': 1})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Something went wrong: {str(e)}'})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
from collections import defaultdict

def statsCategory(request):
    try:
        # Retrieve all OrderItems
        order_items = OrderItem.objects.all()

       
        category_products_count = defaultdict(int)
        subcategory_products_count = defaultdict(int)
        for order_item in order_items:
            category_name = order_item.product.category.name
            subcategory_name = order_item.product.subcategory.name
            category_products_count[category_name] += order_item.quantity
            subcategory_products_count[subcategory_name] += order_item.quantity


        categories = list(category_products_count.keys())
        category_sales = [category_products_count[category_name] for category_name in categories]

        # Extract subcategory names and purchased sales
        subcategories = list(subcategory_products_count.keys())
        subcategory_sales = [subcategory_products_count[subcategory_name] for subcategory_name in subcategories]

        return JsonResponse({'category_wise': [categories, category_sales], 'subcategory_wise': [subcategories, subcategory_sales]}, safe=False)
    except ObjectDoesNotExist as e:
        # Handle the ObjectDoesNotExist exception, for example:
        return JsonResponse({'error': 'Object does not exist'}, status=404)
    except Exception as e:
        # Handle other exceptions, for example:
        return JsonResponse({'error': str(e)}, status=500)
    
def statsCompany(request):
    try:
        order_items = OrderItem.objects.all()
        company_sales_count = defaultdict(int)
        for order_item in order_items:
            product = order_item.product
            company_name = product.company.name
            company_sales_count[company_name] += order_item.quantity
        companies = list(company_sales_count.keys())
        company_sales = [company_sales_count[company_name] for company_name in companies]

        return JsonResponse({'company_wise': [companies, company_sales]}, safe=False)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': 'Object does not exist'}, status=404)
    except Exception as e:

        return JsonResponse({'error': str(e)}, status=500)
    
def statsSales(request):
    try:
        # Initialize counters for different ranges
        below_1000_count = Order.objects.filter(total_amount__lt=1000).count()
        between_1001_5000_count = Order.objects.filter(total_amount__range=(1001, 5000)).count()
        between_5001_10000_count = Order.objects.filter(total_amount__range=(5001, 10000)).count()
        above_10000_count = Order.objects.filter(total_amount__gt=10000).count()

        # Construct labels and values
        labels = ['Below ₹1000', '₹1001 - ₹5000', '₹5001 - ₹10000', '₹10000+']
        values = [below_1000_count, between_1001_5000_count, between_5001_10000_count, above_10000_count]

       
        return JsonResponse({'amnt_wise': [labels, values]}, safe=False)
        
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


import requests
import pdfkit




       
def generateBill(request, order_id):
    try:
        # Retrieve the order details
        order = get_object_or_404(Order, order_id=order_id)
        
        # Retrieve the user details
        user = order.user

        # Retrieve all order items for the given order
        order_items = OrderItem.objects.filter(order=order)
        
        if not order_items:
            return HttpResponse("No items found for this order.", status=404)
        
        # Prepare a list to hold detailed information about each order item
        items_details = []
        totalAmntSaved = 0
        for item in order_items:
            product = item.product
            company = product.company
            
            item_details = {
                'product_name': product.name,
                'mrp_price': product.mrp_price,
                'selling_price': product.selling_price,
                'quantity': item.quantity,
                'subtotal': item.subtotal,
                'company_name': company.name,
                'amount_saved': (product.mrp_price * item.quantity) - (product.selling_price * item.quantity)
            }
            totalAmntSaved += ((product.mrp_price * item.quantity) - (product.selling_price * item.quantity))
            items_details.append(item_details)
        
        # Prepare context for the template
        context = {
            'order': order,
            'order_items': items_details,
            'total_amount': order.total_amount,
            'user_full_name': f"{user.first_name} {user.last_name}",
            'user_phone': user.phone_number,
            'user_email': user.email,
            'amount_saved': totalAmntSaved
        }
        print(context)
        return render(request, "auth_pages/bill.html", context)
    
    except Order.DoesNotExist:
        return HttpResponse("Order not found.", status=404)
    except OrderItem.DoesNotExist:
        return HttpResponse("Order items not found.", status=404)
    except Product.DoesNotExist:
        return HttpResponse("Product not found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
    



def statsPage(request):
    return render(request, 'admin_pages/stats.html')


# Algorthm
# Prepare a set (Unique) which consist of all the words of query seperated by spaces, length of word ? 2
# Then each of this word will be checked if present in 
    # a product title, if yes add 5 points
    # product desc, if yes add 1 points
    # add the score and see if it is greater than or equal to half of lengtth of tokens generated if yess display that product to user
def search_products(query):
    try:
        tokens = [word.lower() for word in word_tokenize(query) if len(word) > 2]

        products = Product.objects.all()

        scored_products = []
        for product in products:
            title_tokens = set(word.lower() for word in word_tokenize(product.name) if len(word) > 2)
            description_tokens = set(word.lower() for word in word_tokenize(product.description) if len(word) > 2)

            title_score = sum(5 for token in tokens if token in title_tokens)
            description_score = sum(1 for token in tokens if token in description_tokens)

            total_score = title_score + description_score
            scored_products.append((product, total_score))

        scored_products.sort(key=lambda x: x[1], reverse=True)

        top_matches = []
        for product, score in scored_products[:5]:
            if not top_matches or score >= (top_matches[0]["algo_score"] / 2)+ 2:
                top_matches.append({"product_name": product.name, "product_id": product.product_id, "algo_score": score})

        return {"result": top_matches, "status_code": 4}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"result": [], "status_code": 0}







def process_query(query):
    if re.search(r'(\w+) under (\d+)', query):
        match = re.search(r'(\w+) under (\d+)', query)
        tag_name = match.group(1)
        max_price = int(match.group(2))
        
        try:
            # Get all products associated with tags containing the tag_name and filter by selling_price
            unique_products = set()
            for product_tag in ProductTag.objects.filter(tag__name__icontains=tag_name):
                if product_tag.product.selling_price <= max_price and len(unique_products) < 5:
                    unique_products.add(product_tag.product)

            products_list = []
            for product in unique_products:
                product_dict = {
                    'product_name': product.name,
                    'product_id': product.product_id,
                    'selling_price': product.selling_price
                }
                products_list.append(product_dict)
            
            return {"result": products_list, "status_code": 1}
        
        except Tag.DoesNotExist:
            return []
    
    elif re.search(r'order (id )?(\d+)', query):
        match = re.search(r'order (id )?(\d+)', query)
        order_id = match.group(2)

        try:
            order = Order.objects.get(order_id=order_id)
            result = {
                "order_id": order.order_id,
                "order_date": order.order_date.date(),
                "total_amount": order.total_amount,
                "address": order.address,
                "status": order.status,
                "text": f"Your order with ID {order.order_id}, placed on {order.order_date.date()}, "
                        f"totaling {order.total_amount}, and shipped to {order.address}, "
                        f"ORDER STATUS is - {order.status}.",
                "link": f"/bill/{order.order_id}/"
                
            }

            return {"result": result, "status_code": 2}
        except Order.DoesNotExist:
            return {"result": "Order not found", "status_code": 0}
        
    elif re.search(r'developers|technical (aspect|side)|about shopease', query, re.IGNORECASE):
        # Provide information about developers or technical aspects
        technical_details = {
            "developers": [
                {"name": "Pratheek Rao K B"},
                {"name": "Jacob George"},
                {"name": "Sarthak Raj M S"},
                {"name": "Parthiv Vinay"}
            ],
            "technical_aspects": {
                "backend": "Django",
                "database": "MySQL",
                "frontend": ["HTML", "CSS", "JavaScript"],
                "features": [
                    "Machine learning for Product Categorization",
                    "Chatbot System",
                    "Dynamic Home Page",
                    "Secure Checkout Process",
                    "Hierarchical Comment Section"
                ]
            },
            "project": "ShopEase",
            "description": "An e-commerce platform combining cutting-edge technology with user-friendly design. Developed as a Mini Project at LBS College Of Engineering, Kasaragod.",
            "Documents": {
                "ER_Diagram": "/media/shop/admin_images/ShopEase_ER_Diagram.png",
                "UML_Diagram": "/media/shop/admin_images/UML_Diagram.png",
                "Flow_Chart": "/media/shop/admin_images/ShopEase_FlowDiagram.png"
            }
        }
        return {"result": technical_details, "status_code": 3}
    
    else:
        search_results = search_products(query)
        print(search_results)
        return {"result": search_results, "status_code": 4}
       






@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            query = body.get('query', '')
            if query:
                response = process_query(query)
                # print(response)
                return JsonResponse(response)
            else:
                return JsonResponse("")
        except json.JSONDecodeError:
            return JsonResponse("")
    else:
        return JsonResponse({'result': [], 'result_status': 0})
    
def help(request):
    return render(request,'main_pages/help.html')


def calculate_discount_percentage(mrp_price, selling_price):
    if mrp_price > 0:
        return round(((mrp_price - selling_price) / mrp_price) * 100)
    return 0


def product_catelogue(request):
    products = Product.objects.select_related('company', 'category', 'subcategory').all()
    product_details = []

    for product in products:
        discount_percentage = calculate_discount_percentage(product.mrp_price, product.selling_price)
        product_details.append({
            'name': product.name,
            'image': product.image.url,
            'mrp_price': product.mrp_price,
            'selling_price': product.selling_price,
            'discount_percentage': discount_percentage,
            'company_name': product.company.name,
            'category_name': product.category.name,
            'subcategory_name': product.subcategory.name
        })

    context = {
        'product_details': product_details
    }
    return render(request, 'main_pages/product_catelogue.html', context)   
    # return render(request, 'product_list.html', context)


    # products = Product.objects.select_related('category', 'subcategory', 'company').all()