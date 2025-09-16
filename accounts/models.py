from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class MovieRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=200)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie_name} requested by {self.user.username}"
