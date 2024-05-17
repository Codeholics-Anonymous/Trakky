from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime, date
from user.models import UserProfile


class Macros(models.Model):
    protein = models.FloatField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])
    carbohydrates = models.FloatField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])
    fat = models.FloatField(null=True, blank=True, default=0, validators=[MinValueValidator(0)])

    class Meta:
        abstract = True

    def update_macros(self, protein, carbohydrates, fat):
        if (protein < 0 or carbohydrates < 0 or fat < 0):
            return False
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fat = fat
        return True

class Product(Macros):
    product_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True) # foreign key to user_id at django User class
    name = models.CharField(max_length=250, blank=False, null=False)

    @property
    def calories_per_hundred_grams(self):
        if (self.protein is not None) and (self.carbohydrates is not None) and (self.fat is not None):
            return round(4 * self.protein + 4 * self.carbohydrates + 9 * self.fat)

    @classmethod
    def add_product(cls, user_id, name, protein, carbohydrates, fat):
        new_product = cls(user_id=user_id, name=name, protein=protein, carbohydrates=carbohydrates, fat=fat)
        new_product.save()
        return new_product

    @classmethod
    def update_product(cls, product_id, name, protein, carbohydrates, fat):
        product = cls.objects.get(product_id=product_id)
        product.name = name
        product.protein = protein
        product.carbohydrates = carbohydrates
        product.fat = fat
        product.save()
        return product

    @classmethod
    def calculate_nutrition(cls, gram_amount, product): # calculate nutrition basing on different amount (g) of product
        factor = (gram_amount / 100) # we have information about 100g of product
        return (factor*product.protein, factor*product.carbohydrates, factor*product.fat)

class Demand(Macros):
    demand_id = models.AutoField(primary_key=True)
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    daily_calory_demand = models.PositiveIntegerField(null=False, blank=False, validators=[MaxValueValidator(12250)])
    date = models.DateField(null=True, blank=True)
    
    @classmethod
    def update_calories(cls, userprofile_id, protein, fat, carbohydrates, daily_calory_demand):
        try:
            demand = cls.objects.filter(userprofile_id=userprofile_id, date=date.today()).order_by('-demand_id').first() 
            demand.protein = protein
            demand.fat = fat
            demand.carbohydrates = carbohydrates
            demand.daily_calory_demand = daily_calory_demand
            demand.save()
            return demand
        except cls.DoesNotExist:
            return None

    @classmethod
    def create_demand(cls, userprofile_id, date, protein, carbohydrates, fat, daily_calory_demand):
        new_demand = cls(
            userprofile_id=userprofile_id,
            date=date,
            protein=protein,
            carbohydrates=carbohydrates,
            fat=fat,
            daily_calory_demand=daily_calory_demand
        )
        new_demand.save()
        return new_demand

class Summary(Macros):
    summary_id = models.AutoField(primary_key=True)
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    daily_calory_intake = models.PositiveIntegerField(null=False, blank=False)
    date = models.DateField()

    @classmethod
    def update_calories(cls, userprofile_id, increase, fat, protein, carbohydrates, date):
        try:
            summary = cls.objects.get(userprofile_id=userprofile_id, date=date)
            change = round((protein * 4) + (carbohydrates * 4) + (fat * 9))
            if increase:
                summary.daily_calory_intake = round(summary.daily_calory_intake + change, 1)
                summary.protein = round(summary.protein + protein, 1)
                summary.carbohydrates = round(summary.carbohydrates + carbohydrates, 1)
                summary.fat = round(summary.fat + fat, 1)
            else:
                summary.daily_calory_intake = round(summary.daily_calory_intake - change, 1)
                summary.protein = round(summary.protein - protein, 1)
                summary.carbohydrates = round(summary.carbohydrates - carbohydrates, 1)
                summary.fat = round(summary.fat - fat, 1)
            summary.save()
            return summary
        except cls.DoesNotExist:
            return None

    @classmethod
    def create_summary(cls, userprofile_id, date, fat=0, protein=0, carbohydrates=0):
        calories = round((protein * 4) + (carbohydrates * 4) + (fat * 9))

        new_summary = cls(
            userprofile_id=userprofile_id,
            date=date,
            daily_calory_intake=calories
        )
        new_summary.save()
        return new_summary

class Meal(models.Model):
    meal_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=250)
    date = models.DateField()

    @classmethod
    def add_meal(cls, user_id, type, date):
        meal = cls(user_id=user_id, type=type, date=date)
        meal.save()
        return meal

class MealItem(models.Model):
    meal_item_id = models.AutoField(primary_key=True)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, null=True, blank=True) # this field represents meal_id
    product_id = models.IntegerField(null=False, blank=False)
    gram_amount = models.PositiveIntegerField(null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(2000)])

    @classmethod
    def add_product(cls, meal_id, product_id, gram_amount):
        meal_item = cls(meal_id=meal_id, product_id=product_id, gram_amount=gram_amount)
        meal_item.save()
        return meal_item

    @classmethod
    def remove_product(cls, id):
        return cls.objects.get(meal_item_id=id).delete()
