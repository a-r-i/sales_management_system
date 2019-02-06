from django.forms import ModelForm
from .models import Fruit, Sale


class FruitForm(ModelForm):

    class Meta:
        model = Fruit
        fields = ('name', 'price',)


class SaleForm(ModelForm):

    class Meta:
        model = Sale
        fields = ('fruit_name', 'amount', 'sold_at')
