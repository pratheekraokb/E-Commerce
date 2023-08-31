from django.shortcuts import render, HttpResponse

# Create your views here.
def adminHome(request):
    return render(request, 'admin_pages/home.html')

def adminProducts(request):
    return render(request, 'admin_pages/products.html')

def adminCompany(request):
    return render(request, 'admin_pages/company.html')

def adminCatSub(request):
    return render(request,'admin_pages/catSubcat.html')