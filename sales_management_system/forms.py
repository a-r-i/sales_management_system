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
                    sale = Sale(
                                fruit=fruit,
                                amount=amount,
                                revenue=revenue,
                                sold_at=sold_at
                                )
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
    
    def clean(self):
        self.fruit_name = self.cleaned_data['fruit']
        self.amount = self.cleaned_data['amount']
        self.revenue = self.calclate_revenue(self.fruit_name, self.amount)
        self.sold_at = self.cleaned_data['sold_at']

    def calclate_revenue(self, fruit_name, amount):
        fruit = Fruit.objects.get(name__exact=fruit_name)
        revenue = fruit.price * amount
        return revenue

    def save(self, pk):
        # 新規登録と編集で処理を分ける
        if pk:  # 編集
            sale = Sale.objects.get(id=pk)
            sale.fruit = self.fruit_name
            sale.amount = self.amount
            sale.revenue = self.revenue
            sale.sold_at = self.sold_at
            sale.save()
        else:  # 新規登録
            sale = Sale(
                        fruit=self.fruit_name,
                        amount=self.amount,
                        revenue=self.revenue,
                        sold_at=self.sold_at
                        )
            sale.save()
