from django.test import TestCase
from .models import *
from datetime import date

class MacrosTestCase(TestCase):
    def test_correct_update_macros(self): # input is correct
        class ConcreteMacros(Macros): # create subclass to test abstract class Macros methods
            ...
        macros = ConcreteMacros()

        self.assertTrue(macros.update_macros(120, 200, 50)) # check if function returns result True, which means that input was correct
        self.assertEqual(macros.protein, 120)
        self.assertEqual(macros.carbohydrates, 200)
        self.assertEqual(macros.fat, 50)

    def test_wrong_update_calories(self): # input is incorrect
        class ConcreteMacrosSecond(Macros): # create subclass to test abstract class Macros methods
            ...
        macros = ConcreteMacrosSecond()

        self.assertFalse(macros.update_macros(-50, 3, 120))
        self.assertFalse(macros.update_macros(0, -5, 111))
        self.assertFalse(macros.update_macros(-50, -50, -100))

# unit test for Demand class

class DemandTestCase(TestCase):

    def setUp(self):
        # Create demands for tests
        self.user1 = User.objects.create(username='test_user1')
        self.user2 = User.objects.create(username='test_user2')
        self.user3 = User.objects.create(username='test_user3')
        self.userprofile1 = UserProfile.objects.create(user_id=self.user1.id, sex='M', weight=70, height=170, work_type=0, birth_date='2000-01-01', user_goal=0)
        self.userprofile2 = UserProfile.objects.create(user_id=self.user2.id, sex='M', weight=70, height=170, work_type=0, birth_date='2000-01-01', user_goal=0)
        self.userprofile3 = UserProfile.objects.create(user_id=self.user3.id, sex='M', weight=70, height=170, work_type=0, birth_date='2000-01-01', user_goal=0)
        self.demand1 = Demand.objects.create(userprofile_id=self.userprofile1.userprofile_id, daily_calory_demand=1820, date=date.today(), protein=120, fat=60, carbohydrates=200)
        self.demand2 = Demand.objects.create(userprofile_id=self.userprofile2.userprofile_id, daily_calory_demand=2000, date=date.today(), protein=165, fat=60, carbohydrates=200)

    def test_create_demand_object(self):
        demand = Demand.create_demand(userprofile_id=self.userprofile3.userprofile_id, daily_calory_demand=1820, date=date.today(), protein=120, fat=60, carbohydrates=200)

        self.assertEqual(demand.userprofile_id, self.userprofile3.userprofile_id)
        self.assertEqual(demand.daily_calory_demand, 1820)
        self.assertEqual(demand.protein, 120)
        self.assertEqual(demand.carbohydrates, 200)
        self.assertEqual(demand.fat, 60)
        self.assertEqual(demand.date, date.today())

        # check existence in database

        saved_demand = Demand.objects.get(demand_id=demand.demand_id)
        self.assertEqual(saved_demand.daily_calory_demand, 1820)
        self.assertEqual(saved_demand.protein, 120)
        self.assertEqual(saved_demand.carbohydrates, 200)
        self.assertEqual(saved_demand.fat, 60)
        self.assertEqual(saved_demand.date, date.today())

    def test_demand_update_calories(self):
        updated_demand = Demand.update_calories(userprofile_id=self.demand1.userprofile_id, protein=130, fat=70, carbohydrates=190, daily_calory_demand=1910)

        # Check if first demand was updated correctly
        self.assertIsNotNone(updated_demand)
        self.assertEqual(updated_demand.daily_calory_demand, 1910)
        self.assertEqual(updated_demand.protein, 130)
        self.assertEqual(updated_demand.fat, 70)
        self.assertEqual(updated_demand.carbohydrates, 190)
        self.assertEqual(updated_demand.date, date.today())

        # Check if other records are same as before update
        unchanged_demand = Demand.objects.get(demand_id=self.demand2.demand_id)
        self.assertEqual(unchanged_demand.daily_calory_demand, 2000)
        self.assertEqual(unchanged_demand.protein, 165)
        self.assertEqual(unchanged_demand.fat, 60)
        self.assertEqual(unchanged_demand.carbohydrates, 200)
        self.assertEqual(unchanged_demand.date, date.today())

# unit tests for Summary class

class SummaryTestCase(TestCase):

    def setUp(self):
        # Create demands for tests
        self.user1 = User.objects.create(username='test_user1')
        self.user2 = User.objects.create(username='test_user2')
        self.user3 = User.objects.create(username='test_user3')
        self.userprofile1 = UserProfile.objects.create(user_id=self.user1.id, sex='M', weight=70, height=170, work_type=0, birth_date='2000-01-01', user_goal=0)
        self.userprofile2 = UserProfile.objects.create(user_id=self.user2.id, sex='M', weight=70, height=170, work_type=0, birth_date='2000-01-01', user_goal=0)
        self.userprofile3 = UserProfile.objects.create(user_id=self.user3.id, sex='M', weight=70, height=170, work_type=0, birth_date='2000-01-01', user_goal=0)
        self.summary1 = Summary.objects.create(userprofile_id=self.userprofile1.userprofile_id, daily_calory_intake=0, date=date.today(), protein=0, fat=0, carbohydrates=0)
        self.summary2 = Summary.objects.create(userprofile_id=self.userprofile2.userprofile_id, daily_calory_intake=0, date=date.today(), protein=0, fat=0, carbohydrates=0)

    def test_create_summary_object(self):
        summary = Summary.create_summary(
            userprofile_id=self.userprofile3.userprofile_id,
            date=date.today(),
            protein=100,
            carbohydrates=50,
            fat=20
            )

        self.assertEqual(summary.userprofile_id, self.userprofile3.userprofile_id)
        self.assertEqual(summary.daily_calory_intake, 100*4 + 50*4 + 20*9)
        self.assertEqual(summary.protein, 100)
        self.assertEqual(summary.carbohydrates, 50)
        self.assertEqual(summary.fat, 20)
        self.assertEqual(summary.date, date.today())

        # check existence in database

        saved_summary = Summary.objects.get(summary_id=summary.summary_id)
        self.assertEqual(saved_summary.userprofile_id, self.userprofile3.userprofile_id)
        self.assertEqual(saved_summary.daily_calory_intake, 100*4 + 50*4 + 20*9)
        self.assertEqual(saved_summary.protein, 100)
        self.assertEqual(saved_summary.carbohydrates, 50)
        self.assertEqual(saved_summary.fat, 20)
        self.assertEqual(saved_summary.date, date.today())

    def test_summary_update_calories(self):
        updated_summary = Summary.update_calories(userprofile_id=self.summary1.userprofile_id, increase=True, protein=30, fat=10, carbohydrates=20, date=date.today())

        # Check if first summary was updated correctly
        self.assertIsNotNone(updated_summary)
        self.assertEqual(updated_summary.daily_calory_intake, 4*30 + 9*10 + 4*20)
        self.assertEqual(updated_summary.date, date.today())
        self.assertEqual(updated_summary.protein, 30)
        self.assertEqual(updated_summary.fat, 10)
        self.assertEqual(updated_summary.carbohydrates, 20)

        # Check if other records are same as before update
        unchanged_summary = Summary.objects.get(summary_id=self.summary2.summary_id)
        self.assertEqual(unchanged_summary.daily_calory_intake, 0)
        self.assertEqual(unchanged_summary.protein, 0)
        self.assertEqual(unchanged_summary.fat, 0)
        self.assertEqual(unchanged_summary.carbohydrates, 0)

class ProductTestCase(TestCase):
    def setUp(self):
        # Create products for tests
        self.user = User.objects.create()
        self.product1 = Product.objects.create(name="apple", protein=0, fat=0, carbohydrates=0)
        self.product2 = Product.objects.create(name="orange", protein=30, carbohydrates=20, fat=10)

    def test_add_product(self):
        product = Product.add_product(user_id=self.user.id, name="apple", protein=10, carbohydrates=20, fat=30)

        # Check if product was added correctly
        self.assertIsNotNone(product.product_id)
        self.assertEqual(product.name, "apple")
        self.assertEqual(product.protein, 10)
        self.assertEqual(product.carbohydrates, 20)
        self.assertEqual(product.fat, 30)
        self.assertEqual(product.calories_per_hundred_grams, 390)
        
        # Check if product exists in our database
        saved_product = Product.objects.get(product_id=product.product_id)
        self.assertEqual(saved_product.name, "apple")
        self.assertEqual(saved_product.protein, 10)
        self.assertEqual(saved_product.carbohydrates, 20)
        self.assertEqual(saved_product.fat, 30)
        self.assertEqual(saved_product.calories_per_hundred_grams, 390)

    def test_update_product(self):
        updated_product = Product.update_product(product=self.product1, name="cake", protein=10, carbohydrates=10, fat=10)

        # Check if first product was updated correctly
        self.assertIsNotNone(updated_product)
        self.assertEqual(updated_product.name, "cake")
        self.assertEqual(updated_product.protein, 10)
        self.assertEqual(updated_product.carbohydrates, 10)
        self.assertEqual(updated_product.fat, 10)
        self.assertEqual(updated_product.calories_per_hundred_grams, 170)

        # Check if other records are same as before
        unchanged_product = Product.objects.get(product_id=self.product2.product_id)
        self.assertEqual(unchanged_product.name, "orange")
        self.assertEqual(unchanged_product.protein, 30)
        self.assertEqual(unchanged_product.carbohydrates, 20)
        self.assertEqual(unchanged_product.fat, 10)
        self.assertEqual(unchanged_product.calories_per_hundred_grams, 290)

class MealTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create()

    def test_add_meal(self):
        meal = Meal.add_meal(user_id=self.user.id, type="dinner", date=date.today())

        # Check if meal was added correctly
        self.assertIsNotNone(meal)
        self.assertEqual(meal.user_id, self.user.id)
        self.assertEqual(meal.type, "dinner")
        self.assertEqual(meal.date, date.today())
        
        # Check if meal exists in our database
        saved_meal = Meal.objects.get(meal_id=meal.meal_id)
        self.assertEqual(saved_meal.user_id, self.user.id)
        self.assertEqual(saved_meal.type, "dinner")
        self.assertEqual(saved_meal.date, date.today())

class MealItemTestCase(TestCase):
    def setUp(self):
        # Create MealItem for tests
        self.meal1 = Meal.objects.create(date=date.today(), type="breakfast")
        self.meal2 = Meal.objects.create(date=date.today(), type="breakfast")
        self.product1 = Product.objects.create()
        self.meal_item1 = MealItem.objects.create(meal_id=self.meal1.meal_id, product_id=self.product1.product_id, gram_amount=200)

    def test_add_product(self):
        meal_item = MealItem.add_product(meal_id=self.meal2.meal_id, product_id=self.product1.product_id, gram_amount=200)

        # Check if mealItem was added correctly
        self.assertIsNotNone(meal_item)
        self.assertEqual(meal_item.gram_amount, 200)
        self.assertEqual(meal_item.meal_id, self.meal2.meal_id)
        self.assertEqual(meal_item.product_id, self.product1.product_id)

        # Check if mealItem exists in our database
        saved_meal_item = MealItem.objects.get(meal_item_id=meal_item.meal_item_id)
        self.assertIsNotNone(saved_meal_item)
        self.assertEqual(saved_meal_item.gram_amount, 200)
        self.assertEqual(saved_meal_item.meal_id, self.meal2.meal_id)
        self.assertEqual(saved_meal_item.product_id, self.product1.product_id)

    def test_remove_product(self):
        # Get the product to remove
        product_to_remove = self.meal_item1
        product_to_remove_id = product_to_remove.meal_item_id

        # Remove the product from the meal
        MealItem.remove_product(id=product_to_remove_id)

        # Check if the removed product no longer exists in the database
        self.assertFalse(MealItem.objects.filter(meal_item_id=product_to_remove_id).exists())

from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token

class ProductRequests(TestCase):
    def setUp(self):
        self.client = APIClient() # create API client
        self.user = User.objects.create(username="test_user", password="test_password")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) # add authorization token to each request user will send

    def test_post_and_get_product(self):
        # create own product
        data = {
            'name' : 'test_product',
            'protein' : 10,
            'carbohydrates' : 20,
            'fat' : 10
        }
        post_response = self.client.post('/api/create_product/', data)
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(post_response.data, data|{'calories_per_hundred_grams' : 4*data['protein']+4*data['carbohydrates']+9*data['fat']})
        get_response = self.client.get('/api/product/test_product/')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.data[0]['name'], 'test_product')
        # create product with incorrect amount of macros
        incorrect_data = {
            'name' : 'incorrect_product',
            'protein' : -1,
            'carbohydrates' : 0,
            'fat' : 10
        }
        incorrect_post_response = self.client.post('/api/create_product/', incorrect_data)
        self.assertEqual(incorrect_post_response.status_code, 400)
        incorrect_macros_sum_data = {
            'name' : 'incorrect_product',
            'protein' : 10,
            'carbohydrates' : 50,
            'fat' : 41
        }
        incorrect_macros_sum_response = self.client.post('/api/create_product/', incorrect_macros_sum_data)
        self.assertEqual(incorrect_macros_sum_response.status_code, 400)
        self.assertEqual(
            incorrect_macros_sum_response.data['message'], 
            f"Macros amount to high ({float(incorrect_macros_sum_data['protein']+incorrect_macros_sum_data['carbohydrates']+incorrect_macros_sum_data['fat'])}/{100.0})")