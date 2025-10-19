from django.urls import path
from . import views

app_name = "mapview"

urlpatterns = [
    path("", views.map_page, name="map_page"),
    path("api/local/", views.local_popularity_data, name="local_popularity_data"),
]