from django.urls import path
from products_and_meals.api.views import (
                #PRODUCT
                api_detail_product_view,
                api_update_product_view,
                api_delete_product_view,
                api_create_product_view,
                #SUMMARY
                api_detail_summary_view,
                #DEMAND
                api_detail_demand_view,
                api_create_demand_view,
                #MEAL
                api_detail_meal_view,
                api_update_meal_view,
                api_delete_meal_view,
                api_create_meal_view,
                #MEAL ITEM
                api_detail_meal_item_view,
                api_update_meal_item_view,
                api_delete_meal_item_view,
                api_create_meal_item_view
            )

app_name = "products_and_meals"

urlpatterns = [
    #PRODUCT
    path('product/<int:product_id>/', api_detail_product_view, name='product_detail'),
    path('product/<int:product_id>/update', api_update_product_view, name='product_update'),
    path('product/<int:product_id>/delete', api_delete_product_view, name='product_delete'),
    path('product/create/', api_create_product_view, name='product_create'),
    #SUMMARY
    path('summary/<int:user_id>/<str:start_date>/<str:end_date>/', api_detail_summary_view, name='summary_detail'),
    #DEMAND
    path('demand/<int:user_id>/<str:date>/', api_detail_demand_view, name='demand_detail'),
    path('demand/create/', api_create_demand_view, name='demand_create'),
    #MEAL
    path('meal/<int:meal_id>/', api_detail_meal_view, name='meal_detail'),
    path('meal/<int:meal_id>/update', api_update_meal_view, name='meal_update'),
    path('meal/<int:meal_id>/delete', api_delete_meal_view, name='meal_delete'),
    path('meal/create/', api_create_meal_view, name='meal_create'),
    #MEAL ITEM
    path('meal/item/<int:meal_item_id>', api_detail_meal_item_view, name='meal_item_detail'),
    path('meal/item/<int:meal_item_id>/update', api_update_meal_item_view, name='meal_item_update'),
    path('meal/item/<int:meal_item_id>/delete', api_delete_meal_item_view, name='meal_item_delete'),
    path('meal/item/create', api_create_meal_item_view, name='meal_item_create')
]