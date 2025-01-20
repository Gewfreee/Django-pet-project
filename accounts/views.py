from django.contrib.auth import  login, logout, authenticate
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm, ForgotPasswordForm, ResetPasswordForm
from django.contrib.auth.decorators import login_required
from .tasks import send_reset_code_email
from library.models import User
from .models import Password_reset_code
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string


def SignUpView(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
        print(form.errors)
        return render(request, 'signup.html', {'form': form})

    form = SignUpForm()
    return render(request, 'signup.html', {'form' : form})

def LogInView(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LogInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
        print(form.errors)
        return render(request, 'login.html', {'form': form})

    form = LogInForm()
    return render(request, 'login.html', {'form': form})

@login_required
def LogOutView(request):
    logout(request)
    return redirect('main')

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                reset_code = get_random_string(length=6)
                Password_reset_code.objects.filter(user=user).delete()
                Password_reset_code.objects.create(user=user, code=reset_code)
                send_reset_code_email.delay(user.id, reset_code)
                return redirect('reset_password')
            except User.DoesNotExist:
                form.add_error('email', 'Invalid email.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            reset_code = Password_reset_code.objects.filter(code=code).order_by('-created_at').first()
            if reset_code is None:
                form.add_error('code', 'Invalid or expired reset code.')
                return render(request, 'password_reset.html', {'form' : form})
            if new_password and confirm_password and new_password != confirm_password:
                form.add_error('confirm_password', 'Passwords don\'t match')
                return render(request, 'password_reset.html', {'form': form})
            user = reset_code.user
            if reset_code.code == code:
                Password_reset_code.objects.filter(code=code).delete()
            user.password = make_password(new_password)
            user.save()
            reset_code.delete()
            return redirect('login')
    else:
        form = ResetPasswordForm()
    return render(request, 'password_reset.html', {'form': form})