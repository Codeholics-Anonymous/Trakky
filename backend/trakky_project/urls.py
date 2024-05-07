from django.contrib import admin
from django.urls import path
from django.urls import include

from user import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #REST FRAMEWORK URLS
    path('api/', include('products_and_meals.api.urls', 'products_and_meals_api')),
    #USERPROFILE
    path('user/', include('user.urls', 'user_api')),
    #USER_AUTH URLS
    path('login/', views.login, name='login'),
    path('register/', views.signup, name='register'),
    path('test_token/', views.test_token, name='test_token'),
]
