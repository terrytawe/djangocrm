from django.shortcuts import render
from django.views import View

# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
class PasswordResetView(View):
    def get(self, request):
        return render(request, 'authentication/password-reset.html')
    
class PasswordNewView(View):
    def get(self, request):
        return render(request, 'authentication/password-new.html')