from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import UserProfile
from .serializers import UserProfileSerializer
import datetime

class AuthenticationTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_login(self):
        url = reverse('login')  # 'login' is our endpoint
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_registration(self):
        url = reverse('register')  # 'register' is our endpoint
        new_user_data = {
            'username': 'new_user',
            'password': 'new_password'
        }
        response = self.client.post(url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username=new_user_data['username']).exists())  # Check if user was correctly registered

    def test_logout(self):
        url = reverse('logout')  # 'logout' endpoint
        self.client.force_authenticate(user=self.user) # force user authenticate
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserProfileTestCase(TestCase):
    def setUp(self):
        # Create temporary user and profile for tests
        self.userM = User.objects.create_user(username='testuserM', email='test@example.com', password='testpasswordM')
        self.userF = User.objects.create_user(username='testuserF', email='test@example.com', password='testpasswordF')
        self.profileM = UserProfile.objects.create(user_id=self.userM.id, weight=70, activity_level=1.1, sex='M')
        self.profileF = UserProfile.objects.create(user_id=self.userF.id, weight=55, activity_level=1.5, sex='F')

    def test_update_profile(self):
        # Check update_profile method of user
        dataM = {
            'user_id' : self.profileM.user_id,
            'weight' : 75,
            'height' : 175,
            'birth_date' : '2000-01-01'
        }
        serializerM = UserProfileSerializer(self.profileM, data=dataM)
        UserProfile.update_profile(serializerM)
        self.assertEqual(self.profileM.weight, 75)
        self.assertEqual(self.profileM.height, 175)
        self.assertEqual(self.profileM.birth_date, datetime.date(2000, 1, 1))

        dataF = {
            'user_id' : self.profileF.user_id,
            'weight' : 60
        }
        serializerF = UserProfileSerializer(self.profileF, data=dataF)
        UserProfile.update_profile(serializerF)
        self.assertEqual(self.profileF.weight, 60)
        

    def test_calculate_demand(self):
        # Check if calculate_demand adds demand to Demand database
        self.profileM.calculate_demand() # it has to add demand to database
        saved_demand = Demand.objects.filter(user_id=profileM.user_id, daily_calory_demand=profileM.daily_calory_demand)
        self.assertTrue(saved_demand.exists()) # we found at least one element
        #self.assertEqual(self.profileF.daily_calory_demand, 60 * 22 * self.profileF.activity_level)
        #self.assertEqual(self.profileM.daily_calory_demand, 75 * 24 * self.profileM.activity_level)

    def tearDown(self):
        # Clear database
        self.userM.delete()
        self.userF.delete()
        self.profileM.delete()
        self.profileF.delete()