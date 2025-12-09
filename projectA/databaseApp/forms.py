from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms 
from django.forms.widgets import PasswordInput, TextInput
from .models import Post, Comment


class CreateUserForm(UserCreationForm):
    email= forms.EmailField(required=True)
    first_name= forms.CharField(required=True)
    last_name= forms.CharField(required=True)
    phone= forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','phone', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username =  forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ "body"]