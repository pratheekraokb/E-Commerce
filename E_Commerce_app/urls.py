from django.urls import path
from . import views

urlpatterns = [
    # Define your app's URLs here
    path('', views.home, name='home'),

    
    # Add more URLs as needed
]
