import csv
from datetime import datetime
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

        # 別のメソッドに切り分ける？
        for row in reader:
            try:
                fruit = Fruit.objects.get(name__exact=row[0])
            except Fruit.DoesNotExist:
                print('Fruit.DoesNotExist')
            else:
                amount = row[1]
                revenue = row[2]
                try:
                    sold_at = datetime.strptime(row[3], '%Y-%m-%d %H:%M')
                except ValueError:
                    print('ValueError')
                else:
                    sale = Sale(fruit=fruit, amount=amount, revenue=revenue, sold_at=sold_at)
                    self._instances.append(sale)

    def save(self):
        for sale in self._instances:
            try:
                sale.save()
            except ValueError:
                print('ValueError')


class SaleForm(forms.Form):

    fruit = forms.ModelChoiceField(Fruit.objects)
    amount = forms.IntegerField()
    sold_at = forms.DateTimeField()
