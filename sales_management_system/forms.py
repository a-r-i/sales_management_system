import csv
import io

from django import forms
from django.forms import ModelForm

from .models import Fruit, Sale


class FruitForm(ModelForm):

    class Meta:
        model = Fruit
        fields = ('name', 'price',)


class SaleImportFromCSVForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data['file']
        csv_file = io.TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(csv_file)

        self._instances = []

        for row in reader:
            fruit = Fruit.objects.get(name__exact=row[0])
            amount = row[1]
            revenue = row[2]
            sold_at = row[3]
            sale = Sale(fruit=fruit, amount=amount, revenue=revenue, sold_at=sold_at)
            self._instances.append(sale)

    def save(self):
        for sale in self._instances:
            sale.save()


class SaleForm(forms.Form):

    fruit = forms.ModelChoiceField(Fruit.objects)
    amount = forms.IntegerField()
    sold_at = forms.DateTimeField()
