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
                api_create_mealitem_breakfast_view,
                api_create_mealitem_lunch_view,
                api_create_mealitem_dinner_view
            )

app_name = "products_and_meals"

urlpatterns = [
    #PRODUCT
    path('product/<str:product_name>/', api_detail_product_view, name='product_detail'),
    path('product/<int:product_id>/update/', api_update_product_view, name='product_update'),
    path('product/<int:product_id>/delete/', api_delete_product_view, name='product_delete'),
    path('create_product/', api_create_product_view, name='product_create'),
    #SUMMARY
    path('summary/<int:user_id>/<str:start_date>/<str:end_date>/', api_detail_summary_view, name='summary_detail'),
    #DEMAND
    path('demand/<str:date>/', api_detail_demand_view, name='demand_detail'),
    path('create_demand/', api_create_demand_view, name='demand_create'),
    #MEAL
    path('meal/<int:meal_id>/', api_detail_meal_view, name='meal_detail'),
    path('meal/<int:meal_id>/update/', api_update_meal_view, name='meal_update'),
    path('meal/<int:meal_id>/delete/', api_delete_meal_view, name='meal_delete'),
    path('create_meal/', api_create_meal_view, name='meal_create'),
    #MEAL ITEM
    path('mealitem/<int:meal_item_id>/', api_detail_meal_item_view, name='meal_item_detail'),
    path('mealitem/<int:meal_item_id>/update/', api_update_meal_item_view, name='meal_item_update'),
    path('mealitem/<int:meal_item_id>/delete/', api_delete_meal_item_view, name='meal_item_delete'),
    path('create_mealitem/breakfast/<str:date>/', api_create_mealitem_breakfast_view, name='create_mealitem_breakfast'),
    path('create_mealitem/lunch/<str:date>/', api_create_mealitem_lunch_view, name='create_mealitem_lunch'),
    path('create_mealitem/dinner/<str:date>/', api_create_mealitem_dinner_view, name='create_mealitem_dinner')
]