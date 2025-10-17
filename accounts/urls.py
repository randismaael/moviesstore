from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.signup, name="accounts.signup"),
    path("login/", views.login, name="accounts.login"),
    path("logout/", views.logout, name="accounts.logout"),
    path("orders/", views.orders, name="accounts.orders"),
    path(
        "movie_request/add/", views.add_movie_request, name="accounts.add_movie_request"
    ),
    path("movie_request/my/", views.my_requests, name="accounts.my_requests"),
    path("movie_request/<int:pk>/delete/", views.delete_request, name="delete_request"),
    path("profile/", views.profile, name="accounts.profile"),
]
