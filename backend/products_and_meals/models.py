from django.db import models

class Macros(models.Model):
    protein = models.IntegerField()
    carbohydrates = models.IntegerField()
    fat = models.IntegerField()

    def update_macros(self, protein, carbohydrates, fat):

        if (protein <= 0 or carbohydrates <= 0 or fat <= 0):
            return False
        
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fat = fat

        return True

    class Meta:
        abstract = True

class Demand(Macros):
    user_id = models.IntegerField()
    daily_calory_demand = models.IntegerField()
    date = models.DateField()

    def update_calories(self, increase, protein, fat, carbohydrates):
        ...

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    calories_per_hundred_grams = models.IntegerField()

    @classmethod
    def add_product(cls, name, calories_per_hundred_grams):
        new_product = cls(name=name, calories_per_hundred_grams=calories_per_hundred_grams)
        new_product.save()
        return new_product

    @classmethod
    def update_product(cls, product_id, new_name, new_calories):
        try:
            product = cls.objects.get(product_id=product_id)
            product.name = new_name
            product.calories_per_hundred_grams = new_calories
            product.save()
            return product
        except cls.DoesNotExist:
            # Obsłużenie przypadku, gdy produkt o podanym ID nie istnieje
            return None