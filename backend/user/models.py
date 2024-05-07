from django.db import models

# Create your models here.

class UserProfile(models.Model):
    userprofile_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False, blank=False)
    sex = models.CharField(max_length=1)
    weight = models.FloatField(null=True, blank=True, default=0.0)
    height = models.IntegerField(null=True, blank=True, default=0)
    activity_level = models.FloatField(null=True, blank=True, default=1)
    daily_calory_demand = models.IntegerField(null=True, blank=True, default=0.0)

    @classmethod
    def update_profile(cls, serializer):
        if serializer.is_valid():
            serializer.save()
            return True
        else:
            return False

    def calculate_demand(self):
        ...
