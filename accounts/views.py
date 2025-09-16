from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList

# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MovieRequestForm
from .models import MovieRequest


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home.index")


def login(request):
    template_data = {}
    template_data["title"] = "Login"
    if request.method == "GET":
        return render(request, "accounts/login.html", {"template_data": template_data})
    elif request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
    if user is None:
        template_data["error"] = "The username or password is incorrect."
        return render(request, "accounts/login.html", {"template_data": template_data})
    else:
        auth_login(request, user)
        return redirect("home.index")


def signup(request):
    template_data = {}
    template_data["title"] = "Sign Up"

    if request.method == "GET":
        template_data["form"] = CustomUserCreationForm()
        return render(request, "accounts/signup.html", {"template_data": template_data})

    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect("accounts.login")
        else:
            template_data["form"] = form
            return render(
                request, "accounts/signup.html", {"template_data": template_data}
            )


@login_required
def orders(request):
    template_data = {}
    template_data["title"] = "Orders"
    template_data["orders"] = request.user.order_set.all()
    return render(request, "accounts/orders.html", {"template_data": template_data})


@login_required
def add_movie_request(request):
    if request.method == "POST":
        form = MovieRequestForm(request.POST)
        if form.is_valid():
            movie_request = form.save(commit=False)
            movie_request.user = request.user
            movie_request.save()
            return redirect("accounts.my_requests")
    else:
        form = MovieRequestForm()
    return render(request, "accounts/add_movie_request.html", {"form": form})


@login_required
def my_requests(request):
    requests = MovieRequest.objects.filter(user=request.user)
    return render(request, "accounts/my_requests.html", {"requests": requests})


@login_required
def delete_request(request, pk):
    r = get_object_or_404(MovieRequest, pk=pk, user=request.user)
    r.delete()
    return redirect("accounts.my_requests")
