from django.db import models


from django.db import models

class Macros(models.Model):
    protein = models.IntegerField()
    carbohydrates = models.IntegerField()
    fat = models.IntegerField()

    class Meta:
        abstract = True

class Product(Macros):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    calories_per_hundred_grams = models.IntegerField(blank=True, null=True)  # Ustawiamy jako opcjonalne

    def calculate_calories_per_hundred_grams(self):
        # Obliczamy kalorie na 100 gram na podstawie protein, carbohydrates i fat
        calories_from_protein = self.protein * 4
        calories_from_carbs = self.carbohydrates * 4
        calories_from_fat = self.fat * 9
        total_calories = calories_from_protein + calories_from_carbs + calories_from_fat
        return total_calories

    def clean(self):
        # Automatycznie obliczamy calories_per_hundred_grams, jeśli nie podano wartości
        if self.calories_per_hundred_grams is None:
            self.calories_per_hundred_grams = self.calculate_calories_per_hundred_grams()

    @classmethod
    def add_product(cls, name, calories_per_hundred_grams=None, protein=0, carbohydrates=0, fat=0):
        new_product = cls(name=name, calories_per_hundred_grams=calories_per_hundred_grams,
                          protein=protein, carbohydrates=carbohydrates, fat=fat)
        new_product.full_clean()  # Wywołujemy clean() przed zapisaniem
        new_product.save()
        return new_product

    @classmethod
    def update_product(cls, product_id, new_name, new_protein, new_carbohydrates, new_fat, new_calories=None):
        try:
            product = cls.objects.get(product_id=product_id)
            product.name = new_name
            product.protein = new_protein
            product.carbohydrates = new_carbohydrates
            product.fat = new_fat
            if new_calories is not None:
                product.calories_per_hundred_grams = new_calories
            else:
                # Obliczamy calories_per_hundred_grams na nowo
                product.calories_per_hundred_grams = product.calculate_calories_per_hundred_grams()
            product.full_clean()  # Wywołujemy clean() przed zapisaniem
            product.save()
            return product
        except cls.DoesNotExist:
            return None


class Demand(Macros):
    
    user_id = models.IntegerField()
    daily_calory_demand = models.IntegerField()
    date = models.DateField()
    
    def update_calories(self, increase, protein, fat, carbohydrates):
        ...