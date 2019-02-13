from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
import pytz

from .models import Sale


def aggregate_sales_information(date_type, number):
    sales_information = []

    now = datetime.now(pytz.timezone('Asia/Tokyo'))
    today = now.date()

    for i in range(1, number + 1):
        if date_type == 'month':
            today_aggregate_month = today + relativedelta(months=-i)
            first_day_aggregate_month = today_aggregate_month.replace(day=1)
            last_day_aggregate_month = first_day_aggregate_month + relativedelta(months=1, days=-1)
            aggregate_date = '%i年%i月' % (first_day_aggregate_month.year, first_day_aggregate_month.month)
            sale_objects = Sale.objects.filter(sold_at__range=[first_day_aggregate_month, last_day_aggregate_month])
            revenue = aggregate_revenue(sale_objects)
            detail = aggregate_detail(sale_objects)
            sales_information.append({'date': aggregate_date, 'revenue': revenue, 'detail': detail})
        elif date_type == 'day':
            aggregate_date = today + timedelta(days=-i)
            sale_objects = Sale.objects.filter(sold_at__date=aggregate_date)
            revenue = aggregate_revenue(sale_objects)
            detail = aggregate_detail(sale_objects)
            sales_information.append({'date': aggregate_date, 'revenue': revenue, 'detail': detail})

    return sales_information


def aggregate_revenue(sale_objects):
    total_revenue = 0

    for obj in sale_objects:
        total_revenue += obj.revenue

    return total_revenue


def aggregate_detail(sales_objects):
    daily_detail_dict = {}

    for obj in sales_objects:
        fruit_name = str(obj.fruit)
        if fruit_name in daily_detail_dict.keys():
            daily_detail_dict[fruit_name]['revenue'] += obj.revenue
            daily_detail_dict[fruit_name]['amount'] += obj.amount
        else:
            daily_detail_dict[fruit_name] = {}
            daily_detail_dict[fruit_name]['revenue'] = obj.revenue
            daily_detail_dict[fruit_name]['amount'] = obj.amount

    daily_detail = ''

    for key, value in daily_detail_dict.items():
        daily_detail += '%s:%i円(%i)' % (key, value['revenue'], value['amount'])

    return daily_detail
