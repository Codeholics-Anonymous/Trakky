from django.urls import path
from products_and_meals.api.views import (
                api_detail_product_view,
                api_update_product_view,
                api_delete_product_view,
                api_create_product_view
            )

app_name = "products_and_meals"

urlpatterns = [
    path('<int:product_id>/', api_detail_product_view, name='detail'),
    path('<int:product_id>/update', api_update_product_view, name='update'),
    path('<int:product_id>/delete', api_delete_product_view, name='delete'),
    path('create', api_create_product_view, name='create'),
]