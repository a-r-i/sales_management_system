import csv
from datetime import datetime
import io

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from django.forms import ModelForm

from .models import Fruit, Sale


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class FruitForm(ModelForm):
    class Meta:
        model = Fruit
        fields = ('name', 'price',)


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ('fruit', 'amount', 'sold_at')


class SaleImportFromCSVForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data['file']
        csv_file = io.TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(csv_file)

        self.sale_array = []

        # 別のメソッドに切り分ける？
        for row in reader:
            try:
                fruit = Fruit.objects.get(name__exact=row[0])
            except Fruit.DoesNotExist:
                print('Fruit.DoesNotExist')
            else:
                amount = int(row[1])
                revenue = int(row[2])
                try:
                    sold_at = datetime.strptime(row[3], '%Y-%m-%d %H:%M')
                except ValueError:
                    print('ValueError')
                else:
                    print(fruit, amount, revenue, sold_at)
                    sale = Sale(
                                fruit=fruit,
                                amount=amount,
                                revenue=revenue,
                                sold_at=sold_at
                                )
                    self.sale_array.append(sale)

    def save(self):
        for sale in self.sale_array:
            try:
                sale.save()
            except ValueError:
                print('ValueError')
