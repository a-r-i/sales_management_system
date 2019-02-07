from django import forms
from django.forms import ModelForm

from .models import Fruit, Sale


class FruitForm(ModelForm):

    class Meta:
        model = Fruit
        fields = ('name', 'price',)


class SaleForm(forms.Form):

    fruit = forms.ModelChoiceField(Fruit.objects)
    amount = forms.IntegerField()
    sold_at = forms.DateTimeField()
