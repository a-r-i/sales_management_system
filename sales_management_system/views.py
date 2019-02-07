from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.views import View

from .forms import FruitForm, SaleForm
from .models import Fruit, Sale


class TopView(TemplateView):

    template_name = "sales_management_system/index.html"


class FruitListView(ListView):

    model = Fruit
    queryset = Fruit.objects.order_by('-updated_at')


class FruitCreateView(CreateView):

    model = Fruit
    form_class = FruitForm
    template_name = 'sales_management_system/fruit_form.html'
    success_url = '/fruit-list'


class FruitUpdateView(UpdateView):

    model = Fruit
    form_class = FruitForm
    template_name = 'sales_management_system/fruit_form.html'
    success_url = '/fruit-list'


class FruitDeleteView(View):

    def get(self, request, pk):
        fruit = Fruit.objects.get(id=pk)
        fruit.delete()
        return redirect('fruit_list')


class SaleListView(ListView):

    model = Sale
    queryset = Sale.objects.order_by('-sold_at')


class SaleCreateView(FormView):

    model = Sale
    form_class = SaleForm
    template_name = 'sales_management_system/sale_form.html'
    success_url = '/sale-list'

    def form_valid(self, form):
        fruit_name = form.cleaned_data['fruit']
        amount = form.cleaned_data['amount']
        total_price = self.culc_total_price(fruit_name, amount)
        sold_at = form.cleaned_data['sold_at']
        sale = Sale(fruit=fruit_name, amount=amount, total_price=total_price, sold_at=sold_at)
        sale.save()
        return super(SaleCreateView, self).form_valid(form)

    def culc_total_price(self, fruit_name, amount):
        fruit = Fruit.objects.get(name__exact=fruit_name)
        total_price = fruit.price * amount
        return total_price


class SaleUpdateView(UpdateView):

    model = Sale
    form_class = SaleForm
    template_name = 'sales_management_system/sale_form.html'
    success_url = '/sale-list'


class SaleDeleteView(View):

    def get(self, request, pk):
        sale = Sale.objects.get(id=pk)
        sale.delete()
        return redirect('sale_list')


class SaleStatisticsView(TemplateView):

    template_name = "sales_management_system/sale_statistics.html"
