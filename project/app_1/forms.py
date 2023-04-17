from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import get_user_model
from django import forms

from .models import *


# User = get_user_model()

class AddPostForm(forms.ModelForm):
    # fields = ['name', 'text', 'images']
    # images = forms.ImageField(label='Картинка')
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-input'}))
    text = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    class Meta:
        model = Post
        fields = ['name', 'text', 'images']
        # images = forms.ImageField(label='Картинка')
        # name = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
        # text = forms.CharField(label='Password', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-input'}),
        #     'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        # }

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    # avatar = forms.ImageField(label='Аватар')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'avatar', 'email', 'password1', 'password2') # 'first_name', 'last_name',
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }

class ProfileForm(forms.ModelForm):

    username = forms.CharField(label='Логин')

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'first_name', 'last_name']#, 'avatar'
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-input'}),
        #     'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        # }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        # widgets = {
        #     'text': forms.TextInput(attrs={'class': 'form-input'}),
        #     # 'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        # }
class VipForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['vip']

    def clean_vip(self):
        vip = self.cleaned_data['vip']
        if vip != '1932':
            raise forms.ValidationError('Неверный пароль')
        else:
            vip = 1
        return vip
