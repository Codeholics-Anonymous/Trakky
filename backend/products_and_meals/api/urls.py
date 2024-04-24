from django.urls import path
from products_and_meals.api.views import api_detail_product_view

app_name = "products_and_meals"

urlpatterns = [
    path('<int:product_id>/', api_detail_product_view, name='detail'),
]