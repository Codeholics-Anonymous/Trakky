from django.urls import path
from products_and_meals.api.views import (
                api_detail_product_view,
                api_update_product_view,
                api_delete_product_view,
                api_create_product_view,
                api_detail_summary_view,
                api_detail_demand_view,
                api_create_demand_view
            )

app_name = "products_and_meals"

urlpatterns = [
    # PRODUCT URLS
    path('product/<int:product_id>/', api_detail_product_view, name='product_detail'),
    path('product/<int:product_id>/update', api_update_product_view, name='product_update'),
    path('product/<int:product_id>/delete', api_delete_product_view, name='product_delete'),
    path('product/create', api_create_product_view, name='product_create'),
    # SUMMARY URLS
    path('summary/<int:user_id>/<str:start_date>/<str:end_date>/', api_detail_summary_view, name='summary_detail'),
    # DEMAND URLS
    path('demand/<int:user_id>/<str:date>/', api_detail_demand_view, name='demand_detail'),
    path('demand/create/', api_create_demand_view, name='demand_create')
]