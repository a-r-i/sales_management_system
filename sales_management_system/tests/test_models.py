from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Fruit, Sale


class TestFruit(TestCase):
    fixtures = ['test_models.json']

    def test_delete_fruit(self):
        """
            削除リンクを押すと、対象の果物は削除されることを検証
        """
        self.client.force_login(User.objects.create_user('testuser'))

        pk = 1

        # 事前状態の検証
        fruit_count = Fruit.objects.filter(pk=pk).count()
        self.assertEqual(fruit_count, 1)

        self.client.get('/delete-fruit/%i/' % pk)

        # 事後状態の検証
        fruit_count = Fruit.objects.filter(pk=pk).count()
        self.assertEqual(fruit_count, 0)


class TestSale(TestCase):
    fixtures = ['test_models.json']

    def test_delete_sale(self):
        """
            削除リンクを押すと、対象の果物は削除されることを検証
        """
        self.client.force_login(User.objects.create_user('testuser'))

        pk = 1

        # 事前状態の検証
        sale_count = Sale.objects.filter(pk=pk).count()
        self.assertEqual(sale_count, 1)

        self.client.get('/delete-sale/%i/' % pk)

        # 事後状態の検証
        sale_count = Sale.objects.filter(pk=pk).count()
        self.assertEqual(sale_count, 0)
