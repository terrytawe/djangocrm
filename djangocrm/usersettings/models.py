from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserSettings(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(User+"'s preferences")
