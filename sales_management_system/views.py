from datetime import datetime, timedelta

from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.views import View

import pytz

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


class SaleDeleteView(View):

    def get(self, request, pk):
        sale = Sale.objects.get(id=pk)
        sale.delete()
        return redirect('sale_list')


class SaleStatisticsView(TemplateView):

    template_name = "sales_management_system/sale_statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale_objects_all = Sale.objects.all()
        context['total_revenue'] = self.aggregate_revenue(sale_objects_all)
        context['last3months_sales'] = self.aggregate_last3months_sales()
        context['last3days_sales'] = self.aggregate_last3days_sales()
        return context

    def aggregate_revenue(self, sale_objects):
        total_revenue = 0

        for sale_object in sale_objects:
            total_revenue += sale_object.revenue

        return total_revenue

    # のちのち仕様が変わったときのために、「3」という定数を使わないほうがいい？集計する月数・日数を引数で与えるよう変えるべきか
    def aggregate_last3months_sales(self):
        last3months_sales = [{'date': '2019/1', 'revenue': 100, 'detail': 'hoge'}]
        return last3months_sales

    def aggregate_last3days_sales(self):
        last3days_sales = []

        now = datetime.now(pytz.timezone('Asia/Tokyo'))
        today = now.date()

        for i in range(1, 4):
            target_day = today + timedelta(days=-i)

            sale_objects_of_target_day = Sale.objects.filter(sold_at__date=target_day)

            daily_revenue = self.aggregate_revenue(sale_objects_of_target_day)
            daily_detail = self.aggregate_daily_detail(sale_objects_of_target_day)

            last3days_sales.append({'date': target_day, 'revenue': daily_revenue, 'detail': daily_detail})

        return last3days_sales

    def aggregate_daily_detail(self, sales_objects_of_target_day):
        daily_detail_dict = {}

        for object in sales_objects_of_target_day:
            fruit_name = str(object.fruit)
            if fruit_name in daily_detail_dict.keys():
                daily_detail_dict[fruit_name]['revenue'] += object.revenue
                daily_detail_dict[fruit_name]['amount'] += object.amount
            else:
                daily_detail_dict[fruit_name] = {}
                daily_detail_dict[fruit_name]['revenue'] = object.revenue
                daily_detail_dict[fruit_name]['amount'] = object.amount

        daily_detail = ''

        for key, value in daily_detail_dict.items():
            daily_detail += '%s:%i円(%i)' % (key, value['revenue'], value['amount'])

        return daily_detail
