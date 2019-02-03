from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    def __str__(self):
        return self.name


class Sale(models.Model):
    fruit = models.ForeignKey(Fruit, on_delete=models.PROTECT)
    amount = models.IntegerField()
    total_price = models.IntegerField()  # 合計金額
    sold_at = models.DateTimeField()  # 販売日時
