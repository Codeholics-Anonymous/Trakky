from django.db import models
from django.core.validators import MaxValueValidator
from datetime import datetime, date
from user.models import UserProfile


class Macros(models.Model):
    protein = models.PositiveIntegerField(null=True, blank=True, default=0, validators=[MaxValueValidator(250)])
    carbohydrates = models.PositiveIntegerField(null=True, blank=True, default=0, validators=[MaxValueValidator(1000)])
    fat = models.PositiveIntegerField(null=True, blank=True, default=0, validators=[MaxValueValidator(200)])

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
    name = models.CharField(max_length=250, blank=False, null=False)
    calories_per_hundred_grams = models.PositiveIntegerField(blank=True, null=True) # it will be calculated using protein, carbohydrates and fat

    @classmethod
    def add_product(cls, name, protein, carbohydrates, fat):
        new_product = cls(name=name, protein=protein, carbohydrates=carbohydrates, fat=fat, calories_per_hundred_grams=(4*protein + 4*carbohydrates + 9*fat))
        new_product.save()
        return new_product

    @classmethod
    def update_product(cls, product_id, new_name, new_protein, new_carbohydrates, new_fat):
        try:
            product = cls.objects.get(product_id=product_id)
            product.name = new_name
            product.protein = new_protein
            product.carbohydrates = new_carbohydrates
            product.fat = new_fat
            product.save()
            return product
        except cls.DoesNotExist:
            return None

class Demand(Macros):
    demand_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    daily_calory_demand = models.IntegerField(null=True, blank=True, default=0)  # To pole będzie obliczane automatycznie
    date = models.DateField(null=True, auto_now_add=True, blank=True)

    @classmethod
    def update_calories(cls, user_id, protein, fat, carbohydrates):
        try:
            demand = cls.objects.get(user_id=user_id,date=date.today())
            demand.protein = protein
            demand.fat = fat
            demand.carbohydrates = carbohydrates
            demand.daily_calory_demand = protein * 4 + carbohydrates * 4 + fat * 9
            demand.save()
            return demand
        except cls.DoesNotExist:
            return None

    @classmethod
    def create_demand(cls, user_id, date, protein=0, carbohydrates=0, fat=0):
        # Tworzenie nowego obiektu Demand
        new_demand = cls(
            user_id=user_id,
            date=date,
            protein=protein,
            carbohydrates=carbohydrates,
            fat=fat
        )
        # Obliczanie i ustawienie daily_calory_demand na podstawie wartości makroskładników
        new_demand.daily_calory_demand = new_demand.calculate_daily_calory_demand()
        new_demand.save()
        return new_demand

class Summary(Macros):
    summary_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    daily_calory_intake = models.IntegerField()
    date = models.DateField()

    @classmethod
    def update_calories(cls, user_id, increase, fat, protein, carbohydrates, date):
        try:
            summary = cls.objects.get(user_id=user_id, date=date)
            summary.protein = protein
            summary.carbohydrates = carbohydrates
            summary.fat = fat
            change = (protein * 4) + (carbohydrates * 4) + (fat * 9)
            if increase:
                summary.daily_calory_intake += change
            else:
                summary.daily_calory_intake -= change
            summary.save()
            return summary
        except cls.DoesNotExist:
            return None

    @classmethod
    def create_summary(cls, user_id, date, fat=0, protein=0, carbohydrates=0):
        calories = (protein * 4) + (carbohydrates * 4) + (fat * 9)

        new_summary = cls(
            user_id=user_id,
            date=date,
            daily_calory_intake=calories
        )
        new_summary.save()
        return new_summary

class Meal(models.Model):
    meal_id = models.AutoField(primary_key=True)
    user_profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=250)
    date = models.DateField()

    @classmethod
    def add_meal(cls, user_profile_id, type, date):
        meal = cls(user_profile_id=user_profile_id, type=type, date=date)
        meal.save()
        return meal

class MealItem(models.Model):
    meal_item_id = models.AutoField(primary_key=True)
    meal_id = models.ForeignKey(Meal, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    gram_amount = models.IntegerField()

    @classmethod
    def add_product(cls, meal_id, product_id, gram_amount):
        meal_item = cls(meal_id=meal_id, product_id=product_id, gram_amount=gram_amount)
        meal_item.save()
        return meal_item

    @classmethod
    def remove_product(cls, id):
        return MealItem.objects.get(meal_item_id=id).delete()
