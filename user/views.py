from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import auth
from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required


def forgot_password_view(request):
    if request.method == 'GET':
        return render(request, 'forgot_password.html')


def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.data.get('username'), password=form.data.get('password'))
            login(request, user)
            if user is not None:
                return redirect('/')
            else:
                form.add_error(field='username', error='Invalid password or login')
                return render(request, 'user/login.html', {'form': form})
        else:
            return render(request, 'user/login.html', {'form': form})


def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_data = auth.authenticate(request, email=user.email, password=form.data.get('password'))
            if auth_data is not None:
                login(request, auth_data)
                return redirect('/')
            return redirect('/auth/login/')
        return render(request, 'user/register.html', {'form': form})


def logout_view(request):
    auth.logout(request)
    return redirect('/auth/login')

def profile_view(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'user/settings.html')
        else:
            return redirect('/auth/login/')