from django.test import TestCase

from ..forms import FruitForm, SaleForm


class TestFruitForm(TestCase):

    def test_valid(self):
        form_data = {
                        'name': 'リンゴ',
                        'price': 100,
                        'created_at': '2018-12-10 09:18:30.845202',
                        'updated_at': '2018-12-10 09:18:30.845202'
                    }
        form = FruitForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        """
            price(単価)に文字列(数値以外の値)を渡した場合、is_valid()がFalseを返すか検証
        """
        form_data = {
                        'name': 'リンゴ',
                        'price': 'hoge',
                        'created_at': '2018-12-10 09:18:30.845202',
                        'updated_at': '2018-12-10 09:18:30.845202'
                    }
        form = FruitForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestSaleForm(TestCase):
    fixtures = ['test_forms.json']

    def test_valid(self):
        form_data = {
                        'fruit': 1,
                        'amount': 5,
                        'revenue': 500,
                        'sold_at': '2018-12-10 09:18:30.845202'
                    }
        form = SaleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_amount(self):
        """
            amount(個数)に文字列(数値以外の値)を渡した場合、is_valid()がFalseを返すか検証
        """
        form_data = {
                        'fruit': 1,
                        'amount': 'hoge',
                        'revenue': 500,
                        'sold_at': '2018-12-10 09:18:30.845202'
                    }
        form = SaleForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_sold_at(self):
        """
            sold_at(販売日時)に不正な形式の値を渡した場合、is_valid()がFalseを返すか検証
        """
        form_data = {
                        'fruit': 1,
                        'amount': 5,
                        'revenue': 500,
                        'sold_at': '20181210 09:18:30.845202'
                    }
        form = SaleForm(data=form_data)
        self.assertFalse(form.is_valid())
