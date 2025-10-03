from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    yes_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

# Optional: one-vote-per-user (recommended)
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name="votes")
    value = models.CharField(max_length=3, default="yes")

    class Meta:
        unique_together = ("user", "petition")
