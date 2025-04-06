import json
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email # type: ignore
from django.contrib import messages, auth
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .utils import activation_token
from django.utils.html import strip_tags



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
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': activation_token.make_token(user)})
                activate_url = 'http://' + get_current_site(request).domain + link

                email_subject = 'Activate your account'
                # email_body = render_to_string('authentication/activation.html', {'username': username, 'link': activate_url})
                email_sender = 'noreply.developer00@gmail.com'
                email_recipient = [email,]

                html_content = render_to_string("authentication/activation.html", {
                    'username': username, 
                    'link': activate_url
                })

                email_body = strip_tags(html_content)
                email = EmailMultiAlternatives(
                    email_subject, 
                    email_body, 
                    email_sender, 
                    email_recipient
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)

                message_success = 'Your account has been successfully created. Please check your email and confirm'
                messages.success(request, message_success)

                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')
   
#--------------------------------------------------------------------------------------------------    
#View to render login page
#--------------------------------------------------------------------------------------------------    
class ActivationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')



#--------------------------------------------------------------------------------------------------    
#View to render login page
#--------------------------------------------------------------------------------------------------    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('expenses')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
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


#--------------------------------------------------------------------------------------------------    
#View to process logout action
#--------------------------------------------------------------------------------------------------    
class LogoutView(View):
    def get(self, request):

        # Clear any existing messages
        storage = messages.get_messages(request)
        list(storage)  # This consumes the generator and clears it

        auth.logout(request)

        messages.success(request, 'You have been logged out')
        return redirect('login')
   