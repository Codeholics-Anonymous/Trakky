from django.contrib import admin
from django.urls import path
from django.urls import include

from user import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # PRODUCTS AND MEALS URLS
    path('api/', include('products_and_meals.api.urls', 'products_and_meals_api')),
    # USERPROFILE
    path('user/', include('user.urls', 'user_api')),
    # USER_AUTH URLS
    path('register/', views.signup, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('test_token/', views.test_token, name='test_token'),
]
