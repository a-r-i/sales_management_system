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


class SaleFormView(FormView):

    model = Sale
    form_class = SaleForm
    template_name = 'sales_management_system/sale_form.html'
    success_url = '/sale-list'

    def form_valid(self, form):
        fruit_name = form.cleaned_data['fruit']
        amount = form.cleaned_data['amount']
        price_sum = self.culc_price_sum(fruit_name, amount)
        sold_at = form.cleaned_data['sold_at']

        # 新規登録と編集で処理を分ける
        try:
            pk = self.kwargs['pk']
        except KeyError:  # 新規登録
            sale = Sale(fruit=fruit_name, amount=amount, total_price=price_sum, sold_at=sold_at)
            sale.save()
        else:  # 編集
            sale = Sale.objects.get(id=pk)
            sale.fruit = fruit_name
            sale.amount = amount
            sale.total_price = price_sum
            sale.sold_at = sold_at
            sale.save()

        return super(SaleFormView, self).form_valid(form)

    def culc_price_sum(self, fruit_name, amount):
        fruit = Fruit.objects.get(name__exact=fruit_name)
        price_sum = fruit.price * amount
        return price_sum


class SaleDeleteView(View):

    def get(self, request, pk):
        sale = Sale.objects.get(id=pk)
        sale.delete()
        return redirect('sale_list')


class SaleStatisticsView(TemplateView):

    template_name = "sales_management_system/sale_statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['revenue_sum'] = self.culc_revenue_sum()
        context['last3months_sales_data'] = self.total_last3months_sales()
        return context

    def culc_revenue_sum(self):
        revenue_sum = 0

        sale_objects_all = Sale.objects.all()

        for sale_object in sale_objects_all:
            revenue_sum += sale_object.total_price

        return revenue_sum

    def total_last3months_sales(self):
        last3months_sales_data = [{'date': '2019/1', 'revenue': 100, 'detail': 'hoge'}]
        return last3months_sales_data