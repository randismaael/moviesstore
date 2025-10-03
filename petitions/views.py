from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .forms import PetitionForm
from .models import Petition, Vote

def petition_list(request):
    qs = Petition.objects.order_by("-created_at")
    return render(request, "petitions/list.html", {"petitions": qs})

@login_required
def petition_create(request):
    if request.method == "POST":
        form = PetitionForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.created_by = request.user
            p.save()
            messages.success(request, "Petition created.")
            return redirect("petitions:detail", pk=p.pk)
    else:
        form = PetitionForm()
    return render(request, "petitions/new.html", {"form": form})

def petition_detail(request, pk):
    p = get_object_or_404(Petition, pk=pk)
    user_has_voted = False
    if request.user.is_authenticated:
        user_has_voted = Vote.objects.filter(user=request.user, petition=p).exists()
    return render(request, "petitions/detail.html", {"petition": p, "user_has_voted": user_has_voted})

@login_required
def petition_vote_yes(request, pk):
    p = get_object_or_404(Petition, pk=pk)

    # one-vote-per-user:
    created = False
    vote, created = Vote.objects.get_or_create(user=request.user, petition=p, defaults={"value": "yes"})
    if created:
        Petition.objects.filter(pk=p.pk).update(yes_count=F("yes_count") + 1)
        messages.success(request, "Your 'Yes' vote was recorded.")
    else:
        messages.info(request, "You already voted on this petition.")

    return redirect("petitions:detail", pk=p.pk)
