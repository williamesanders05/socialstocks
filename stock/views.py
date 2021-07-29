from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import requests
import datetime

from .models import *

# Create your views here.
def index(request):
    predictions = Predictions.objects.all()
    return render(request, "stock/index.html", {
        'predictions': predictions
    })

def create(request):
    if request.method == "POST":
        prediction = Predictions(
            owner = request.user.username,
            symbol = request.POST['symbol'],
            predictedprice = request.POST['predictedprice'],
            predictedtime = request.POST['predictedtime'],
        )
        prediction.save()
        return HttpResponseRedirect(reverse('index'))
    currentdate = datetime.date.today
    return render(request, "stock/create.html", {
        'date': currentdate
    })

def closed():
    predictions = Predictions.objects.filter(closed = False)
    for prediction in predictions:
        today = datetime.date.now
        if today == prediction.predictedtime:
            prediction.update(closed = True)
            symbol = prediction.symbol
            url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=ZAW10ODA2OT1H0A8' % (symbol)
            r = requests.get(url)
            data = r.json()
            price = (data['Global Quote']['05. price'])
            if symbol >= price:
                users = User.objects.filter(username = prediction.owner)
                for user in users:
                    reputation = user.reputaion + 10
                    user.objects.update(reputation = reputation)
            else:
                users = User.objects.filter(username = prediction.owner)
                for user in users:
                    reputation = user.reputaion - 10
                    user.objects.update(reputation = reputation)
            prediction.objects.update(closed = True)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "stock/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "stock/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "stock/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "stock/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "stock/register.html")