from django.contrib import admin
from user.models import UserProfile

@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ['userprofile_id', 'user_id', 'sex', 'weight', 'height', 'work_type', 'daily_calory_demand']