from django.db import models
from django.contrib.auth.models import User
from datetime import date
from utils.user_utils import gender_validation
from utils.date import date_validation, age_validation
from django.core.validators import MaxValueValidator

class UserProfile(models.Model):
    userprofile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, null=False, blank=False, validators=[gender_validation])
    weight = models.FloatField(null=False, blank=False, validators=[MaxValueValidator(635)])
    height = models.IntegerField(null=False, blank=False, validators=[MaxValueValidator(272)])
    work_type = models.IntegerField(null=False, blank=False)
    birth_date = models.DateField(null=False, blank=False, validators=[date_validation, age_validation])
    daily_calory_demand = models.IntegerField(null=True, blank=True)
    user_goal = models.IntegerField(null=False, blank=False)

    @classmethod
    def update_profile(cls, serializer):
        if serializer.is_valid():
            new_demand = cls.calculate_demand(
                weight=serializer.validated_data['weight'],
                height=serializer.validated_data['height'],
                birth_date=serializer.validated_data['birth_date'],
                work_type=serializer.validated_data['work_type'],
                sex=serializer.validated_data['sex'],
                user_goal=serializer.validated_data['user_goal']
                )
            serializer.validated_data['daily_calory_demand'] = new_demand
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
            BMR = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            BMR = (10 * weight) + (6.25 * height) - (5 * age) - 161
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
        return round(result)
