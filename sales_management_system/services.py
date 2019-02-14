from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
import pytz

from .models import Sale


def aggregate_revenue(sale_objects):
    total_revenue = 0

    for obj in sale_objects:
        total_revenue += obj.revenue

    return total_revenue


def aggregate_sales_information(date_type, number):
    sales_information = []

    now = datetime.now(pytz.timezone('Asia/Tokyo'))
    today = now.date()

    for i in range(1, number + 1):
        if date_type == 'month':
            this_day_aggregate_month = today + relativedelta(months=-i)  # 統計を取る月の今日
            first_day_aggregate_month = this_day_aggregate_month.replace(day=1)  # 統計を取る月の1日
            last_day_aggregate_month = first_day_aggregate_month + relativedelta(months=1, days=-1)  # 統計を取る月の最終日

            sale_objects_aggregate_month = Sale.objects.filter(sold_at__range=[
                                                                               first_day_aggregate_month,
                                                                               last_day_aggregate_month
                                                                               ])

            aggregate_date = '%i年%i月' % (this_day_aggregate_month.year, this_day_aggregate_month.month)  # 統計を取る年月
            revenue = aggregate_revenue(sale_objects_aggregate_month)
            detail = aggregate_detail(sale_objects_aggregate_month)

            sales_information.append({'date': aggregate_date, 'revenue': revenue, 'detail': detail})
        elif date_type == 'day':
            aggregate_date = today + timedelta(days=-i)  # 統計を取る年月日

            sale_objects_aggregate_date = Sale.objects.filter(sold_at__date=aggregate_date)

            revenue = aggregate_revenue(sale_objects_aggregate_date)
            detail = aggregate_detail(sale_objects_aggregate_date)

            sales_information.append({'date': aggregate_date, 'revenue': revenue, 'detail': detail})

    return sales_information


def aggregate_detail(sale_objects):
    detail_dict = {}

    # 「同じ果物の販売情報」をひとつに合算し、以下の形式の二次元辞書をつくる
    # {'ブルーベリー': {'revenue': 200, 'amount': 4}, 'メロン': {'revenue': 20200, 'amount': 8}}
    for obj in sale_objects:
        fruit_name = str(obj.fruit)
        if fruit_name in detail_dict.keys():
            detail_dict[fruit_name]['revenue'] += obj.revenue
            detail_dict[fruit_name]['amount'] += obj.amount
        else:
            detail_dict[fruit_name] = {}
            detail_dict[fruit_name]['revenue'] = obj.revenue
            detail_dict[fruit_name]['amount'] = obj.amount

    detail = ''

    for key, value in detail_dict.items():
        detail += '%s:%i円(%i)' % (key, value['revenue'], value['amount'])

    return detail