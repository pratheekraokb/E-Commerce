from django.shortcuts import render, HttpResponse
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User

# Create your views here.
def adminHome(request):
    return render(request, 'admin_pages/home.html')

def adminProducts(request):
    return render(request, 'admin_pages/products.html')

def adminCompany(request):
    return render(request, 'admin_pages/company.html')

def adminCatSub(request):
    return render(request,'admin_pages/catSubcat.html')


# GET Requests API


# POST Requests API
@csrf_exempt
def user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['username', 'email', 'password', 'first_name', 'last_name']

            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing field: {field}'}, status=400)
            
            username = data['username']
            email = data['email']
            password = data['password']
            first_name = data['first_name']
            last_name = data['last_name']
            phone_number = data.get('phone_number')  
            is_admin = data.get('is_admin', False)
            date_of_birth = data.get('date_of_birth')  
            profile_image = data.get('profile_image')

            if is_admin and not profile_image:
                profile_image = 'user_images/default_admin.png'
            elif not is_admin and not profile_image:
                profile_image = 'user_images/default_user.png'

            user = User.objects.create(
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

            return JsonResponse({'message': 'User created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'POST method required'}, status=405)