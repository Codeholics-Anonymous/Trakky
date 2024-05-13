from rest_framework.decorators import api_view
from rest_framework.response import Response 

from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import UserProfile

from products_and_meals.models import Demand
from datetime import date

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
    register_data = request.data['register_data']
    userprofile_data = request.data['userprofile_data']
    register_serializer = UserSerializer(data=register_data)
    userprofile_serializer = UserProfileSerializer(data=userprofile_data)
    
    # REGISTER PART
    if register_serializer.is_valid():
        register_serializer.save()
        user = User.objects.get(username=register_data['username'])
        user.set_password(register_data['password'])
        user.save()
        register_serializer.validated_data['password'] = user.password
        token = Token.objects.create(user=user)
    else:
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # USERPROFILE PART
    if (userprofile_serializer.is_valid()):
        userprofile_serializer.validated_data['user_id'] = user.id
        userprofile_serializer.save()
    else:
        user.delete() # if userprofile information hasn't been entered, we have to delete user
        return Response(userprofile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DEMAND PART BASED ON USERPROFILE INFO
    daily_calory_demand = UserProfile.calculate_demand(
        weight=userprofile_serializer.validated_data['weight'],
        height=userprofile_serializer.validated_data['height'],
        birth_date=userprofile_serializer.validated_data['birth_date'],
        work_type=userprofile_serializer.validated_data['work_type'],
        sex=userprofile_serializer.validated_data['sex'],
        user_goal=userprofile_serializer.validated_data['user_goal']
        )
    # approximated amounts of macros
    # 40/30/30 rule - 40% carbohydrates, 30% protein, 30% fat
    protein = (0.3*daily_calory_demand) / 4
    carbohydrates = (0.4*daily_calory_demand) / 4
    fat = (0.3*daily_calory_demand) / 9
    Demand.create_demand(user_id=user.id, date=date.today(), protein=protein, carbohydrates=carbohydrates, fat=fat, daily_calory_demand=daily_calory_demand)

    return Response({"token" : token.key, "user" : register_serializer.validated_data, "profile" : userprofile_serializer.validated_data})

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
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def api_detail_userprofile_view(request):
    user_id = request.user.id
    try:
        userprofile = UserProfile.objects.get(user_id=user_id)
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
        return Response(serializer.data, status=status.HTTP_200_OK)
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