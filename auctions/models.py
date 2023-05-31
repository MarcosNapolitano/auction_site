from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    watchlist = []
    
    def __str__(self):
        return self.first_name

    def addToWatchlist(self, Product):
        self.watchlist.append(Product)
        return self.watchlist

class Product(models.Model):

    def returnBids(self):
        
        return list(Bid.objects.filter(product = self.pk))

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 30, unique = True)
    description = models.TextField()
    price = models.DecimalField(max_digits = 8, decimal_places = 2)
    created = models.DateField(auto_now_add=True)
    category = models.CharField(max_length = 30, blank=True)
    image = models.URLField(blank=True)
    bids = returnBids


    def __str__(self):
        return self.title

    
class Bid(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits = 8, decimal_places = 2)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Bid {self.pk} on {self.product}"

class Comment(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()


    def __str__(self):
        return f"Comment {self.pk} from user {self.user} on {self.product}"