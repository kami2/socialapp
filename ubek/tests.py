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
        self.test_user = test_user


    def test_login_user_incorrect(self):
        data_test = {"username" : "test", "password" : "test_password"}
        response = self.client.post('/login/', data_test, follow=True)
        messages = list(response.context['messages'])
        status_code = response.status_code
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Username OR password is incorrect')
        self.assertEqual(status_code, 200)


    def test_login_user_correct(self):
        user = User.objects.create_user(username='testuser', password='12345')
        data_test = {"username" : "testuser", "password" : "12345"}
        response = self.client.post('/login/', data_test, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/profile/' + str(user.id) + '/' )


