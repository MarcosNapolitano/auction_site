from .models import User, Product

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from django.forms import ModelForm
from django import forms
from django.db import IntegrityError



class new_auction(ModelForm):

    class Meta:
        model = Product
        exclude = ["user"]

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Broom'}),
            'description': forms.Textarea(attrs={'placeholder': 'The best broom ever!', 'style':'width:300px'}),
            'price': forms.NumberInput(attrs={'placeholder': 'u$D 10.00'}),
            'category': forms.TextInput(attrs={'placeholder': 'Misc.'}),
            'image': forms.URLInput(attrs={'placeholder': 'Image url'})
        }
        

def index(request):
    return render(request, "auctions/index.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def create_auction(request):
    if request.method=="POST": 

        form = new_auction(request.POST)

        if form.is_valid():

            try:
                product = form.save(commit=False)
                product.user = request.user
                product.save()

            except IntegrityError:
                return render(request, "auctions/createAuction.html", {"form":form, "error":error})
            
            return render(request, "auctions/item.html", {"form":form})

        else:

            return render(request, "auctions/createAuction.html", {"form":form})
            
    return render(request, "auctions/createAuction.html", {"form":new_auction()})


def display_item(request, pk):

    product = Product.objects.get(pk=pk)
    return render(request, "auctions/item.html", {"product":product})