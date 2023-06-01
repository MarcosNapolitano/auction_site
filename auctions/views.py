from .models import User, Product, Bid

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from django.db.models import Max
from django.forms import ModelForm
from django import forms
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


class new_auction(ModelForm):

    class Meta:
        model = Product
        exclude = ["user", "watchlist"]

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Broom'}),
            'description': forms.Textarea(attrs={'placeholder': 'The best broom ever!', 'style':'width:300px'}),
            'price': forms.NumberInput(attrs={'placeholder': 'u$D 10.00'}),
            'image': forms.URLInput(attrs={'placeholder': 'Image url'})
        }


#code reducer
def query_product(id):
    try:
        return Product.objects.get(pk = id)
    except ObjectDoesNotExist:
        return None

def query_product(id):
    try:
        return Product.objects.get(pk = id)
    except ObjectDoesNotExist:
        return None
        

def index(request):

    context = {"product_list" : Product.objects.all()}

    return render(request, "auctions/index.html", context)


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
            
            return HttpResponseRedirect(reverse("item", kwargs={'pk':product.id}))

        else:

            return render(request, "auctions/createAuction.html", {"form":form})
            
    return render(request, "auctions/createAuction.html", {"form":new_auction()})


def display_item(request, pk, is_open = True):

    #query current product
    product = query_product(pk)

    if product : 

        #query if still open and search for winner in that case
        if not product.is_open: 
            is_open = False
            winner = product.winner.username
        else:
            winner = None
    
        #query if user has the current item on watchlist
        try:
            watchlist = Product.objects.filter(watchlist=request.user.id).get(pk=pk)

        except ObjectDoesNotExist:
            watchlist = False

        #query if any bid was placed on the current item
        try:
            bids = Bid.objects.filter(product=pk)
            last_bid = bids.order_by('-created').first() #prevents error if NONE!

            #only if authenticated
            if request.user.is_authenticated:

                if request.user.id == last_bid.user.id: last_bid = True
                else: last_bid = False
                
            else: last_bid = False

        except ObjectDoesNotExist:
            bids = False

        #if you are the author of the product
        if request.user.is_authenticated and product.user_id == request.user.id: owner = True

        
        
        else: owner = False

        context = {"product":product, "watchlist" : watchlist, "bids" : bids, 
                "last_bid" : last_bid, "owner" : owner, "open" : is_open, "winner":winner}

        return render(request, "auctions/item.html", context)
    
    else: return HttpResponseRedirect(reverse("index"))


@login_required(login_url="login")
def add_to_watchlist(request, pk):

    product = query_product(pk)

    if product : product.watchlist.add(request.user)
        
    else: return HttpResponseRedirect(reverse("index"))
    
    return HttpResponseRedirect(reverse("item", kwargs={'pk':pk}))


@login_required(login_url="login")
def remove_from_watchlist(request, pk):

    product = query_product(pk)

    if product : product.watchlist.remove(request.user)
        
    else: return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("item", kwargs={'pk':pk}))


@login_required(login_url="login")
def bid(request, pk):

    product = query_product(pk)

    if product : 

        price = float(request.GET.get('price',''))
        
        if price>product.price:
            bid = Bid(user = request.user, product = product, bid = price)
            bid.save()
            product.price = price
            product.save()

        return HttpResponseRedirect(reverse("item", kwargs={'pk':pk}))
    
    else: return HttpResponseRedirect(reverse("index"))


@login_required(login_url="login")
def close(request, pk):

    product = query_product(pk)

    if product :

        if request.user.is_authenticated and product.user_id == request.user.id: 

            product.is_open = False

            #find bids if any
            bids = Bid.objects.filter(product=pk).order_by('-created').first()

            if bids: 

                try: product.winner = User.objects.get(pk = bids.user_id)
                
                #if user was deleted
                except ObjectDoesNotExist: product.winner = None

            product.save()
            
            return display_item(request, pk, is_open = False)

    else: return HttpResponseRedirect(reverse("index"))

    
