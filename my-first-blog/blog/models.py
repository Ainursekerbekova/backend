from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User

class needforvideo(models.Model):
    title=models.CharField(max_length=50)
    img=models.FileField( blank=True)
    #is_using_now=models.BooleanField(default=False)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name="видео для главной страницы"
        verbose_name_plural="Видео"

class feedback(models.Model):
    author = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    text = models.TextField()
    def get_absolute_url(self):
        return reverse('index')
    def __str__(self):
        return self.text

    class Meta:
        verbose_name="отзыв"
        verbose_name_plural="Отзывы"

class kolvo(models.Model):
    def __str__(self):
        return self.name
    name=models.CharField(max_length=70)

class Type(models.Model):
    name=models.CharField(max_length=70)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name="группу продуктов"
        verbose_name_plural="Группы продуктов"


class product(models.Model):
    type=models.ForeignKey(Type, on_delete=models.CASCADE)
    title=models.CharField(max_length=70)
    content=models.TextField()
    price=models.IntegerField()
    edinica=models.ForeignKey(kolvo, on_delete=models.CASCADE)
    img=models.FileField( blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name="продукт"
        verbose_name_plural="Продукты"



class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user.username+' '+str(self.order_date)
    def get_sum(self):
        items=OrderItem.objects.filter(order=self.id)
        sum=0
        for item in items:
            sum+=item.get_sum()
        return sum

    class Meta:
        verbose_name="Заказ"
        verbose_name_plural="Заказы"

class OrderItem(models.Model):
    prod=models.ForeignKey(product, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    order=models.ForeignKey(Order, on_delete=models.CASCADE,default=None)
    def __str__(self):
        return self.prod.title+'  '+str(self.quantity)
    def get_sum(self):
        return self.prod.price*self.quantity
    class Meta:
        verbose_name="Единица заказа"
        verbose_name_plural="Единицы заказов"













