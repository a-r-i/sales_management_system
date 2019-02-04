from django.forms import ModelForm
from .models import Fruit


class FruitForm(ModelForm):

    class Meta:
        model = Fruit
        fields = ("name", "price",)
