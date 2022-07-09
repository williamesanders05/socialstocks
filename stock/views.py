from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from html2text import re
import requests
import datetime
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import null

from .models import *

key = open('apikey.txt').read()
ts = TimeSeries(key, output_format='pandas', indexing_type='integer')

# Create your views here.
def index(request):
    owns = Owned.objects.filter(owner = request.user.username)
    for own in owns:
        data, meta = ts.get_intraday(symbol = own.symbol, interval = '5min', outputsize='full')
        datas = float(data['1. open'][0])
        totaldatas = datas * own.shares
        own.currentprice = totaldatas
        own.save()
    return render(request, "stock/index.html", {
        'owns': owns,
    })

def create(request):
    if request.method == "POST":
        owned = Owned(
            owner = request.user.username,
            symbol = request.POST['symbol'],
            pricebought = request.POST['pricebought'],
            shares = request.POST['shares'],
            totalprice = float(request.POST['pricebought']) * float(request.POST['shares'])
        )
        owned.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, "stock/create.html")

def search(request):
    if request.method == "POST":
        data, meta = ts.get_intraday(symbol=request.POST['symbol'], interval = '5min', outputsize='full')
        return render(request, "stock/search.html", {
            'data': data['1. open'][0],
            'symbol': request.POST['symbol']
        })
    null

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