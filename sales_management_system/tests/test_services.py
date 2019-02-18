from django.db.models import Sum
from django.test import TestCase

from ..models import Sale
from ..services import aggregate_revenue


class TestAggregateRevenue(TestCase):
    fixtures = ['test_services.json']

    def test_aggregate_revenue(self):
        """
            Pythonのコードで集計した累計売り上げとDjango ORMの集計関数で集計した累計売り上げが同じか検証
        """
        sale_obj_all = Sale.objects.all()

        # Django ORMの集計関数を利用せず、Pythonのコードで集計した累計売り上げ
        total_revenue = aggregate_revenue(sale_obj_all)

        # Django ORMの集計関数で集計した累計売り上げ
        total_revenue_django_orm = Sale.objects.aggregate(Sum('revenue'))['revenue__sum']

        self.assertEqual(total_revenue, total_revenue_django_orm)
