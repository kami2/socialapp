from django.test import TestCase
from .models import Profile, User

# Create your tests here.


class URLTest(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_loginpage(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)


class ProfileModelTest(TestCase):
    def test_profile_str_return(self):
        profile = User.objects.create_user('test', 'test@test.com', 'testtesttest')
        self.assertEqual(str(profile), 'test')


