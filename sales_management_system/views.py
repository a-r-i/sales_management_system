from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import FruitForm
from .models import Fruit


class FruitListView(ListView):

    model = Fruit
    queryset = Fruit.objects.order_by('-updated_at')


class FruitCreateView(CreateView):

    model = Fruit
    form_class = FruitForm
    template_name = "sales_management_system/fruit_form.html"
    success_url = "/create-fruit"


class FruitUpdateView(UpdateView):

    model = Fruit
    fields = ("name", "price",)
