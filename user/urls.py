from django.urls import path
from .views import login_view, logout_view, register_view, forgot_password_view, profile_view, profile_edit

app_name = 'auth'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='edit_profile'),
]
