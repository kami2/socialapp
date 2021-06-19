from django.test import TestCase
from .models import Profile, User
from django.contrib.auth import get_user_model


# Create your tests here.
User = get_user_model()

class URLTest(TestCase):
    def test_is_homepage_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_is_loginpage_response(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)


class ProfileModelTest(TestCase):
    def test_profile_str_return(self):
        profile = User.objects.create_user('test', 'test@test.com', 'testtesttest')
        self.assertEqual(str(profile), 'test')


class LoginUserTest(TestCase):

    def setUp(self):
        test_user = User(username='test', email='test@test.com')
        test_user.set_password('testtesttest')
        test_user.save()
        self.test_user_user = test_user
        self.test_user_pw = test_user.password


    def test_login_user_view(self):
        data = {"username" : "test", "password" : self.test_user_pw}
        response = self.client.post('/login/', data, follow=True)
        status_code = response.status_code
        self.assertIs(self.test_user_user.is_authenticated, True)
        self.assertEqual(status_code, 200)

