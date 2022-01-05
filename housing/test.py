from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class LoginTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create(username="testuser")
        user.set_password("MyPassword")
        user.save()

    def test_correct_login_attempt(self):
        c = Client()
        logged_in = c.login(username="testuser", password="MyPassword")
        self.assertTrue(logged_in)

    def test_incorrect_login_attempt(self):
        c = Client()
        logged_in = c.login(username="testuser", password="NotMyPassword")
        self.assertFalse(logged_in)
