from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control


def index(request):
    return render(request, 'expenses/index.html')

@login_required(login_url='/authentication/login')
def expenses(request):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "expenses/expenses.html")

@login_required(login_url='authentication/login')
def add_expense(request):
    return render(request, "expenses/add_expense.html")
