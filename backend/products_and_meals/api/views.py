from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from products_and_meals.models import Product
from products_and_meals.api.serializers import ProductSerializer

@api_view(['GET', ])
def api_detail_product_view(request, slug):
    try:
        product = Product.objects.get(product_id=slug)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)