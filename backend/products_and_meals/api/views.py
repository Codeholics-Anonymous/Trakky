from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from utils.responses import custom_response, not_found_response

from products_and_meals.models import (Product, Summary, Demand, Meal, MealItem)
from products_and_meals.api.serializers import (ProductSerializer, SummarySerializer, DemandSerializer, MealSerializer, MealItemSerializer)
from datetime import datetime, date

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

# PRODUCT VIEWS

from utils.products_and_meals_utils import above_upper_limit

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_product_view(request, product_name):
    product = Product.objects.filter(Q(name__icontains=product_name) & (Q(user_id__isnull=True) | Q(user_id=request.user.id)))
    if (len(product) == 0):
        return not_found_response()

    serializer = ProductSerializer(product, many=True)
    for i in range(len(serializer.data)):
        serializer.data[i]['calories_per_hundred_grams'] = product[i].calories_per_hundred_grams
    return Response(serializer.data, status=status.HTTP_200_OK)

from utils.products_and_meals_utils import find_mealitems

@api_view(['PUT'])
def api_update_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return not_found_response()

    if (product.user_id != request.user.id): # user can edit only products that were created by him
        return custom_response("Product", "cannot be edited", status.HTTP_400_BAD_REQUEST)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        # find userprofile to update summary later
        userprofile_id = UserProfile.objects.get(user_id=request.user.id).userprofile_id
        # check if sum of macros isn't larger than 100g
        if above_upper_limit(serializer.validated_data['protein'], serializer.validated_data['carbohydrates'], serializer.validated_data['fat'], limit=100):
            return custom_response("Macros", f"amount to high ({serializer.validated_data['protein'] + serializer.validated_data['carbohydrates'] + serializer.validated_data['fat']}/{100})", status.HTTP_400_BAD_REQUEST) 
        # update today summary if this product was added (optimization - don't update past summaries)
        mealitems = find_mealitems(user_id=request.user.id, product_id=product_id, date=date.today()) # amount of products added today to summary
        mealitems_amount = len(mealitems)
        if (mealitems_amount != 0):
            # calculate product amount (grams)
            mealitems_gram_amount = 0
            for x in mealitems:
                mealitems_gram_amount += x.gram_amount
            # call function to calculate how many protein, carbohydrates and fat we have (using information about grams of product)
            all_product_macros = Product.calculate_nutrition(gram_amount=mealitems_gram_amount, product=product)
            # subtract calories, because past macros and calories of product aren't current
            Summary.update_calories( 
                userprofile_id=userprofile_id, 
                increase=0, 
                protein=all_product_macros[0], 
                carbohydrates=all_product_macros[1], 
                fat=all_product_macros[2], 
                date=date.today()
                )
        # update product information provided by user
        updated_product = Product.update_product(
            product_id=product_id, 
            name=serializer.validated_data['name'], 
            protein=serializer.validated_data['protein'],
            fat=serializer.validated_data['fat'],
            carbohydrates=serializer.validated_data['carbohydrates']
            )
        # after product update, we have to increase number of calories and macros in summary
        all_updated_product_macros = Product.calculate_nutrition(gram_amount=mealitems_gram_amount, product=updated_product)
        Summary.update_calories(
            userprofile_id=userprofile_id, 
            increase=1, 
            protein=all_updated_product_macros[0],
            carbohydrates=all_updated_product_macros[1],
            fat=all_updated_product_macros[2],
            date=date.today())
        return custom_response("Success", "update successful")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'],)
def api_delete_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return not_found_response()

    operation = product.delete()
    data = {}
    if operation:
        return custom_response("Success", "deletion successful")
    else:
        return custom_response("Failure", "deletion failed", status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_product_view(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        # check if this product exists in database
        if Product.objects.filter(name=serializer.validated_data['name']).exists():
            return custom_response("Product", "already exists")
        # check if sum of macros amount isn't larger than 100g
        if above_upper_limit(serializer.validated_data['protein'], serializer.validated_data['carbohydrates'], serializer.validated_data['fat'], limit=100):
            return custom_response("Macros", f"amount to high ({serializer.validated_data['protein'] + serializer.validated_data['carbohydrates'] + serializer.validated_data['fat']}/{100})", status.HTTP_400_BAD_REQUEST)
        # add product
        added_product = Product.add_product(
            user_id=request.user.id,
            name=serializer.validated_data['name'],
            protein=serializer.validated_data['protein'],
            carbohydrates=serializer.validated_data['carbohydrates'],
            fat=serializer.validated_data['fat'],
        )
        data = serializer.validated_data|{'calories_per_hundred_grams' : added_product.calories_per_hundred_grams}
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# SUMMARY VIEWS

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_summary_view(request, starting_date, ending_date):
    userprofile_id = UserProfile.objects.get(user_id=request.user.id).userprofile_id
    summaries = Summary.objects.filter(userprofile_id=userprofile_id, date__range=(starting_date, ending_date))

    d_start = datetime.strptime(starting_date, "%Y-%m-%d")
    d_end = datetime.strptime(ending_date, "%Y-%m-%d")

    if (d_start > d_end):
        return custom_response("Data", "range is incorrect", status.HTTP_400_BAD_REQUEST)

    # empty summaries aren't store in database but we don't need to imitate they exist (anyway they will be included as 0)
    calories_sum = 0
    protein_sum = 0
    carbohydrates_sum = 0
    fat_sum = 0
    for x in summaries:
        calories_sum += x.daily_calory_intake
        protein_sum += x.protein
        carbohydrates_sum += x.carbohydrates
        fat_sum += x.fat

    return Response({'calories_sum' : round(calories_sum), 'protein_sum' : round(protein_sum, 1), 'carbohydrates_sum' : round(carbohydrates_sum, 1), 'fat_sum' : round(fat_sum, 1)})

# DEMAND VIEWS
# ways to create demand:
# 1 option - we are creating demand basing on data that user gave us during registration 
# 2 option - user can set his demand by himself (by giving us protein, carbohydrates, fat and calories) (this option is presented below)

from utils.date import calculate_days_difference, date_validation

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_demand_view(request, starting_date, ending_date):
    userprofile_id = UserProfile.objects.get(user_id=user_id).userprofile_id
    date_validation(starting_date, ending_date)
    # check first demand existence
    beginning_demand = None
    beginning_demand = Demand.objects.filter(userprofile_id=userprofile_id, date__lte=starting_date).order_by('-date').first()
    if beginning_demand is None:
        return custom_response("No information", "about demand for the selected period", status.HTTP_404_NOT_FOUND)
    # find all demands
    other_demands = Demand.objects.filter(userprofile_id=userprofile_id, date__gt=starting_date, date__lte=ending_date)
    all_demands = [beginning_demand,] + [_ for _ in other_demands]
    # calculate calories, protein, carbohydrates and fat sum
    demand_calories_sum = 0
    demand_protein_sum = 0
    demand_carbohydrates_sum = 0
    demand_fat_sum = 0
    if (len(all_demands) == 1): # case when starting_date and ending_date are all in one demand
        days_difference = calculate_days_difference(starting_date, ending_date)
        demand_calories_sum = days_difference*all_demands[0].daily_calory_demand
        demand_protein_sum = days_difference*all_demands[0].protein
        demand_carbohydrates_sum = days_difference*all_demands[0].carbohydrates
        demand_fat_sum = days_difference*all_demands[0].fat
    else: # we have to check more than one demand
        # firstly - calculate from starting date to date of second demand
        days_difference = calculate_days_difference(starting_date, all_demands[1].date) - 1
        demand_calories_sum += days_difference*all_demands[0].daily_calory_demand
        demand_protein_sum += days_difference*all_demands[0].protein
        demand_carbohydrates_sum += days_difference*all_demands[0].carbohydrates
        demand_fat_sum += days_difference*all_demands[0].fat
        # now - calculate indirect demands between starting and ending date
        for i in range(1, len(all_demands) - 1):
            days_difference = calculate_days_difference(all_demands[i].date, all_demands[i+1].date) - 1
            demand_calories_sum += days_difference*all_demands[i].daily_calory_demand
            demand_protein_sum += days_difference*all_demands[i].protein
            demand_carbohydrates_sum += days_difference*all_demands[i].carbohydrates
            demand_fat_sum += days_difference*all_demands[i].fat
        # lastly - calculate demand from date of last demand up to ending_date
        days_difference = calculate_days_difference(all_demands[len(all_demands) - 1].date, ending_date)
        demand_calories_sum += days_difference*all_demands[len(all_demands) - 1].daily_calory_demand
        demand_protein_sum += days_difference*all_demands[len(all_demands) - 1].protein
        demand_carbohydrates_sum += days_difference*all_demands[len(all_demands) - 1].carbohydrates
        demand_fat_sum += days_difference*all_demands[len(all_demands) - 1].fat

    return Response({
        'demand_calories_sum' : demand_calories_sum, 
        'demand_protein_sum' : demand_protein_sum, 
        'demand_carbohydrates_sum' : demand_carbohydrates_sum, 
        'demand_fat_sum' : demand_fat_sum
        }, status=status.HTTP_200_OK)

from user.models import UserProfile
from utils.products_and_meals_utils import basic_macros

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_basic_demand_view(request):
    user_basic_demand = UserProfile.objects.get(user_id=request.user.id).daily_calory_demand
    user_basic_macros = basic_macros(user_basic_demand)
    data = {
        'demand' : user_basic_demand,
        'protein' : user_basic_macros[0],
        'carbohydrates' : user_basic_macros[1],
        'fat' : user_basic_macros[2]
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_demand_view(request):
    user_id = request.user.id
    userprofile_id = UserProfile.objects.get(user_id=user_id).userprofile_id
    serializer = DemandSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    EPSILON = 10 # absolute calorie error

    calories_sum = round(4 * serializer.validated_data['protein'] + 4 * serializer.validated_data['carbohydrates'] + 9 * serializer.validated_data['fat'])
    if (calories_sum > serializer.validated_data['daily_calory_demand'] + EPSILON):
        return Response({'Macros calories too high' : f'{calories_sum}/{serializer.validated_data["daily_calory_demand"]}'})
    elif (calories_sum < serializer.validated_data['daily_calory_demand'] - EPSILON):
        return Response({'Macros calories too low' : f'{calories_sum}/{serializer.validated_data["daily_calory_demand"]}'})
    
    # try to get demand from today, if exists - update it, if not create demand with date = today
    try:
        Demand.objects.get(userprofile_id=userprofile_id, date=date.today())
        Demand.update_calories(
            userprofile_id=userprofile_id, 
            protein=serializer.validated_data['protein'],
            carbohydrates=serializer.validated_data['carbohydrates'],
            fat=serializer.validated_data['fat'],
            daily_calory_demand=serializer.validated_data['daily_calory_demand'])
    except Demand.DoesNotExist:
        Demand.create_demand(
            userprofile_id=userprofile_id,
            protein=serializer.validated_data['protein'],
            carbohydrates=serializer.validated_data['carbohydrates'],
            fat=serializer.validated_data['fat'],
            daily_calory_demand=serializer.validated_data['daily_calory_demand'],
            date=date.today()
            )
    return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

# MEAL VIEWS

# returns information about each meal from selected day with all mealitems included
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_meal_view(request, date):
    try:
        meal = Meal.objects.filter(user_id=request.user.id, date=date)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # find mealitems added by user at this date

    query = Q()

    for x in meal:
        query = Q(meal_id=x.meal_id) | query

    mealitems = MealItem.objects.filter(query)

    # now get from this information all products info

    breakfast_meal_id = lunch_meal_id = dinner_meal_id = None

    for x in meal:
        if (x.type=='breakfast'):
            breakfast_meal_id = x.meal_id
        elif (x.type=='lunch'):
            lunch_meal_id = x.meal_id
        elif (x.type=='dinner'):
            dinner_meal_id = x.meal_id

    data = {
        'breakfast' : {},
        'lunch' : {},
        'dinner' : {}
    }

    i = j = k = 0 # iterators to add products named as product0, product1, ...

    for x in mealitems:
        product = Product.objects.get(product_id=x.product_id) # get product from database
        product_macros_info = Product.calculate_nutrition(gram_amount=x.gram_amount, product=product) # calculate macros per gram_amount
        product_info = {
            'mealitem_id' : x.meal_item_id,
            'product_id' : product.product_id,
            'name' : product.name,
            'protein' : round(product_macros_info[0], 1),
            'carbohydrates' : round(product_macros_info[1], 1),
            'fat' : round(product_macros_info[2], 1),
            'calories' : round(product_macros_info[0]*4+product_macros_info[1]*4+product_macros_info[2]*9),
            'grams' : x.gram_amount
        }
        if (breakfast_meal_id is not None) and (x.meal_id == breakfast_meal_id):
            data['breakfast'][f'product{i}'] = product_info
            i += 1
        elif (lunch_meal_id is not None) and (x.meal_id == lunch_meal_id):
            data['lunch'][f'product{j}'] = product_info
            j += 1
        if (dinner_meal_id is not None) and (x.meal_id == dinner_meal_id):
            data['dinner'][f'product{k}'] = product_info
            k += 1

    return Response(data, status=status.HTTP_200_OK) 
    
# MEALITEM VIEWS

@api_view(['GET'])
def api_detail_meal_item_view(request, meal_item_id):
    try:
        meal_item = MealItem.objects.get(meal_item_id=meal_item_id)
    except MealItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MealItemSerializer(meal_item)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_update_meal_item_view(request, meal_item_id):
    userprofile_id = UserProfile.objects.get(user_id=request.user.id).userprofile_id
    try:
        mealitem = MealItem.objects.get(meal_item_id=meal_item_id)
    except MealItem.DoesNotExist:
        return not_found_response()
    
    serializer = MealItemSerializer(mealitem, request.data)
    if serializer.is_valid():
        # get product 
        product = Product.objects.get(product_id=mealitem.product_id)
        grams_difference = serializer.validated_data['gram_amount'] - mealitem.gram_amount # calculate difference between grams
        product_macros = Product.calculate_nutrition(gram_amount=abs(grams_difference), product=product) # calculate calories per grams_difference
        # update summary
        meal_id = mealitem.meal_id # find id of meal this mealitem belongs to
        summary_date = Meal.objects.get(meal_id=meal_id).date # since we have mealitem, it must exist
        if grams_difference < 0:
            new_summary = Summary.update_calories(userprofile_id=userprofile_id, increase=0, protein=product_macros[0], carbohydrates=product_macros[1], fat=product_macros[2], date=summary_date)
        else:
            new_summary = Summary.update_calories(userprofile_id=userprofile_id, increase=1, protein=product_macros[0], carbohydrates=product_macros[1], fat=product_macros[2], date=summary_date)
        summary_serializer = SummarySerializer(new_summary)
        serializer.save()
        return Response(serializer.validated_data|summary_serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def api_delete_meal_item_view(request, meal_item_id):
    try:
        meal_item = MealItem.objects.get(id=meal_item_id)
    except MealItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    operation = MealItem.objects.get(id=meal_item_id).delete()
    data = {}
    if operation:
        data['success'] = 'deletion successful'
    else:
        data['failure'] = 'deletion failed'
    return Response(data=data)

def create_mealitem(type, user_id, request_data, date):
    userprofile_id = UserProfile.objects.get(user_id=user_id).userprofile_id
    serializer = MealItemSerializer(data=request_data)
    if serializer.is_valid():
        # PRODUCT EXISTENCE
        try:
            product_to_add = Product.objects.get(Q(product_id=serializer.validated_data['product_id']) & (Q(user_id=user_id) | Q(user_id=1))) # check if this product should be available for user
        except Product.DoesNotExist:
            return custom_response("Product", "does not exist", status.HTTP_404_NOT_FOUND)
        # MEAL EXISTENCE
        if not Meal.objects.filter(user_id=user_id, date=date, type=type).exists():
            Meal.add_meal(user_id=user_id, type=type, date=date)
        # SUMMARY EXISTENCE
        if not Summary.objects.filter(userprofile_id=userprofile_id, date=date).exists():
            Summary.create_summary(userprofile_id=userprofile_id, date=date)
        # MEAL ITEM PART
        meal_id = Meal.objects.get(user_id=user_id, date=date, type=type).meal_id # now we can get meal_id because we know that meal exists
        MealItem.add_product(meal_id=meal_id, product_id=product_to_add.product_id, gram_amount=serializer.validated_data['gram_amount'])
        # calculate product macros and calories (gram_amount of product can be different than 100)
        protein, carbohydrates, fat = Product.calculate_nutrition(gram_amount=serializer.validated_data['gram_amount'], product=product_to_add)
        # update summary
        Summary.update_calories(userprofile_id=userprofile_id, increase=True, protein=protein, carbohydrates=carbohydrates, fat=fat, date=date)
        # create data to return
        data = serializer.validated_data|{'name' : product_to_add.name, 'calories' : round((4*protein + 4*carbohydrates + 9*fat)), 'protein' : round(protein, 1), 'carbohydrates' : round(carbohydrates, 1), 'fat' : round(fat, 1)}
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_mealitem_breakfast_view(request, date):
    return create_mealitem(type="breakfast", user_id=request.user.id, request_data=request.data, date=date)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_mealitem_lunch_view(request, date):
    return create_mealitem(type="lunch", user_id=request.user.id, request_data=request.data, date=date)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_mealitem_dinner_view(request, date):
    return create_mealitem(type="dinner", user_id=request.user.id, request_data=request.data, date=date)
