from django.contrib import admin
from django.urls import path, include
from files.views import home, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('files/', include('files.urls')),  # Include the app's URLs
    path('', home, name='home'),  # Home page
    path('accounts/register/', register, name='register'),  # Add the registration URL
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
]