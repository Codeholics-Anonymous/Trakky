from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile 
        exclude = ['user', 'daily_calory_demand']

    def get_user_goal_description(self, obj):
        if obj.user_goal == -1:
            return "Lose Weight"
        elif obj.user_goal == 0:
            return "Maintain Weight"
        elif obj.user_goal == 1:
            return "Gain Weight"
        return "Unknown Goal"

    def get_work_type_description(self, obj):
        if obj.work_type == 0:
            return "Mental Work"
        elif obj.work_type == 1:
            return "Physical Work"
        return "Unknown Work"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['work_type'] = self.get_work_type_description(instance)
        representation['user_goal'] = self.get_user_goal_description(instance)
        return representation