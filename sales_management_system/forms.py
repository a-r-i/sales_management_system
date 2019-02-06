from django import forms
from django.forms import ModelForm

from .models import Fruit, Sale


class FruitForm(ModelForm):

    class Meta:
        model = Fruit
        fields = ('name', 'price',)


def total_fruits_names():
    fruits_names = []

    fruits = Fruit.objects.all()

    for fruit in fruits:
        fruits_names.append([fruit.name, fruit.name])

    return fruits_names


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ('fruit_name', 'amount', 'sold_at')
        FRUIT_NAME_CHOICES = total_fruits_names()
        widgets = {
            'fruit_name': forms.Select(choices=FRUIT_NAME_CHOICES, attrs={'class': 'form-control'}),
        }
