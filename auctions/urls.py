from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction", views.create_auction, name="new_auction"),
    path("auction/<int:pk>", views.display_item, name="item"),
    path("auction/<int:pk>/add", views.add_to_watchlist, name="add"),
    path("auction/<int:pk>/remove", views.remove_from_watchlist, name="remove"),
    path("auction/<int:pk>/bid", views.bid, name="bid"),
    path("auction/<int:pk>/close", views.close, name="close"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.get_categories, name="categories"),
    path("categories/<int:pk>", views.category, name="category")

    
]
