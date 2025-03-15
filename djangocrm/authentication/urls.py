from .views import RegistrationView
from .views import LoginView
from .views import PasswordResetView
from .views import PasswordNewView
from django.urls import path

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('password-new', PasswordNewView.as_view(), name="password-new"),
    path('password-reset', PasswordResetView.as_view(), name="password-register"),
]
