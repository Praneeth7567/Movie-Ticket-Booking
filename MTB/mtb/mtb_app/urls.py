from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("bookings", views.bookings, name="bookings"),
    path("theaters", views.theater, name="theaters"),
    path("bookmovie/<int:id>", views.bookmovie, name="bookmovie"),
    path("result", views.search, name="result"),
    path("search", views.search_page, name="search"),
    
]