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
# Create your views here.
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
    return render(request,'user_pages/signup.html', {'user_form': user_form})

def signIn(request):
    return render(request,'user_pages/signin.html' )
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
                print("default user")
                
                if(int(is_admin) == 1):
                    profile_image = default_admin_image
                    print("default admin")
                
                    
            else:
                profile_image = profile_image
                print("custom")
            # if is_admin:
            #     profile_image = profile_image or default_admin_image
  

            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                is_admin=is_admin,
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
            new_product.save()
            # images = request.FILES.getlist('images')
            tags_data = request.POST.get('tagsData')  
            
            if tags_data is not None:
               
            
                tags_dict = json.loads(tags_data)
                tags_array = list(set(tags_dict.get('tags', [])))
                for tag_name in tags_array:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    ProductTag.objects.create(product=new_product, tag=tag)
                    # print(tags_array)

        

                
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
           
            print("bye1")
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
        print(company_name,company_location,company_phone)
        
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

def usersHome(request):
    return HttpResponse("Hello Welcome")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['usernameSignIn']
        password = request.POST['passwordSignIn']
        
        # Authenticate the user using the provided credentials
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log in the user
            
            if user.is_admin:
                return redirect('adminHome')  # Redirect to admin dashboard
            else:
                return redirect('users_home')  # Redirect to regular user page
        else:
            messages.error(request, 'Invalid login attempt. Please check your username and password.')

    return render(request, 'user_pages/signin.html')  # Replace with your actual template name