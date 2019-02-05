from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.views import View

from .forms import FruitForm
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
        sales_count = Sale.objects.filter(fruit_name=fruit.name).count()

        if sales_count != 0:
            fruit.delete()

        return redirect('fruit_list')
