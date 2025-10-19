from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Movie, Review, Rating
from .forms import RatingForm


def index(request):
    search_term = request.GET.get("search")
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {
        "title": "Movies",
        "movies": movies,
    }
    return render(request, "movies/index.html", {"template_data": template_data})


def show(request, id):
    movie = get_object_or_404(Movie.objects.prefetch_related("ratings"), id=id)
    reviews = Review.objects.filter(movie=movie).select_related("user")

    # ratings context
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, movie=movie).first()

    template_data = {
        "title": movie.name,
        "movie": movie,
        "reviews": reviews,
        "avg_rating": movie.average_rating,
        "ratings_count": movie.ratings_count,
        "user_rating": user_rating,
        "rating_form": RatingForm(
            initial={"value": getattr(user_rating, "value", None)}
        ),
    }
    return render(request, "movies/show.html", {"template_data": template_data})


@login_required
def rate_movie(request, id):
    """Create or update the logged-in user's rating for this movie, then return to detail."""
    movie = get_object_or_404(Movie, id=id)
    if request.method != "POST":
        return redirect("movies.show", id=id)

    form = RatingForm(request.POST)
    if form.is_valid():
        value = form.cleaned_data["value"]
        Rating.objects.update_or_create(
            user=request.user, movie=movie, defaults={"value": value}
        )
        messages.success(request, f"Your rating of {value}★ has been saved.")
    else:
        messages.error(request, "Invalid rating.")
    return redirect("movies.show", id=id)


@login_required
def create_review(request, id):
    if request.method == "POST" and request.POST.get("comment", "").strip():
        movie = get_object_or_404(Movie, id=id)
        Review.objects.create(
            comment=request.POST["comment"],
            movie=movie,
            user=request.user,
        )
        return redirect("movies.show", id=id)
    else:
        return redirect("movies.show", id=id)


@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        return redirect("movies.show", id=id)

    if request.method == "GET":
        template_data = {
            "title": "Edit Review",
            "review": review,
        }
        return render(
            request, "movies/edit_review.html", {"template_data": template_data}
        )

    elif request.method == "POST" and request.POST.get("comment", "").strip():
        review.comment = request.POST["comment"]
        review.save()
        return redirect("movies.show", id=id)

    else:
        return redirect("movies.show", id=id)


@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect("movies.show", id=id)
