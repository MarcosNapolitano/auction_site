import random

from .models import User, Product, Bid, Comment

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
        exclude = ["user", "watchlist", "is_open", "winner"]

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Broom'}),
            'price': forms.NumberInput(attrs={'placeholder': 'u$D 10.00'}),
            'image': forms.URLInput(attrs={'placeholder': 'Image url'}),
            'description': forms.Textarea(attrs={'placeholder': 'The best broom ever!'})

        }


#code reducer
def query_product(id):
    try:
        return Product.objects.get(pk = id)
    except ObjectDoesNotExist:
        return None


#need a first run to work
def categories_first():
    #query a product that MUST exist just to get the category list
    #maybe create a separate category model?
    product = query_product(2)

    global categories 

    #original list in models is a tuple just need the first element!
    categories = list(map(lambda x: x[0], product.category_choice))
    categories = list(enumerate(categories))
    

def index(request):

    category = {"title" : "Home décor", "id" : 1} #could later be changed
    product_list = Product.objects.filter(is_open = True)
    most_sold   = product_list.filter(category = category["title"])[:5] #only 5 results
    most_recent = product_list.order_by('-created')[:5] #only 5 results
    rand_index = product_list[random.randrange(len(product_list))] #random auction

    context = {"product_list" : product_list, "category" : category,
               "most_sold" : most_sold, "most_recent" : most_recent,
               "rand_index": rand_index, "categories" : categories}
               

    return render(request, "auctions/index.html", context)


def search(request):

    #q is the value and '' default in case None
    to_search = request.GET.get('search','')
    products = Product.objects.filter(title__icontains=to_search)

    #prevents search if empty
    if to_search=="": return index(request)

    length = len(products)

    #if no results you get a message, if just one result, you get the page if 1+ you get the list

    if length<1: return render(request, "auctions/search.html", {"categories" : categories})
    if length==1: return display_item(request, products[0].id)
    if length>1: return render(request, "auctions/search.html", {"products":products, "categories" : categories})


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
                "message": "Invalid username and/or password.", 
                "categories":categories
            })
    else:
        return render(request, "auctions/login.html", {"categories":categories})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = username

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.", 
                "categories":categories
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "categories":categories
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {"categories":categories})


def display_item(request, pk, is_open = True):

    #query current product
    product = query_product(pk)

    #someone commented!
    if request.method == "POST" and request.user.is_authenticated: 

        Comment(product = product, 
                user = request.user, 
                comment = request.POST.get("comment")).save()
        
        return HttpResponseRedirect(reverse("item", kwargs={'pk':pk}))
        

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
            if request.user.is_authenticated and last_bid:

                if request.user.id == last_bid.user.id: last_bid = True
                else: last_bid = False
                
            else: last_bid = False

        except ObjectDoesNotExist:
            bids = False

        #if you are the author of the product
        if request.user.is_authenticated and product.user_id == request.user.id: owner = True
        
        else: owner = False

        #query comments
        comments = Comment.objects.filter(product_id = pk)

        context = {"product"  : product,  "watchlist" : watchlist, "bids"       : bids, 
                   "last_bid" : last_bid, "owner"     : owner,     "open"       : is_open, 
                   "winner"   : winner,   "comments"  : comments,  "categories" : categories}

        return render(request, "auctions/item.html", context)
    
    else: return HttpResponseRedirect(reverse("index"))


def get_categories(request):
    
    categories_first()
    context = {"categories" : categories}
    return render(request, "auctions/categories_hub.html", context)


def category(request, pk):

    category = list(filter(lambda x: x[0] == pk, categories))

    #if not empty, set value to first item's name, else redirect home
    if category: category = category[0][1]
    else: return HttpResponseRedirect(reverse('index'))

    products = Product.objects.filter(category = category)


    if not products: products = None
    context = {"products" : products, "category" : category, "categories" : categories}

    return render(request, "auctions/category.html", context)


# --------------------------------------- LOGIN REQUIRED --------------------------------------- #

@login_required(login_url="login")
def create_auction(request):
    if request.method=="POST": 

        form = new_auction(request.POST)

        if form.is_valid():

            try:
                product = form.save(commit=False)
                product.user = request.user
                product.title.title()
                product.save()

            except IntegrityError:
                return render(request, "auctions/createAuction.html", {"form":form, "error":error, "categories" : categories})
            
            return HttpResponseRedirect(reverse("item", kwargs={'pk':product.id}))

        else:

            return render(request, "auctions/createAuction.html", {"form":form, "categories" : categories})
            
    return render(request, "auctions/createAuction.html", {"form":new_auction() , "categories" : categories})


@login_required(login_url="login")
def watchlist(request):
    

    context = {"products" : Product.objects.filter(watchlist = request.user), 
               "categories" : categories}

    return render(request, "auctions/watchlist.html", context)


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


categories_first()
