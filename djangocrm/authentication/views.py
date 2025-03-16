from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum(): #Validating username
            return JsonResponse({'username_error':'username can only contain alpanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():  #Validatin username
            return JsonResponse({'username_error':'username already in use choose another name'}, status=409)
        return JsonResponse({'username_valid': True})

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
   