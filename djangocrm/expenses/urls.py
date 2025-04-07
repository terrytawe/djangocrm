from django.urls import path
from . import views
from .views import ExpenseCreateView

urlpatterns = [
    path('', views.index, name="index"),
    path('expenses', views.expenses, name="expenses"),
    path('add/', ExpenseCreateView.as_view(), name="add_expense" ) 
]
