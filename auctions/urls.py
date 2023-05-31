from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction", views.create_auction, name="new_auction"),
    path("auction/<int:pk>", views.display_item, name="item")
    
]
