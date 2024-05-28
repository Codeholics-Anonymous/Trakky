from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from utils.responses import short_response, not_found_response

from products_and_meals.models import (Product, Summary, Demand, Meal, MealItem)
from products_and_meals.api.serializers import (ProductSerializer, SummarySerializer, DemandSerializer, MealSerializer, MealItemSerializer)
from datetime import datetime, date

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

# PRODUCT VIEWS

from utils.products_and_meals_utils import above_upper_limit

# find all products available to the user (by name parameter)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_search_product_view(request, product_name):
    product = Product.objects.filter(Q(name__icontains=product_name) & (Q(user_id__isnull=True) | Q(user_id=request.user.id)))
    if (len(product) == 0):
        return not_found_response()

    serializer = ProductSerializer(product, many=True)
    for i in range(len(serializer.data)):
        serializer.data[i]['calories_per_hundred_grams'] = product[i].calories_per_hundred_grams
    return Response(serializer.data, status=status.HTTP_200_OK)

# display user products added by him

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_display_user_products_view(request):
    products = Product.objects.filter(user_id=request.user.id)
    if len(products) == 0:
        return short_response("message", "You haven't added any products yet.")
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

from utils.products_and_meals_utils import find_mealitems

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_update_product_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return not_found_response()

    if ((product.user_id is None) or (product.user_id != request.user.id)): # user can edit only products that were created by him
        return short_response("message", "Product cannot be edited", status.HTTP_400_BAD_REQUEST)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        # check if sum of macros isn't larger than 100g
        if above_upper_limit(serializer.validated_data['protein'], serializer.validated_data['carbohydrates'], serializer.validated_data['fat'], limit=100):
            return short_response("message", f"Macros amount to high ({serializer.validated_data['protein'] + serializer.validated_data['carbohydrates'] + serializer.validated_data['fat']}/{100})", status.HTTP_400_BAD_REQUEST) 

        # check if product with this name does not exist in database
        if (serializer.validated_data['name'] != product.name) and Product.objects.filter(name=serializer.validated_data['name']).exists():
            return short_response("message", "Product already exists.", status.HTTP_400_BAD_REQUEST)

        # update today's summary if this product has been added (optimization - don't update past summaries)
        mealitems = find_mealitems(user_id=request.user.id, product_id=product_id, date=date.today()) # list of mealitems (from today) that contains updated product
        mealitems_amount = len(mealitems)
        mealitems_gram_amount = 0
        userprofile_id = None

        if (mealitems_amount > 0):
            # calculate product amount (grams)
            for x in mealitems:
                mealitems_gram_amount += x.gram_amount
            # call function to calculate how many protein, carbohydrates and fat we have in these mealitems
            all_product_macros = Product.calculate_nutrition(gram_amount=mealitems_gram_amount, product=product)
            # find userprofile to update summary
            userprofile_id = UserProfile.objects.get(user_id=request.user.id).userprofile_id
            # subtract previous macros and calories 
            Summary.update_calories( 
                userprofile_id=userprofile_id, 
                increase=0, 
                protein=all_product_macros[0], 
                carbohydrates=all_product_macros[1], 
                fat=all_product_macros[2], 
                date=date.today()
                )

        # update product using information provided by user
        updated_product = Product.update_product(
            product=product, 
            name=serializer.validated_data['name'], 
            protein=serializer.validated_data['protein'],
            carbohydrates=serializer.validated_data['carbohydrates'],
            fat=serializer.validated_data['fat']
            )

        if (mealitems_amount > 0):
            # after product update, we have to increase number of calories and macros in summary
            all_updated_product_macros = Product.calculate_nutrition(gram_amount=mealitems_gram_amount, product=updated_product)
            Summary.update_calories(
                userprofile_id=userprofile_id, 
                increase=1, 
                protein=all_updated_product_macros[0],
                carbohydrates=all_updated_product_macros[1],
                fat=all_updated_product_macros[2],
                date=date.today()
                )

        return short_response("message", "Product updated.")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from utils.permissions import IsProductManager

# Product Managers can edit products available for all users

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def api_update_product_for_all_view(request, product_id):
    try:
        product = Product.objects.get(user_id__isnull=True, product_id=product_id)
    except Product.DoesNotExist:
        return short_response("message", "You cannot update this product.", status.HTTP_400_BAD_REQUEST)

    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        # check if sum of macros isn't larger than 100g
        if above_upper_limit(serializer.validated_data['protein'], serializer.validated_data['carbohydrates'], serializer.validated_data['fat'], limit=100):
            return short_response("message", f"Macros amount to high ({serializer.validated_data['protein'] + serializer.validated_data['carbohydrates'] + serializer.validated_data['fat']}/{100.0})", status.HTTP_400_BAD_REQUEST) 
        # check if product with this name does not exist in database
        if (product.name != serializer.validated_data['name']) and Product.objects.filter(name=serializer.validated_data['name']).exists():
            return short_response("message", "Product already exists.", status.HTTP_400_BAD_REQUEST)
        # update product
        Product.update_product(
            product=product, 
            name=serializer.validated_data['name'], 
            protein=serializer.validated_data['protein'], 
            carbohydrates=serializer.validated_data['carbohydrates'], 
            fat=serializer.validated_data['fat']
            )
        return short_response("message", "Product updated.")

def delete_product(user_id, product_id):
    try:
        product = Product.objects.get(user_id=user_id, product_id=product_id)
    except Product.DoesNotExist:
        return short_response("message", "You cannot delete this product.")

    operation = product.delete()
    if operation:
        return short_response("message", "Deletion successful")
    else:
        return short_response("message", "Deletion failed", status.HTTP_400_BAD_REQUEST)

# view for deleting product only from products added by user

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_delete_product_view(request, product_id):
    return delete_product(user_id=request.user.id, product_id=product_id)

# view for deleting product from products available for all users (available only for Product Managers)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def api_delete_product_for_all_view(request, product_id):
    return delete_product(user_id=None, product_id=product_id)

def add_product(request_data, user_id):
    serializer = ProductSerializer(data=request_data)
    if serializer.is_valid():
        # check if this product exists in database (only in products for this user and for all users)
        if Product.objects.filter(Q(name=serializer.validated_data['name']) & (Q(user_id = user_id) | Q(user_id__isnull=True))).exists():
            return short_response("message", "Product already exists", status.HTTP_400_BAD_REQUEST)
        # check if sum of macros isn't larger than 100g
        if above_upper_limit(serializer.validated_data['protein'], serializer.validated_data['carbohydrates'], serializer.validated_data['fat'], limit=100):
            return short_response("message", f"Macros amount to high ({serializer.validated_data['protein'] + serializer.validated_data['carbohydrates'] + serializer.validated_data['fat']}/{100.0})", status.HTTP_400_BAD_REQUEST)
        # add product
        added_product = Product.add_product(
            user_id=user_id,
            name=serializer.validated_data['name'],
            protein=serializer.validated_data['protein'],
            carbohydrates=serializer.validated_data['carbohydrates'],
            fat=serializer.validated_data['fat'],
        )
        data = serializer.validated_data|{'calories_per_hundred_grams' : added_product.calories_per_hundred_grams}
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_product_view(request):
    max_products_num = 100
    # check if user has not exceeded maximum number of products that can be added by him
    products = Product.objects.filter(user_id=request.user.id)
    if (len(products) >= max_products_num):
        return short_response("message", f"Maximum number of products that can be added ({max_products_num}) has been exceeded")
    return add_product(request_data=request.data, user_id=request.user.id)

# VIEW TO ADD PRODUCT FOR ALL USERS (AVAILABLE ONLY FOR PRODUCT MANAGERS)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsProductManager])
def api_create_product_for_all_view(request):
    return add_product(request_data=request.data, user_id=None)

# SUMMARY VIEWS

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_summary_view(request, starting_date, ending_date):
    try:
        userprofile_id = UserProfile.objects.get(user_id=request.user.id).userprofile_id
    except UserProfile.DoesNotExist:
        return short_response("message", "user profile does not exist.", status.HTTP_404_NOT_FOUND)
    
    summaries = Summary.objects.filter(userprofile_id=userprofile_id, date__range=(starting_date, ending_date))

    d_start = datetime.strptime(starting_date, "%Y-%m-%d")
    d_end = datetime.strptime(ending_date, "%Y-%m-%d")

    if (d_start > d_end):
        return short_response("Data", "range is incorrect", status.HTTP_400_BAD_REQUEST)

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

    return Response({'summary_calories_sum' : round(calories_sum), 'summary_protein_sum' : round(protein_sum, 1), 'summary_carbohydrates_sum' : round(carbohydrates_sum, 1), 'summary_fat_sum' : round(fat_sum, 1)})

# DEMAND VIEWS
# ways to create demand:
# 1 option - we are creating demand basing on data that user gave us during registration 
# 2 option - user can set his demand by himself (by giving us protein, carbohydrates, fat and calories) (this option is presented below)

from utils.date import calculate_days_difference, date_validation

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_demand_view(request, starting_date, ending_date):
    userprofile_id = UserProfile.objects.get(user_id=request.user.id).userprofile_id
    # validate date
    if (starting_date > ending_date):
        return short_response("message", "Incorrect date", status.HTTP_400_BAD_REQUEST)
    # check first demand existence
    beginning_demand = None
    beginning_demand = Demand.objects.filter(userprofile_id=userprofile_id, date__lte=starting_date).order_by('-date').first()
    if beginning_demand is None:
        return short_response("message", "No information about demand for the selected period", status.HTTP_404_NOT_FOUND)
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

def get_meal(user_id, request_data, date, type):
    # find meal_id from selected date
    try:
        meal_id = Meal.objects.get(user_id=user_id, date=date, type=type).meal_id
    except Meal.DoesNotExist:
        return short_response("message", "meal does not exist", status.HTTP_404_NOT_FOUND)

    # find all mealitems added to found meal
    mealitems = MealItem.objects.filter(meal_id=meal_id)

    final_data = {}
    product_data = {}
    i = 0
    
    for x in mealitems:
        product = Product.objects.get(product_id=x.product_id)
        product_macros = Product.calculate_nutrition(x.gram_amount, product)
        product_data = {
            'mealitem_id' : x.meal_item_id,
            'product_id' : product.product_id,
            'name' : product.name,
            'calories' : 4*product_macros[0]+4*product_macros[1]+9*product_macros[2],
            'grams' : x.gram_amount,
            'protein' : product_macros[0],
            'carbohydrates' : product_macros[1],
            'fat' : product_macros[2],
        }
        final_data[f'product{i}'] = product_data
        i += 1

    return Response(final_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_breakfast_meal_view(request, date):
    return get_meal(request.user.id, request.data, date, "breakfast")

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_lunch_meal_view(request, date):
    return get_meal(request.user.id, request.data, date, "lunch")

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_dinner_meal_view(request, date):
    return get_meal(request.user.id, request.data, date, "dinner")

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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_detail_meal_item_view(request, meal_item_id):
    try:
        meal_item = MealItem.objects.get(meal_item_id=meal_item_id)
    except MealItem.DoesNotExist:
        return not_found_response()

    # find product from this mealitem and calculate macros of this product
    product = Product.objects.get(product_id=meal_item.product_id)
    macros = Product.calculate_nutrition(meal_item.gram_amount, product)

    data = {
        'product_name' : product.name, 
        'gram_amount' : meal_item.gram_amount, 
        'protein' : macros[0], 
        'carbohydrates' : macros[1], 
        'fat' : macros[2], 
        'calories' : 4*macros[0] + 4*macros[1] + 9*macros[2]}

    return Response(data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_update_meal_item_view(request, meal_item_id):
    try:
        mealitem = MealItem.objects.get(meal_item_id=meal_item_id)
    except MealItem.DoesNotExist:
        return not_found_response()
    
    serializer = MealItemSerializer(mealitem, request.data)
    if serializer.is_valid():
        # users shouldn't be allowed to change product when updating mealitem
        if serializer.validated_data['product_id'] != mealitem.product_id:
            return short_response("message", "Product cannot be changed.", status.HTTP_400_BAD_REQUEST)
        # get product 
        product = Product.objects.get(product_id=mealitem.product_id)
        grams_difference = serializer.validated_data['gram_amount'] - mealitem.gram_amount # calculate difference between grams
        product_macros = Product.calculate_nutrition(gram_amount=abs(grams_difference), product=product) # calculate calories per grams_difference
        # update summary
        meal_id = mealitem.meal_id # find id of meal this mealitem belongs to
        summary_date = Meal.objects.get(meal_id=meal_id).date # since we have mealitem, it must exist
        userprofile_id = UserProfile.objects.get(user_id=request.user.id).userprofile_id # find userprofile id to find summary in summary update_calories method
        if grams_difference < 0:
            new_summary = Summary.update_calories(userprofile_id=userprofile_id, increase=0, protein=product_macros[0], carbohydrates=product_macros[1], fat=product_macros[2], date=summary_date)
        else:
            new_summary = Summary.update_calories(userprofile_id=userprofile_id, increase=1, protein=product_macros[0], carbohydrates=product_macros[1], fat=product_macros[2], date=summary_date)
        summary_serializer = SummarySerializer(new_summary)
        # prepare data to return
        final_macros = Product.calculate_nutrition(gram_amount=mealitem.gram_amount+grams_difference, product=product) # calculate final macros
        modified_mealitem_data = {
            'calories' : 4*final_macros[0] + 4*final_macros[1] + 9*final_macros[2],
            'protein' : final_macros[0],
            'carbohydrates' : final_macros[1],
            'fat' : final_macros[2]
        }
        serializer.save() # save info about mealitem
        modified_summary_data = summary_serializer.data
        response_data = {
            'modified_mealitem_data' : modified_mealitem_data,
            'modified_summary_data' : modified_summary_data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_delete_meal_item_view(request, meal_item_id):
    try:
        meal_item = MealItem.objects.get(meal_item_id=meal_item_id)
    except MealItem.DoesNotExist:
        return not_found_response()

    if MealItem.remove_product(id=meal_item.meal_item_id):
        return short_response("message", "Deletion successful")
    else:
        return short_response("message", "Deletion failed", status.HTTP_400_BAD_REQUEST)

from utils.products_and_meals_utils import find_first_demand

def create_mealitem(type, user_id, request_data, date):
    userprofile_id = UserProfile.objects.get(user_id=user_id).userprofile_id
    # check if date isn't earlier than date of account creation
    account_creation_date = find_first_demand(userprofile_id).date
    if account_creation_date > datetime.strptime(date, "%Y-%m-%d").date():
        return short_response("message", "Date earlier than account creation", status.HTTP_400_BAD_REQUEST)    
    # get data from input
    serializer = MealItemSerializer(data=request_data)
    if serializer.is_valid():
        # PRODUCT EXISTENCE
        try:
            product_to_add = Product.objects.get(Q(product_id=serializer.validated_data['product_id']) & (Q(user_id=user_id) | Q(user_id__isnull=True))) # check if this product should be available for user
        except Product.DoesNotExist:
            return short_response("message", "Product does not exist", status.HTTP_404_NOT_FOUND)
        # MEAL EXISTENCE
        meal_id = None
        meal_exists = Meal.objects.filter(user_id=user_id, date=date, type=type).exists()
        # check upper limit for mealitems amount in single meal 
        if meal_exists:
            # check upper limit for mealitems amount
            meal_id = Meal.objects.get(user_id=user_id, date=date, type=type).meal_id
            mealitems = MealItem.objects.filter(meal_id=meal_id)
            if len(mealitems) >= 50:
                return short_response("message", "upper limit of products per meal exceeded", status.HTTP_400_BAD_REQUEST)
        else:
            meal_id = Meal.add_meal(user_id=user_id, type=type, date=date).meal_id
        # SUMMARY EXISTENCE
        if not Summary.objects.filter(userprofile_id=userprofile_id, date=date).exists():
            Summary.create_summary(userprofile_id=userprofile_id, date=date)
        # MEAL ITEM PART
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
