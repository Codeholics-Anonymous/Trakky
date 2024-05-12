from django.db import models
from django.contrib.auth.models import User
from django.core.validators import ValidationError

def validate_user_gender(value):
    if (value not in ('Male', 'Female', 'Other')):
        raise ValidationError("Incorrect gender.")

def validate_user_goal(value):
    if (value not in ('Lose Weight', 'Gain Weight', 'Maintain Weight')):
        raise ValidationError("Incorrect weight goal.")

class UserProfile(models.Model):
    userprofile_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=6, validators=[validate_user_gender], null=False, blank=False)
    weight = models.FloatField(null=False, blank=False)
    height = models.IntegerField(null=False, blank=False)
    activity_level = models.FloatField(null=False, blank=False, default=1) #TODO MAKE CHOICES TO CONVERT STRING DATA INTO NUMBERS TO EASILY CALCULATE CALORIC NEEDS
    birth_date = models.DateField(null=False, blank=False)
    daily_calory_demand = models.IntegerField(null=True, blank=True)
    user_goal = models.CharField(max_length=15, null=False, blank=False)

    @classmethod
    def update_profile(cls, serializer):
        if serializer.is_valid():
            serializer.save()
            return True
        else:
            return False

    @classmethod
    def calculate_demand(cls, weight, height, birth_date, activity_level):
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return activity_level*((10 * weight) + (6.25 * height) + (5 * age))
