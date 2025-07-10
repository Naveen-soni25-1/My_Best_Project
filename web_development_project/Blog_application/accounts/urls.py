"""Define URL for accounts page"""

from django.urls import path, include
from .import views

app_name =  'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # Registration page
    path('register/', views.register, name='register'),
]