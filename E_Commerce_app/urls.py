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

    
    # Add more URLs as needed
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)