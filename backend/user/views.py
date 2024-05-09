from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 

from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import UserProfile

# USER AUTHENTICATION

@api_view(['POST'])
def login(request):
    try:
        user = User.objects.get(username=request.data['username'])
    except User.DoesNotExist:
        return Response({"user" : "not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(request.data['password']):
        return Response({"user" : "not found"}, status=status.HTTP_404_NOT_FOUND)
    
    token, created = Token.objects.get_or_create(user=user) # get or create token if it wasn't create yet. It returns tuple (token, True/False)
    serializer = UserSerializer(user)
    return Response({"token" : token.key, "user" : serializer.data})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        # create userprofile
        userprofile = UserProfile(user_id=user.id)
        userprofile.save()
        return Response({"token" : token.key, "user" : serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(data={"passed for {}".format(request.user.email)})

# USERPROFILE 

from user.models import UserProfile
from user.serializers import UserProfileSerializer

@api_view(['GET'])
def api_detail_userprofile_view(request, userprofile_id):
    try:
        userprofile = UserProfile.objects.get(userprofile_id=userprofile_id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(userprofile)
    return Response(serializer.data)

@api_view(['PUT'])
def api_update_userprofile_view(request, userprofile_id):
    try:
        userprofile = UserProfile.objects.get(userprofile_id=userprofile_id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(userprofile, request.data)
    if (UserProfile.update_profile(serializer)):
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def api_delete_userprofile_view(request, userprofile_id):
    try:
        userprofile = UserProfile.objects.get(userprofile_id=userprofile_id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    operation = userprofile.delete()
    data = {}
    if operation:
        data['success'] = "deletion successful"
    else:
        data['failure'] = 'deletion failed'
    return Response(data)