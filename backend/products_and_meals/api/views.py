from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from products_and_meals.models import Product
from products_and_meals.api.serializers import ProductSerializer

@api_view(['GET', ])
def api_detail_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

@api_view(['PUT', ])
def api_update_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        data = {}
        if serializer.is_valid():
            Product.update_product(
                product_id, 
                serializer.validated_data['name'], 
                serializer.validated_data['protein'],
                serializer.validated_data['fat'],
                serializer.validated_data['carbohydrates'],
                serializer.validated_data['calories_per_hundred_grams']
                )
            data["success"] = "update successful"
            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'],)
def api_delete_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = product.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)

@api_view(['POST'])
def api_create_product_view(request):
    #account = request.user #when we will have users authentication it will work

    product = Product()

    if request.method == 'POST':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            if ('calories_per_hundred_grams' not in serializer.validated_data):
                serializer.validated_data['calories_per_hundred_grams'] = None
            Product.add_product(
                serializer.validated_data['name'],
                serializer.validated_data['calories_per_hundred_grams'],
                serializer.validated_data['protein'],
                serializer.validated_data['carbohydrates'],
                serializer.validated_data['fat'],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
