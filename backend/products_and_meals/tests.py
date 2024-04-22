from django.test import TestCase
from .models import *
from datetime import date

# Create your tests here.

class MacrosTestCase(TestCase):
    def test_correct_update_macros(self): # input is correct
        class ConcreteMacros(Macros): # create subclass to test abstract class Macros methods
            ...
        macros = ConcreteMacros()

        self.assertTrue(macros.update_macros(120, 200, 50)) # check if function returns result True, which means that input was correct
        self.assertEqual(macros.protein, 120)
        self.assertEqual(macros.carbohydrates, 200)
        self.assertEqual(macros.fat, 50)

    def test_wrong_update_macros(self): # input is incorrect
        class ConcreteMacros(Macros): # create subclass to test abstract class Macros methods
            ...
        macros = ConcreteMacros()

        self.assertFalse(macros.update_macros(-50, 3, 120))
        self.assertFalse(macros.update_macros(0, 5, 111))
        self.assertFalse(macros.update_macros(-50, -50, -100))

# unit test for Demand class

class DemandTestCase(TestCase):

    def setUp(self):
        # Create demands for tests
        self.demand1 = Demand.objects.create(user_id=1, daily_calory_demand=2000, date=date.today(), protein=120, fat=60, carbohydrates=200)
        self.demand2 = Demand.objects.create(user_id=2, daily_calory_demand=2000, date=date.today(), protein=120, fat=60, carbohydrates=200)

    def test_create_demand_object(self):
        demand = Demand.objects.create(user_id=3, daily_calory_demand=2000, date=date.today(), protein=120, fat=60, carbohydrates=200)

        self.assertEqual(demand.user_id, 3)
        self.assertEqual(demand.daily_calory_demand, 2000)
        self.assertEqual(demand.date, date.today())

        # check existence in database

        saved_demand = Demand.objects.get(demand_id=demand.demand_id)
        self.assertEqual(saved_demand.daily_calory_demand, 2000)
        self.assertEqual(saved_demand.date, date.today())

    def test_demand_update_calories(self):
        updated_demand = Demand.update_calories(demand_id=self.demand1.demand_id, new_date=date.today(), new_protein=130, new_fat=70, new_carbohydrates=190)

        # Check if first demand was updated correctly
        self.assertIsNotNone(updated_demand)
        self.assertEqual(updated_demand.daily_calory_demand, 4*130 + 4*70 + 9*190)
        self.assertEqual(updated_demand.date, date.today())
        self.assertEqual(updated_demand.protein, 130)
        self.assertEqual(updated_demand.fat, 70)
        self.assertEqual(updated_demand.carbohydrates, 190)

        # Check if other records are same as before update
        unchanged_demand = Demand.objects.get(demand_id=self.demand2.demand_id)
        self.assertEqual(unchanged_demand.daily_calory_demand, 2000)
        self.assertEqual(unchanged_demand.protein, 120)
        self.assertEqual(unchanged_demand.fat, 60)
        self.assertEqual(unchanged_demand.carbohydrates, 200)

    def tearDown():
        self.demand1.delete()
        self.demand2.delete()

# unit tests for Summary class

class SummaryTestCase(TestCase):

    def setUp(self):
        # Create demands for tests
        self.summary1 = Summary.objects.create(user_id=1, daily_calory_intake=0, date=date.today())
        self.summary2 = Summary.objects.create(user_id=2, daily_calory_intake=0, date=date.today())

    def test_create_summary_object(self):
        summary = Summary.objects.create(user_id=3, daily_calory_intake=0, date=date.today())

        self.assertEqual(summary.user_id, 3)
        self.assertEqual(summary.daily_calory_intake, 0)
        self.assertEqual(summary.date, date.today())

        # check existence in database

        saved_summary = Summary.objects.get(summary_id=summary.summary_id)
        self.assertEqual(saved_demand.daily_calory_intake, 0)
        self.assertEqual(saved_demand.date, date.today())

    def test_summary_update_calories(self):
        updated_summary = Summary.update_calories(summary_id=self.summary1.summary_id, new_date=date.today(), increase=True, protein=30, fat=10, carbohydrates=20)

        # Check if first summary was updated correctly
        self.assertIsNotNone(updated_summary)
        self.assertEqual(updated_summary.daily_calory_intake, 4*30 + 4*10 + 9*20)
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

    def tearDown():
        self.summary1.delete()
        self.summary2.delete()

class ProductTestCase(TestCase):
    def setUp(self):
        # Create products for tests
        self.product1 = Product.objects.create(name="apple", calories_per_hundred_grams=50)
        self.product2 = Product.objects.create(name="orange", calories_per_hundred_grams=60)

    def test_add_product(self):
        product = Product.add_product("apple", 50)

        # Check if product was added correctly
        self.assertIsNotNone(product.product_id)
        self.assertEqual(product.name, "apple")
        self.assertEqual(product.calories_per_hundred_grams, 50)
        
        # Check if product exists in our database
        saved_product = Product.objects.get(product_id=product.product_id)
        self.assertEqual(saved_product.name, "apple")
        self.assertEqual(saved_product.calories_per_hundred_grams, 50)

    def test_update_product(self):
        updated_product = Product.update_product(product_id=self.product1.product_id, new_name="cake", new_calories=200)

        # Check if first product was updated correctly
        self.assertIsNotNone(updated_product)
        self.assertEqual(updated_product.name, "cake")
        self.assertEqual(updated_product.calories_per_hundred_grams, 200)

        # Check if other records are same as before
        unchanged_product = Product.objects.get(product_id=self.product2.product_id)
        self.assertEqual(unchanged_product.name, "orange")
        self.assertEqual(unchanged_product.calories_per_hundred_grams, 60)

    def tearDown(self):
        # Clear database
        self.product1.delete()
        self.product2.delete()

class MealTestCase(TestCase):
    def test_add_meal(self):
        meal = Meal.add_meal(user_id=1, type="dinner", date=date.today())

        # Check if meal was added correctly
        self.assertIsNotNone(meal.meal_id)
        self.assertEqual(meal.user_id, 1)
        self.assertEqual(meal.type, "dinner")
        self.assertEqual(meal.date, date.today())
        
        # Check if meal exists in our database
        saved_meal = Meal.objects.get(meal_id=meal.meal_id)
        self.assertEqual(saved_meal.user_id, 1)
        self.assertEqual(saved_meal.type, "dinner")
        self.assertEqual(saved_meal.date, date.today())

class MealItemTestCase(TestCase):
    def setUp(self):
        # Create MealItem for tests
        self.meal_item1 = MealItem.objects.create( meal_id=1, product_id=1, gram_amount=200)

    def test_add_product(self):
        meal_item = MealItem.add_product(meal_id=1, product_id=1, gram_amount=200)

        # Check if mealItem was added correctly
        self.assertIsNotNone(meal_item)
        self.assertEqual(meal_item.gram_amount, 200)
        self.assertEqual(meal_item.meal_id, 1)
        self.assertEqual(meal_item.product_id, 1)

        # Check if mealItem exists in our database
        saved_product = MealItem.objects.get(meal_item_id=meal_item.meal_item_id)
        self.assertIsNotNone(saved_product)
        self.assertEqual(saved_product.meal_id, 1)
        self.assertEqual(saved_product.product_id, 1)
        self.assertEqual(saved_product.gram_amount, 200)

    def test_remove_product(self):
        # Get the product to remove
        product_to_remove = self.meal_item1
        product_to_remove_id = product_to_remove.meal_item_id

        # Remove the product from the meal
        MealItem.objects.filter(meal_item_id=product_to_remove_id).delete()

        # Check if the removed product no longer exists in the database
        self.assertFalse(MealItem.objects.filter(meal_item_id=product_to_remove_id).exists())

        '''test.'''