from .views import RegistrationView, LoginView,PasswordResetView,PasswordNewView,UsernameValidationView, EmailValidationView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('password-new', PasswordNewView.as_view(), name="password-new"),
    path('password-reset', PasswordResetView.as_view(), name="password-register"),
    path('username-validation', csrf_exempt(UsernameValidationView.as_view()), name="username-validation"),
    path('email-validation', csrf_exempt(EmailValidationView.as_view()), name="email-validation"),
]
