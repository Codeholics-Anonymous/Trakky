from django.test import TestCase

# Create your tests here.

"""
class UserTestCase(TestCase):
    def test_login(self):
        user = User(username='testuser', password='password123')
        self.assertTrue(user.login())  # Zakładamy, że metoda login zwraca True przy poprawnym logowaniu

    def test_logout(self):
        user = User(username='testuser', password='password123')
        user.login()
        self.assertTrue(user.logout())  # Zakładamy, że metoda logout zwraca True przy poprawnym wylogowaniu

    def test_register(self):
        user = User(username='newuser', password='newpassword123')
        self.assertTrue(user.register())  # Zakładamy, że metoda register zwraca True przy poprawnej rejestracji

class UserProfileTestCase(TestCase):
    def test_updateProfile(self):
        # Testowanie metody updateProfile
        user_profile = UserProfile(userID=1, weight=70, dailyCaloricDemand=2500)
        user_profile.weight = 75  # Aktualizacja wagi
        self.assertTrue(user_profile.updateProfile())  # Zakładamy, że metoda updateProfile zwraca True przy poprawnej aktualizacji

    def test_calculateDemand(self):
        # Testowanie metody calculateDemand
        user_profile = UserProfile(userID=1, weight=70, dailyCaloricDemand=2500)
        self.assertEqual(user_profile.calculateDemand(), 2600)  # Zakładamy, że metoda calculateDemand zwraca nowe zapotrzebowanie kaloryczne
"""