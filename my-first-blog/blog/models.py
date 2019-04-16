from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class needforvideo(models.Model):
    title=models.CharField(max_length=50)
    img=models.FileField( blank=True)
    def __str__(self):
        return self.title

class feedback(models.Model):
    title=models.CharField(max_length=70)
    author = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    text = models.TextField()

class kolvo(models.Model):
    def __str__(self):
        return self.name
    name=models.CharField(max_length=70)


class Type(models.Model):
    def __str__(self):
        return self.name
    name=models.CharField(max_length=70)


class product(models.Model):
    type=models.ForeignKey(Type, on_delete=models.CASCADE)
    title=models.CharField(max_length=70)
    content=models.TextField()
    price=models.IntegerField()
    edinica=models.ForeignKey(kolvo, on_delete=models.CASCADE)
    img=models.FileField( blank=True)

    def __str__(self):
        return self.title