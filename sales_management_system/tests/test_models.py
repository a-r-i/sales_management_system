from django.test import TestCase

from ..models import Fruit, Sale


class TestSale(TestCase):
    fixtures = ['test_models.json']
    
    def update_fruit_price_not_change_revenue(self):
        """
            販売情報の売り上げは、販売情報登録後に果物の単価が変更されても、金額が変更されずそのままであるか検証
        """
        sale = Sale.objects.get(id=1)

        # 果物単価変更前の売り上げ
        before_revenue = sale.revenue

        # 果物の単価を変更
        fruit = Fruit.objects.get(id=sale.fruit.id)
        before_fruit_price = fruit.price
        print(before_fruit_price)
        fruit.price = before_fruit_price + 1
        fruit.save()
        
        sale.refresh_from_db()

        # 果物単価変更後の売り上げ
        after_revenue = sale.revenue
        
        self.assertEqual(before_revenue, after_revenue)
