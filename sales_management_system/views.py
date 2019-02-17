from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect

from .forms import LoginForm, FruitForm, SaleForm, SaleImportFromCSVForm
from .models import Fruit, Sale
from .services import aggregate_sales_information, aggregate_revenue


class Login(LoginView):
    form_class = LoginForm
    template_name = 'sales_management_system/login.html'


class TopView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'sales_management_system/index.html'


class FruitListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Fruit
    queryset = Fruit.objects.order_by('-updated_at')


class FruitCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Fruit
    form_class = FruitForm
    template_name = 'sales_management_system/fruit_form.html'
    success_url = '/fruit-list/'


class FruitUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Fruit
    form_class = FruitForm
    template_name = 'sales_management_system/fruit_form.html'
    success_url = '/fruit-list/'


class FruitDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        fruit = Fruit.objects.get(id=pk)
        fruit.delete()
        return redirect('fruit_list')


class SaleManagementView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Sale
    form_class = SaleImportFromCSVForm
    template_name = 'sales_management_system/sale_management.html'
    success_url = '/sale-management/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale_objects_order_by_sold_at = Sale.objects.order_by('-sold_at')
        context['sale_objects'] = sale_objects_order_by_sold_at
        return context

    def form_valid(self, form):
        form.save()
        return redirect('/sale-management/')


class SaleCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Sale
    form_class = SaleForm
    template_name = 'sales_management_system/sale_form.html'
    success_url = '/sale-management/'


class SaleUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Sale
    form_class = SaleForm
    template_name = 'sales_management_system/sale_form.html'
    success_url = '/sale-management/'


class SaleDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        sale = Sale.objects.get(id=pk)
        sale.delete()
        return redirect('sale_management')


class SaleStatisticsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'sales_management_system/sale_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale_objects_all = Sale.objects.all()
        context['total_revenue'] = aggregate_revenue(sale_objects_all)
        context['last3months_sales_information'] = aggregate_sales_information('month', 3)
        context['last3days_sales_information'] = aggregate_sales_information('day', 3)
        return context
