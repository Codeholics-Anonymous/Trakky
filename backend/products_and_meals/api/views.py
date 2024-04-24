from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from products_and_meals.models import Product
from products_and_meals.api.serializers import ProductSerializer


