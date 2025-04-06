import os, json
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages, auth
from .models import UserSettings


# Create your views here.
#--------------------------------------------------------------------------------------------------
# Indev View
#--------------------------------------------------------------------------------------------------
def index(request):
    # Clear Messages
    storage = messages.get_messages(request)
    list(storage)  

    # Get JSON File/Data
    color_settings = []
    file_path = os.path.join(settings.BASE_DIR, "color_settings.json")
    with open(file_path) as json_file:
        data = json.load(json_file)

        for k,v in data.items():
            color_settings.append({"name": k, "value": v})

    exists = UserSettings.objects.filter(user=request.user).exists()
    user_settings = None

    if exists:
        user_settings = UserSettings.objects.get(user=request.user)
    
    # GET
    if request.method == 'GET':
        context = {
            'themes': color_settings,
            'settings': user_settings
        }
        return render(request, 'settings/index.html', context)
    
    # POST
    if request.method == 'POST':
        theme = request.POST['theme']
        if exists:  
            user_settings.theme = theme
            user_settings.save()
        else:
            UserSettings.objects.create(user=request.user, theme=theme)
            
        messages.success(request, theme + ' selected')
        return render(request, 'settings/index.html', {"themes": color_settings})


    

