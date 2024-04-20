from django.urls import reverse
from .models import Profile
from .forms import LoginForm, RegisterForm, ProfileForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# from django.contrib.auth.decorators import login_required


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
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile, created = Profile.objects.get_or_create(user=user)
            auth_data = authenticate(request, email=user.email, password=form.cleaned_data.get('password'))
            if auth_data is not None:
                login(request, auth_data)
                return redirect('/')
            else:
                return redirect('/auth/login/')
        else:
            return render(request, 'user/register.html', {'form': form})


def logout_view(request):
    auth.logout(request)
    return redirect('/auth/login')


def profile_edit(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)

        if request.method == 'GET':
            form = ProfileForm(instance=profile)
            return render(request, 'user/settings.html', {'form': form})

        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                profile.bio = form.cleaned_data['bio']
                if 'avatar' in request.FILES:
                    profile.avatar = request.FILES['avatar']
                    print('Avatar uploaded:', profile.avatar)

                if 'photos' in request.FILES:
                    photos = request.FILES.getlist('photos')[:6]
                    for i, photo in enumerate(photos):
                        setattr(profile, f'photo_{i + 1}', photo)
                profile.save()
                return HttpResponseRedirect(reverse('auth:profile'))
    else:
        return redirect('login')


def profile_view(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)

        return render(request, 'user/profile.html', {'profile': profile})
    else:
        return redirect('login')
