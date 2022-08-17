from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass

class Movie(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    cast = models.CharField(max_length=512)
    cnr = models.CharField(max_length=2,choices=[
        ('U','U'),
        ('UA','UA'),
        ('A','A')
    ],default="A")
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

class Theater(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=512)
    city = models.CharField(max_length=64)
    capacity = models.IntegerField(default=60)

    def __str__(self):
        return f'{self.name}, {self.city}'

class Show(models.Model):
    timeslot = models.CharField(max_length = 12,choices=[
        ("09:00-12:00","09:00-12:00"),
        ("12:30-15:30","12:30-15:30"),
        ("16:00-19:00","16:00-19:00")
    ])
    movie = models.ForeignKey(Movie, on_delete=CASCADE)
    theater = models.ForeignKey(Theater, on_delete=CASCADE)
    date = models.DateField()
    seats_avl = models.IntegerField()

    def __str__(self):
        return f'{self.theater}:{self.date}, {self.timeslot}'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    show = models.ForeignKey(Show, on_delete=CASCADE)
    tickets_booked = models.IntegerField()
    booked_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tickets_booked} - {self.show}: {self.booked_time}'