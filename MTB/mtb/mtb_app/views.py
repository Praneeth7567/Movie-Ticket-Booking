from datetime import date
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from .models import User, Movie, Theater, Show, booked
from django.core.paginator import Paginator
from datetime import datetime

def index(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "mtb_app/index.html", {
        "movies":page_obj
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mtb_app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mtb_app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mtb_app/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "mtb_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mtb_app/register.html")

def profile(request):
    return render(request, "mtb_app/profile.html", {
        "details": User.objects.get(username = request.user.username)
    })

def bookings(request):
    return render(request, "mtb_app/bookings.html", {
        "bookings": booked.objects.filter(user = request.user).order_by('-booked_time')
    })

def theater(request):
    theaters = Theater.objects.all()
    paginator = Paginator(theaters, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "mtb_app/theaters.html", {
        "theaters":page_obj
    })

def bookmovie(request,id):
    if request.method == "POST":
        tickets = request.POST.get('tickets')
        slot = request.POST.get('slot')
        show = Show.objects.get(id = slot)
        if show.seats_avl >= int(tickets):
            show.seats_avl-=int(tickets)
            Show.objects.filter(id = slot).update(seats_avl = show.seats_avl)
            booked.objects.create(user = request.user, show_id = slot, tickets_booked = tickets)
            return render(request, "mtb_app/bookmovie.html", {
                "movie" : Movie.objects.get(id=id),
                "slots": Show.objects.filter(movie_id = id),
                "message": "Tickets successfully booked. Check 'My bookings' for all bookings"
    })
        else:
            return render(request, "mtb_app/bookmovie.html", {
                "movie" : Movie.objects.get(id=id),
                "slots": Show.objects.filter(movie_id = id),
                "message": "Requested ticket count is not avaliable in the requested time-slot"
    })
    return render(request, "mtb_app/bookmovie.html", {
        "movie" : Movie.objects.get(id=id),
        "slots": Show.objects.filter(movie_id = id,date__gte = datetime.now(),seats_avl__gte =0)
    })

    
