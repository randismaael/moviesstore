from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="movies.index"),
    path("<int:id>/", views.show, name="movies.show"),
    path("<int:id>/rate/", views.rate_movie, name="movies.rate"),
    path("<int:id>/reviews/create/", views.create_review, name="movies.create_review"),
    path(
        "<int:id>/reviews/<int:review_id>/edit/",
        views.edit_review,
        name="movies.edit_review",
    ),
    path(
        "<int:id>/reviews/<int:review_id>/delete/",
        views.delete_review,
        name="movies.delete_review",
    ),
]
