from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from .models import ExpenseCategory, Expense, Income, IncomeCategory
from .forms import ExpenseForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View


#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
def index(request):
    return render(request, 'expenses/index.html')

#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
@login_required(login_url='/authentication/login')
def expenses(request):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "expenses/expenses.html")

#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/add_expense.html'
    success_url = reverse_lazy('expenses')
    login_url = '/authentication/login'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Expense saved successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        # import pdb; pdb.set_trace()
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expensecategories'] = ExpenseCategory.objects.all()
        return context
        

