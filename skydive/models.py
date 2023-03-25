from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

SKYDIVE_TYPE = (
    ('tandemskydive', 'Tandem Skydive',),
    ('learnskydive', 'Learn Skydive',),
    ('licenseskydive', 'Licensed Skydive',)
)

CURR_TYPE = (
    ('cad', 'CAD',),
    ('inr', 'INR',),
    ('usa', 'USA',),
)


class Destination(models.Model):
    id = models.IntegerField(primary_key=True)
    province = models.CharField(max_length=20)
    img = models.ImageField(upload_to='pics')
    number = models.IntegerField(default=50)

    def __str__(self):
        return self.province


class Destination_desc(models.Model):
    dest_id = models.AutoField(primary_key=True)
    province = models.CharField(max_length=20)
    price = models.IntegerField(default=2000)
    rating = models.IntegerField(default=5)
    desc = models.TextField()
    img_destin = models.ImageField(upload_to='pics')
    type_skydive = models.CharField(max_length=50, choices=SKYDIVE_TYPE)
    curr = models.CharField(max_length=10, choices=CURR_TYPE, default='cad')

    def __str__(self):
        return self.province + "-" + self.type_skydive
