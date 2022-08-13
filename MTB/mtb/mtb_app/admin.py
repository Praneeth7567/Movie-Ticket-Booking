from django.contrib import admin
from .models import Movie, Theater, Show, booked

admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Show)
admin.site.register(booked)
