from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages

# Create your views here.

#View to validate username
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum(): #Validating username
            return JsonResponse({'username_error':'username can only contain alpanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():  #Validatin username
            return JsonResponse({'username_error':'An account already exists with this username.'}, status=409)
        return JsonResponse({'username_valid': True})

#View to validate email
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'useremail_error':'invalid email supplied'}, status=400)
        if User.objects.filter(email=email).exists():  #Validatin username
            return JsonResponse({'useremail_error':'An account already exists with this email.'}, status=409)
        return JsonResponse({'useremail_valid': True})

        
#View to render registration page
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        messages.success(request, 'Success Message')
        return render(request, 'authentication/register.html')

#View to render login page
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

#View to render password reset page
class PasswordResetView(View):
    def get(self, request):
        return render(request, 'authentication/password-reset.html')

#View to render new password page
class PasswordNewView(View):
    def get(self, request):
        return render(request, 'authentication/password-new.html')
   