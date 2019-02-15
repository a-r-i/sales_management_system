from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    def __str__(self):
        return self.name


class Sale(models.Model):
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE)
    amount = models.IntegerField()
    revenue = models.IntegerField()  # 合計金額
    sold_at = models.DateTimeField()  # 販売日時

    @property
    def calclate_revenue(self):
        print(self.fruit)
        fruit_obj = Fruit.objects.get(name__exact=self.fruit)
        return fruit_obj.price * self.amount

    def save(self, *args, **kwargs):
        self.revenue = self.calclate_revenue
        super(Sale, self).save(*args, **kwargs)
