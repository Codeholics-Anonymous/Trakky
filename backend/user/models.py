from django.db import models

class UserProfile(models.Model):
    userprofile_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False, blank=False)
    sex = models.CharField(max_length=1, default='-')
    weight = models.FloatField(null=True, blank=True, default=0.0)
    height = models.IntegerField(null=True, blank=True, default=0)
    activity_level = models.FloatField(null=True, blank=True, default=1)
    birth_date = models.DateField(null=True, blank=True, default='2000-01-01')
    daily_calory_demand = models.IntegerField(null=True, blank=True, default=0.0)
    user_goal = models.CharField(max_length=10, null=True, blank=True, default=0)

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
