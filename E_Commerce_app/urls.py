from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    # Define your app's URLs here
    path('adminSector', views.adminHome, name='adminHome'),
    path('adminSector/products', views.adminProducts, name="adminProducts"),
    path('adminSector/company', views.adminCompany, name="adminCompany"),
    path('adminSector/catSubcat', views.adminCatSub, name="adminCatSub"),

    # User
    path('api/create_user', views.create_user, name='create-user-api'),
    path('api/update_user', views.edit_user, name='edit-user-api'),
    path('api/delete_user/<int:user_id>/', views.delete_user, name='delete-user-api'),

    # Product
    path('api/create_product', views.create_product, name='create-product'),
    path('api/update_product/<int:product_id>', views.update_product, name='update-product'),
    path('api/delete_product/<int:product_id>/', views.delete_product, name='delete-product-api'),
    path('api/create_category', views.create_category, name='create-category'),
    path('api/create_subcategory', views.create_subcategory, name='create-subcategory'),
    path('api/create_company', views.create_company, name='create-company'),

    # GET
    path('api/get_categories', views.get_categories, name='get_categories'),
    path('api/get_subcategory/<int:category_id>', views.get_subcategories, name='get_subcategories_api'),
    path('api/get_companies', views.get_companies, name='get_companies_api'),
    # path('add_product/', views.add_product, name='add_product'),

    
    # Add more URLs as needed
]