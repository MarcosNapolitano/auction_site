from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return self.first_name


class Product(models.Model):

    #categories
    category_choice = [
        ("Fashion & Apparel", "Fashion & Apparel"),
        ("Home décor & Maintenance" , "Home décor & Maintenance"),
        ("Beauty & Personal Care" , "Beauty & Personal Care"),
        ("Eco-friendly & Natural products" , "Eco-friendly & Natural products"),
        ("Healthcare & Fitness" , "Healthcare & Fitness"),
        ("Pet products" , "Pet products")
    ]

    #this will get the deleted user so winner data won't get lost
    def get_user():
        return User.objects.get_or_create(username="deleted")[0]


    #needs a related_name to prevent clashing with the many to many field
    user        = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "author") 
    title       = models.CharField(max_length = 30, unique = True)
    price       = models.DecimalField(max_digits = 8, decimal_places = 2)
    created     = models.DateField(auto_now_add = True)
    updated     = models.DateTimeField(auto_now = True)
    category    = models.CharField(max_length = 35, blank = True, choices = category_choice)
    image       = models.URLField(blank=True)
    watchlist   = models.ManyToManyField(User, blank = True)
    is_open     = models.BooleanField(default = True)
    winner      = models.ForeignKey(User, default = None, null = True, blank = True, 
                                          on_delete = models.SET(get_user), related_name = "winner")
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_winner(self):
        return self.winner.id

    class Meta:
        ordering = ["-updated"]

    
class Bid(models.Model):

    user    = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    bid     = models.DecimalField(max_digits = 8, decimal_places = 2)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Bid {self.pk} on {self.product}"

class Comment(models.Model):

    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user    = models.ForeignKey(User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    comment = models.TextField()


    def __str__(self):
        return f"Comment {self.pk} from user {self.user} on {self.product}"