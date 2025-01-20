from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from library.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={
        'placeholder' : 'Username or email',}))
    email = forms.CharField(label='email', widget=forms.EmailInput(attrs={
        'placeholder' : 'Email',}))
    password1 = forms.CharField(label='password1', widget=forms.PasswordInput(attrs={
        'placeholder' : 'Password',}))
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm a password',}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken')

        if '@' not in email:
            raise forms.ValidationError('Incorrect email')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')

        return cleaned_data


class LogInForm(AuthenticationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={
        'placeholder' : 'Username or email',}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={
        'placeholder' : 'Password',}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Invalid username or password')

        return cleaned_data


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder' : 'Email',}))


class ResetPasswordForm(forms.Form):
    code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'placeholder' : 'Code'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'New password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm a password'}))

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        return cleaned_data