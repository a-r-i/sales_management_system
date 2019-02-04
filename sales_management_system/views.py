from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import FruitForm
from .models import Fruit


class FruitListView(ListView):

    model = Fruit
    queryset = Fruit.objects.order_by('-updated_at')


class FruitCreateView(CreateView):

    model = Fruit
    form_class = FruitForm
    template_name = "sales_management_system/fruit_form.html"
    success_url = "/fruit-list"


class FruitUpdateView(UpdateView):

    model = Fruit
    form_class = FruitForm
    template_name = "sales_management_system/fruit_form.html"
    success_url = "/fruit-list"


class FruitDeleteView(DeleteView):

    model = Fruit
    template_name = "sales_management_system/fruit_confirm_delete.html"
    success_url = "/fruit-list"