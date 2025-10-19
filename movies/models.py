# movies/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.utils import timezone


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to="movie_images/")

    def __str__(self):
        return f"{self.id} - {self.name}"

    # ---- ratings helpers ----
    @property
    def average_rating(self):
        return self.ratings.aggregate(avg=Avg("value"))["avg"] or 0.0

    @property
    def ratings_count(self):
        return self.ratings.aggregate(cnt=Count("id"))["cnt"] or 0


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.movie.name}"


# NEW
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name="ratings", on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "movie"], name="unique_user_movie_rating"
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.movie} = {self.value}"
