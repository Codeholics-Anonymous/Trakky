from django.db import models
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from datetime import date

class UserProfile(models.Model):
    userprofile_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=1, null=False, blank=False)
    weight = models.FloatField(null=False, blank=False)
    height = models.IntegerField(null=False, blank=False)
    work_type = models.IntegerField(null=False, blank=False)
    birth_date = models.DateField(null=False, blank=False)
    daily_calory_demand = models.IntegerField(null=True, blank=True)
    user_goal = models.IntegerField(null=False, blank=False)

    @classmethod
    def update_profile(cls, serializer):
        if serializer.is_valid():
            serializer.save()
            return True
        else:
            return False

    @classmethod
    def calculate_demand(cls, weight, height, birth_date, work_type, sex, user_goal):
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        # BMR - Basal metabolic rate
        if (sex == 'M'):
            BMR = (10 * weight) + (6.25 * height) + (5 * age) + 5
        else:
            BMR = (10 * weight) + (6.25 * height) + (5 * age) - 161
        # NEAT - Number of calories burned per day
        if (work_type == 1): # Physical work
            NEAT = BMR*0.4
        else: # Mental work
            NEAT = BMR*0.2
        result = BMR + NEAT
        # CHECK USER GOAL
        if (user_goal == -1):
            result -= 200
        elif (user_goal == 1):
            result += 200
        return result
