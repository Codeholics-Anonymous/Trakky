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

# unit tests for Summary

class SummaryTestCase(TestCase):
    def test_create_summary_object(self):
        summary = Summary(user_id = 1, daily_calory_intake = 2000, date = date.today()) # create summary object

        # tests for summary object

        self.assertIsNotNone(summary)
        self.assertEqual(summary.user_id, 1)
        self.assertEqual(summary.daily_calory_intake, 2000)
        self.assertEqual(summary.date, date.today())
    
    def test_summary_update_calories(self):
        summary = Summary(user_id = 1, date = date.today(), protein = 120, carbohydrates = 200, fat = 50)

        summary.update_calories(100, 150, 60)

        self.assertEqual(summary.protein, 100)
        self.assertEqual(summary.carbohydrates, 150)
        self.assertEqual(summary.fat, 60)
        self.assertEqual(summary.daily_calory_intake, summary.protein * 4 + summary.carbohydrates * 4 + summary.fat * 9)