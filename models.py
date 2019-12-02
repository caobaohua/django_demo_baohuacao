from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=50)

class Source(models.Model):
    name = models.CharField(max_length=100)

class RevenueRecord(models.Model):
    date = models.DateField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    clicks = models.IntegerField()
    revenue = models.FloatField()
