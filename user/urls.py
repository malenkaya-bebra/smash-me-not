from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, logout_view, register_view, forgot_password_view, profile_view, profile_edit

app_name = 'auth'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='edit_profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/request_password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
