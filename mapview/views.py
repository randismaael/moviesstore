from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from cart.models import Item


@login_required
def map_page(request):
    """Render the Local Popularity Map page."""
    return render(request, "mapview/map.html")


@login_required
def local_popularity_data(request):
    """
    Returns JSON data showing how many times each movie was purchased
    in each region (city/state/country).
    """
    data = (
        Item.objects
        .values(
            'order__user__userprofile__city',
            'order__user__userprofile__state',
            'order__user__userprofile__country',
            'movie__name'
        )
        .annotate(count=Count('movie'))
        .order_by('-count')
    )

    results = {}
    for entry in data:
        region = ", ".join(filter(None, [
            entry['order__user__userprofile__city'],
            entry['order__user__userprofile__state'],
            entry['order__user__userprofile__country']
        ])) or "Tokyo, Japan"  # fallback region for testing

        movie = entry['movie__name']
        count = entry['count']
        results.setdefault(region, []).append({'movie': movie, 'count': count})

    # Sort each region's movies by count (descending)
    for region, movies in results.items():
        results[region] = sorted(movies, key=lambda m: m['count'], reverse=True)

    return JsonResponse(results)