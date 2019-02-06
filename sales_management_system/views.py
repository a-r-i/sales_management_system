from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.views import View

from .forms import FruitForm, SaleForm
from .models import Fruit, Sale


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
        sales_count = Sale.objects.filter(fruit_name__exact=fruit.name).count()

        if sales_count != 0:
            fruit.delete()

        return redirect('fruit_list')


class SaleListView(ListView):

    model = Sale
    queryset = Sale.objects.order_by('-sold_at')


class SaleCreateView(CreateView):

    model = Sale
    form_class = SaleForm
    template_name = 'sales_management_system/sale_form.html'
    success_url = '/sale-list'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.total_price = self.culc_total_price(instance.fruit_name, instance.amount)
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
