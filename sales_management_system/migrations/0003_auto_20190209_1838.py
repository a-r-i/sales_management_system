# Generated by Django 2.1.5 on 2019-02-09 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales_management_system', '0002_auto_20190208_2003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='price_sum',
            new_name='revenue',
        ),
    ]
