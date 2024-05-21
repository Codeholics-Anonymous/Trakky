from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from .serializers import UserSerializer, UserProfileSerializer
from user.models import UserProfile

from products_and_meals.models import Demand
from products_and_meals.api.serializers import DemandSerializer
from datetime import date

from utils.products_and_meals_utils import find_first_demand, basic_macros

# USER AUTHENTICATION

from utils.user_utils import password_validation

@api_view(['POST'])
def login(request):
    try:
        user = User.objects.get(username=request.data['username'])
    except User.DoesNotExist:
        return Response({"message" : "user not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(request.data['password']):
        return Response({"message" : "user not found"}, status=status.HTTP_404_NOT_FOUND)
    
    token, created = Token.objects.get_or_create(user=user) # get or create token if it hasn't been created yet (f.e. because of user logout).
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
        # check if password satisfies validation
        if (not password_validation(register_data['password'])):
            return Response({"message" : "Password incorrect. Please check conditions below.", 1 : "Only letters and digits are allowed", 2 : "At least 8 characters", 3 : "Contains at least one digit", 4 : "Contains at least one letter"}, status=status.HTTP_400_BAD_REQUEST)

        # create and save user instance
        user = register_serializer.save()

        # hash user password
        user.set_password(register_data['password'])
        user.save()
        register_serializer.validated_data['password'] = user.password

        # generate user token
        token = Token.objects.create(user=user)
    else:
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # USERPROFILE PART
    if (userprofile_serializer.is_valid()):
        # check what is daily_calory_demand basing on info given by user
        daily_calory_demand = UserProfile.calculate_demand(
            weight=userprofile_serializer.validated_data['weight'],
            height=userprofile_serializer.validated_data['height'],
            birth_date=userprofile_serializer.validated_data['birth_date'],
            work_type=userprofile_serializer.validated_data['work_type'],
            sex=userprofile_serializer.validated_data['sex'],
            user_goal=userprofile_serializer.validated_data['user_goal']
            )
        userprofile = UserProfile.objects.create(
            user=user,
            daily_calory_demand = daily_calory_demand,
            **userprofile_serializer.validated_data # unpack dictionary as keyword args
        )
    else:
        user.delete() # if userprofile information weren't valid, we have to delete user
        return Response(userprofile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DEMAND PART BASED ON USERPROFILE INFO
    basic_macros_values = basic_macros(daily_calory_demand)
    protein = basic_macros_values[0]
    carbohydrates = basic_macros_values[1]
    fat = basic_macros_values[2]
    Demand.create_demand(userprofile_id=userprofile.userprofile_id, date=date.today(), protein=protein, carbohydrates=carbohydrates, fat=fat, daily_calory_demand=daily_calory_demand)
 
    return Response({"token" : token.key, "user" : register_serializer.validated_data, "profile" : userprofile_serializer.validated_data})

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(data={f"passed for {request.user.username}"})

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # find and delete user token
        token = Token.objects.get(user=request.user)
        token.delete()
        return short_response("message", "Logout successful")
    except Token.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

from utils.responses import short_response
from products_and_meals.models import Product

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_delete_user_view(request):
    # delete all products added by this user
    products = Product.objects.filter(user_id=request.user.id)
    for x in products:
        x.delete()
    # delete user 
    if (request.user.delete()):
        return short_response("message", "Account deleted")
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# USERPROFILE VIEWS

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_userprofile_view(request):
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(userprofile)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_update_userprofile_view(request):
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(userprofile, request.data)
    if (UserProfile.update_profile(serializer)):
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)