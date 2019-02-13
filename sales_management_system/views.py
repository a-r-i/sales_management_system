from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect

from .forms import LoginForm, FruitForm, SaleForm, SaleImportFromCSVForm
from .models import Fruit, Sale
from .services import aggregate_sales_infomation, aggregate_revenue, aggregate_detail


class Login(LoginView):
    form_class = LoginForm
    template_name = "sales_management_system/login.html"


class TopView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = "sales_management_system/index.html"


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


class SaleFormView(LoginRequiredMixin, FormView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Sale
    form_class = SaleForm
    template_name = 'sales_management_system/sale_form.html'
    success_url = '/sale-management/'

    def form_valid(self, form):
        # SaleFormに実装すべき処理？
        fruit_name = form.cleaned_data['fruit']
        amount = form.cleaned_data['amount']
        revenue = self.calclate_revenue(fruit_name, amount)
        sold_at = form.cleaned_data['sold_at']

        # 新規登録と編集で処理を分ける
        try:
            pk = self.kwargs['pk']
        except KeyError:  # 新規登録
            sale = Sale(fruit=fruit_name, amount=amount, revenue=revenue, sold_at=sold_at)
            sale.save()
        else:  # 編集
            sale = Sale.objects.get(id=pk)
            sale.fruit = fruit_name
            sale.amount = amount
            sale.revenue = revenue
            sale.sold_at = sold_at
            sale.save()

        return super(SaleFormView, self).form_valid(form)

    def calclate_revenue(self, fruit_name, amount):
        fruit = Fruit.objects.get(name__exact=fruit_name)
        revenue = fruit.price * amount
        return revenue


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

    template_name = "sales_management_system/sale_statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale_objects_all = Sale.objects.all()
        context['total_revenue'] = aggregate_revenue(sale_objects_all)
        context['last3months_sales_infomation'] = aggregate_sales_infomation('month', 3)
        context['last3days_sales_infomation'] = aggregate_sales_infomation('day', 3)
        return context
