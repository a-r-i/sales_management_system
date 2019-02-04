from django.views.generic import ListView

from .models import Fruit


class FruitListView(ListView):

    model = Fruit
    queryset = Fruit.objects.order_by('-updated_at')