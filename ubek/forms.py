from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile, PostWall




class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'})
    )


    password1 = forms.CharField(
        label= ("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label= ("Password confirmation"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation', 'class': 'form-control'}),
        strip=False,
    )

    class Meta:
        User = get_user_model()
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username' : forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email address', 'class': 'form-control'}),
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class EditProfile(ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'rows':13, 'cols': 70}))
    class Meta:
        model = Profile
        fields = ['birth_date', 'profile_photo', 'about', 'visible']
        widgets = {
            'birth_date' : DateInput(attrs={'class': 'form-control'}),
        }

class EditUserForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    class Meta:
        User = get_user_model()
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email address', 'class': 'form-control'}),
        }

class PostForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'What are you thinking?',
                                                        'class': 'form-control',
                                                        'style': 'height: 70px;width:700px'}))
    class Meta:
        model = PostWall
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title', 'class': 'form-control'}),
        }

class EditPostForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'What are you thinking?',
                                                        'class': 'form-control',
                                                        'style': 'height: 70px;width:700px'}))
    class Meta:
        model = PostWall
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title', 'class': 'form-control'}),
        }