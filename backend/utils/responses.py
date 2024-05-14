from rest_framework.response import Response
from rest_framework import status

def custom_response(object, message, status_code=status.HTTP_200_OK):
    return Response({object : message}, status=status_code)

def not_found_response():
    return Response(status=status.HTTP_404_NOT_FOUND)