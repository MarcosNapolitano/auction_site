from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Bid, Product


# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Bid)

class ProductAdmin(admin.ModelAdmin):
    readonly_fields=("pk", "bids")


admin.site.register(Product, ProductAdmin)








