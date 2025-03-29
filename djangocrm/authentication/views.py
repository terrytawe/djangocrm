import json
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email # type: ignore
from django.contrib import messages, auth
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import TokenGenerator



#--------------------------------------------------------------------------------------------------    
# Create your views here.
#--------------------------------------------------------------------------------------------------    

#--------------------------------------------------------------------------------------------------    
#View to validate username
#--------------------------------------------------------------------------------------------------    
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum(): #Validating username
            return JsonResponse({'username_error':'username can only contain alpanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():  #Validatin username
            return JsonResponse({'username_error':'An account already exists with this username.'}, status=409)
        return JsonResponse({'username_valid': True})

#--------------------------------------------------------------------------------------------------    
#View to validate email
#--------------------------------------------------------------------------------------------------    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'useremail_error':'invalid email supplied'}, status=400)
        if User.objects.filter(email=email).exists():  #Validatin username
            return JsonResponse({'useremail_error':'An account already exists with this email.'}, status=409)
        return JsonResponse({'useremail_valid': True})

#--------------------------------------------------------------------------------------------------       
#View to render registration page
#--------------------------------------------------------------------------------------------------    

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
 
        context = {
           'fieldValues': request.POST
        }

        print(request.POST)

        if not User.objects.filter(username=username).exists():           
            if not User.objects.filter(email=email).exists():             
                if len(password) < 8:                    
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
       
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': TokenGenerator.make_token(user)})
                activate_url = 'http://' + get_current_site(request).domain + link

                email_subject = 'Activate your account'
                email_body = f"""
                                    Hi {user.username}, Your Django CRM account 
                                    has been created successfully.  
                                                                       
                                    Proceed to activate your account using the link below: 
                                    {activate_url}

                                    """
                email_sender = 'noreply.developer00@gmail.com'
                email_recipient = [email,]

                send_mail(
                    email_subject,
                    email_body,
                    email_sender,
                    email_recipient,
                    fail_silently=False,
                )

                message_success = 'Account successfully created. click <a href="' + activate_url +'">here</a> to login'
                         
                messages.success(request, message_success, extra_tags='safe')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')
   
#--------------------------------------------------------------------------------------------------    
#View to render login page
#--------------------------------------------------------------------------------------------------    
class ActivationView(View):
    def get(self, request, uidb64):
        return redirect('login')



#--------------------------------------------------------------------------------------------------    
#View to render login page
#--------------------------------------------------------------------------------------------------    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

#--------------------------------------------------------------------------------------------------    
#View to render password reset page
#--------------------------------------------------------------------------------------------------    
class PasswordResetView(View):
    def get(self, request):
        return render(request, 'authentication/password-reset.html')

#--------------------------------------------------------------------------------------------------    
#View to render new password page
#--------------------------------------------------------------------------------------------------    
class PasswordNewView(View):
    def get(self, request):
        return render(request, 'authentication/password-new.html')
   