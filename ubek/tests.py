from django.test import TestCase
from .models import Profile, User, PostWall
from django.contrib.auth import get_user_model
from .forms import EditPostForm


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


class CanSeeMethodTest(TestCase):

    def test_can_see_profile_method_default_visible(self):
        profile1 = User.objects.create_user('test', 'test@test.com', 'testtesttest')
        profile2 = User.objects.create_user('test2', 'test2@test.com', 'testtesttest2')
        self.assertIs(profile1.profile.can_not_see_profile(profile2), False)

    def test_can_see_profile_method_general(self):
        profile1 = User.objects.create_user('test', 'test@test.com', 'testtesttest')
        profile1.profile.visible = False
        profile2 = User.objects.create_user('test2', 'test2@test.com', 'testtesttest2')
        self.assertIs(profile1.profile.can_not_see_profile(profile2), True)

    def test_can_see_profile_method_is_friend(self):
        profile1 = User.objects.create_user('test', 'test@test.com', 'testtesttest')
        profile1.profile.visible = False
        profile2 = User.objects.create_user('test2', 'test2@test.com', 'testtesttest2')
        profile1.friends.add(profile2)
        self.assertFalse(profile1.profile.can_not_see_profile(profile2))


class EditPostFormTest(TestCase):

    def test_editpost_by_author(self):
        author = User.objects.create_user('test', 'test@test.com', 'testtesttest')
        logged_user = author
        post = EditPostForm(data={
            'user': author,
            'title': 'test title',
            'text': 'lorem ipsum'
        })
        if logged_user == author and post.is_valid():
            post.save()
            return 'Post Updated'

        self.assertEqual('return', 'Post Updated')

    def test_editpost_by_other_user_than_author(self):
        author = User.objects.create_user('test', 'test@test.com', 'testtesttest')
        logged_user = User.objects.create_user('test2', 'test2@test2.com', 'testtesttest2')
        post = EditPostForm(data={
            'user': author,
            'title': 'test title',
            'text': 'lorem ipsum'
        })
        if logged_user == author and post.is_valid():
            post.save()
            return 'Post Updated'
        else:
            return "Logged user is not author of this post so he cannot edit it"

        self.assertEqual("return", "Logged user is not author of this post so he cannot edit it")