from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import UserProfile
from .serializers import UserProfileSerializer
import datetime
from rest_framework.authtoken.models import Token

class AuthenticationTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

    def test_login(self):
        url = reverse('login')  # 'login' is our endpoint
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_registration(self):
        url = reverse('register')  # 'register' is our endpoint
        new_user_data = {
            'register_data' : {
                'username': 'new_user',
                'password': 'password1'
            },
            'userprofile_data' : {
                'sex' : 'O',
                'user_goal' : 0,
                'work_type' : 0,
                'birth_date' : '2000-01-01',
                'weight' : 80,
                'height' : 180
            }
        }
        response = self.client.post(url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username='new_user').exists())  # Check if user was correctly registered

    def test_logout(self):
        url = reverse('logout')  # 'logout' endpoint
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from utils.date import calculate_age

class UserProfileTestCase(TestCase):
    def setUp(self):
        # Create temporary user and profile for tests
        self.userM = User.objects.create_user(username='testuserM', email='test@example.com', password='testpasswordM')
        self.userF = User.objects.create_user(username='testuserF', email='test@example.com', password='testpasswordF')
        self.profileM = UserProfile.objects.create(user_id=self.userM.id, weight=70, height=170, birth_date='1999-01-01', sex='M', work_type=1, user_goal=0)
        self.profileF = UserProfile.objects.create(user_id=self.userF.id, weight=55, height=160, birth_date='1998-01-01', sex='F', work_type=0, user_goal=1)

    def test_update_profile(self):
        # Check update_profile method of user
        dataM = {
            'user_id' : self.profileM.user_id,
            'weight' : 75,
            'height' : 175,
            'birth_date' : '2000-01-01',
            'work_type' : 0,
            'user_goal' : 1,
            'sex' : 'M'
        }
        serializerM = UserProfileSerializer(self.profileM, data=dataM)
        UserProfile.update_profile(serializerM)
        self.assertEqual(self.profileM.user_id, self.profileM.user_id)
        self.assertEqual(self.profileM.weight, 75)
        self.assertEqual(self.profileM.height, 175)
        self.assertEqual(self.profileM.birth_date, datetime.date(2000, 1, 1))
        self.assertEqual(self.profileM.work_type, 0)
        self.assertEqual(self.profileM.user_goal, 1)
        self.assertEqual(self.profileM.sex, 'M')

        dataF = {
            'user_id' : self.profileF.user_id,
            'weight' : 60,
            'height' : 160,
            'birth_date' : '2002-01-01',
            'work_type' : 1,
            'user_goal' : 0,
            'sex' : 'F'
        }

        serializerF = UserProfileSerializer(self.profileF, data=dataF)
        UserProfile.update_profile(serializerF)
        self.assertEqual(self.profileF.user_id, self.profileF.user_id)
        self.assertEqual(self.profileF.weight, 60)
        self.assertEqual(self.profileF.height, 160)
        self.assertEqual(self.profileF.birth_date, datetime.date(2002, 1, 1))
        self.assertEqual(self.profileF.work_type, 1)
        self.assertEqual(self.profileF.user_goal, 0)
        self.assertEqual(self.profileF.sex, 'F')
        
    def test_calculate_demand(self):
        BMR_M = (10 * self.profileM.weight) + (6.25 * self.profileM.height) - (5 * calculate_age(self.profileM.birth_date)) + 5
        NEAT_M = 0.5*BMR_M
        demand_M = round(BMR_M + NEAT_M)
        self.assertEqual(UserProfile.calculate_demand(weight=self.profileM.weight, height=self.profileM.height, birth_date=self.profileM.birth_date, work_type=self.profileM.work_type, sex='M', user_goal=self.profileM.user_goal), demand_M)
        BMR_F = (10 * self.profileF.weight) + (6.25 * self.profileF.height) - (5 * calculate_age(self.profileF.birth_date)) - 161
        NEAT_F = 0.3*BMR_F
        demand_F = round(BMR_F + NEAT_F + 200)
        self.assertEqual(UserProfile.calculate_demand(weight=self.profileF.weight, height=self.profileF.height, birth_date=self.profileF.birth_date, work_type=self.profileF.work_type, sex='F', user_goal=self.profileF.user_goal), demand_F)