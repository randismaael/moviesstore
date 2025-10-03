from django.contrib import admin
from .models import Petition, Vote

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "yes_count", "created_by", "created_at")
    search_fields = ("title",)

admin.site.register(Vote)
