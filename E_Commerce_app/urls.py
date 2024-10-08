from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    # Define your app's URLs here
    path('', views.productsHome, name='productsHome'),
    path('signIn', views.signIn, name='signIn'),
    path('signUp', views.signUp, name='signUp'),

    path('subcategory/<int:subcategory_id>', views.viewSubCategory, name="viewSubCategory"),

    path('about/', views.aboutus, name="aboutus"),
    path('profile/', views.profile, name="profile"),
    path('profile/personalDetails/', views.profilePersonal, name="profilePersonal"),
    path('myorders/', views.myorders, name="myorders"),
    path('bill/<int:order_id>/', views.generateBill, name='generateBill'),

    path('adminSector', views.adminHome, name='adminHome'),
    path('adminSector/products', views.adminProducts, name="adminProducts"),
    path('adminSector/company', views.adminCompany, name="adminCompany"),
    path('adminSector/catSubcat', views.adminCatSub, name="adminCatSub"),
    path('adminSector/stats', views.statsPage, name="statsPage"),
    # User
    path('api/create_user', views.create_user, name='create-user-api'),
    path('api/update_user', views.edit_user, name='edit-user-api'),
    path('api/delete_user/<int:user_id>/', views.delete_user, name='delete-user-api'),

    path('api/check_email/', views.check_email, name='check_email'),
    path('api/check_username/', views.check_username, name='check_username'),

    # Product
    path('api/create_product', views.create_product, name='create-product'),
    path('api/update_product/<int:product_id>', views.update_product, name='update-product'),
    path('api/delete_product/<int:product_id>/', views.delete_product, name='delete-product-api'),
    path('api/create_category', views.create_category, name='create-category'),
    path('api/create_subcategory', views.create_subcategory, name='create-subcategory'),
    path('api/create_company', views.create_company, name='create-company'),

    path('api/submit_order/', views.submit_order, name='submit_order'),

    path('api/stats/category/', views.statsCategory, name="statsCategory"),
    path('api/stats/company/', views.statsCompany, name='statsCompany'),
    path('api/stats/amountWiseSales/', views.statsSales, name='statsSales'),
    # path('api/downloadBill/<int:orderid>/', views.downloadBill, name='downloadBill'),
    # Comment

    path('api/add_comment', views.add_comment, name='add-comment'),
    # path('api/retrieve_comment/<int:product_id>', views.retrieve_comment, name='retrieve-comment'),
    # GET
    path('api/get_categories', views.get_categories, name='get_categories'),
    path('api/get_subcategory/<int:category_id>', views.get_subcategories, name='get_subcategories_api'),
    path('api/get_companies', views.get_companies, name='get_companies_api'),
    path('api/get_companies/<int:comp_id>', views.get_companies_by_id, name='get_companiesById_api'),
    path('api/alter_company', views.alter_company, name='alter-company'),

    path('api/authenticate_upi/', views.authenticate_upi, name="authenticateUPI"),
    # path('home', views.usersHome, name='usersHome'),
    path('ml/<str:title>/<str:description>/', views.MLPredict, name='MLPredict'),

    path('login', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),  # Add this line for logout
    # path('add_product/', views.add_product, name='add_product'),

    
    path('product/<int:product_num>', views.product_display, name="product_display"),
    path('mycart/', views.mycart_page, name='mycart_page'),
    
    path('billing/', views.billing, name='billing'),

    path('chatbot/', views.chatbot, name="chatbot"),
    path('help/', views.help, name="help"),
    path('product_catelogue/', views.product_catelogue, name="product_catelogue"),
]
