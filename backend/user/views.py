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

from utils.user_utils import password_validation

@api_view(['POST'])
def login(request):
    try:
        user = User.objects.get(username=request.data['username'])
    except User.DoesNotExist:
        return Response({"user" : "not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(request.data['password']):
        return Response({"user" : "not found"}, status=status.HTTP_404_NOT_FOUND)
    
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
        if (not password_validation(register_data['password'])):
            return Response({"Password incorrect" : "Please check conditions below", 1 : "Only letters and digits are allowed", 2 : "At least 8 characters", 3 : "Contains at least one digit", 4 : "Contains at least one letter"})
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
        user.delete() # if userprofile information weren't valid, we have to delete user
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
    # 50/20/30 rule - 50% carbohydrates, 20% protein, 30% fat
    protein = (0.2*daily_calory_demand) / 4
    carbohydrates = (0.5*daily_calory_demand) / 4
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
    return Response(data={f"passed for {request.user.username}"})

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # find and delete user token
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'Logout' : 'successful'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# USERPROFILE 

from user.models import UserProfile
from user.serializers import UserProfileSerializer

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

from utils.products_and_meals_utils import find_basic_demand

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_userprofile_view(request):
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(userprofile, request.data)
    if (UserProfile.update_profile(serializer)):
        # update basic demand if user changed something in profile
        basic_demand = find_basic_demand(request.user.id)
        basic_demand.daily_calory_demand = UserProfile.calculate_demand(weight=serializer.validated_data['weight'], height=serializer.validated_data['height'], birth_date=serializer.validated_data['birth_date'], work_type=serializer.validated_data['work_type'], sex=serializer.validated_data['sex'], user_goal=serializer.validated_data['user_goal'])
        basic_demand.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
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