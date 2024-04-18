from django.test import TestCase
from .models import *
from datetime import date

# Create your tests here.
"""
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
"""

# unit test for Demand class
"""
class DemandTestCase(TestCase):
    def test_create_demand_object(self):
        demand = Demand(user_id = 1, daily_calory_demand = 2000, date = date.today())

        self.assertEqual(demand.user_id, 1)
        self.assertEqual(demand.daily_calory_demand, 2000)
        self.assertEqual(demand.date, date.today())

    def test_demand_update_calories(self):
        demand = Demand(user_id = 1, daily_calory_demand = 0, date = date.today(), protein=120, fat=60, carbohydrates=200)

        demand.update_calories(1, 0, 0, 0)

        self.assertEqual(demand.protein, 120)
        self.assertEqual(demand.fat, 60)
        self.assertEqual(demand.carbohydrates, 200)
        self.assertTrue(demand.daily_calory_demand, 4*120 + 4*60 + 9*200)

        demand.update_calories(1, 30, 20, 10)

        self.assertEqual(demand.protein, 150)
        self.assertEqual(demand.fat, 80)
        self.assertEqual(demand.carbohydrates, 210)
        self.assertEqual(demand.daily_calory_demand, 4*150 + 4*80 + 9*210)

        demand.update_calories(0, 10, 20, 30)

        self.assertEqual(demand.protein, 140)
        self.assertEqual(demand.fat, 60)
        self.assertEqual(demand.carbohydrates, 180)
        self.assertEqual(demand.daily_calory_demand, 4*140 + 4*60 + 9*180)
"""

# unit tests for Summary class

"""class SummaryTestCase(TestCase):
    def test_create_summary_object(self):
        summary = Summary(user_id = 1, daily_calory_intake = 2000, date = date.today(), protein = 125, fat = 125, carbohydrates = 111)

        self.assertIsNotNone(summary)
        self.assertEqual(summary.user_id, 1)
        self.assertEqual(summary.daily_calory_intake, 2000)
        self.assertEqual(summary.date, date.today())
        self.assertEqual(summary.protein, 125)
        self.assertEqual(summary.date, 125)
        self.assertEqual(summary.date, 111)
    
    def test_summary_update_calories(self):
        summary = Summary(user_id = 1, date = date.today(), protein = 0, carbohydrates = 0, fat = 0)

        summary.update_calories(protein = 20, fat = 0, carbohydrates = 30) # we have to add input values to current macro

        self.assertEqual(summary.protein, 100)
        self.assertEqual(summary.carbohydrates, 150)
        self.assertEqual(summary.fat, 60)
        self.assertEqual(summary.daily_calory_intake, summary.protein * 4 + summary.carbohydrates * 4 + summary.fat * 9)
    """

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

        print(Product.objects.all().values())

        # Check if first product was updated correctly
        self.assertIsNotNone(updated_product)
        self.assertEqual(updated_product.name, "cake")
        self.assertEqual(updated_product.calories_per_hundred_grams, 200)

        # Check if other records are same as before
        unchanged_product = Product.objects.get(product_id=self.product2.product_id)
        self.assertEqual(unchanged_product.name, "orange")
        self.assertEqual(unchanged_product.calories_per_hundred_grams, 60)

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

class MealItem():
    ...
