from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Bid, Product


# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Bid)
admin.site.register(Product)








