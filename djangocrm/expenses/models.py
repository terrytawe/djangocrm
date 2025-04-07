from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.

#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category
    
    class Meta:
        ordering: ['-date'] # type: ignore
    
#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
class ExpenseCategory(models.Model): 
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = 'Expense Categories'

    def __str__(self):
        return self.name

#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category
    
    class Meta:
        ordering: ['-date'] # type: ignore

#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
class IncomeCategory(models.Model): 
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = 'Income Categories'

    def __str__(self):
        return self.name