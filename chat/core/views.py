from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import Profile, Tweet
from .forms import LoginForm, RegisterForm, TweetForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url="core:login")
def index(request):
    form = TweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("core:index")

    followed_tweets = Tweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")
    return render(
        request,
        "core/index.html",
        {"form": form, "tweets": followed_tweets},
    )


@login_required(login_url="core:login")
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "core/profile_list.html", {"profiles": profiles})


@login_required(login_url="core:login")
def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "core/profile.html", {"profile": profile})


def logout_user(request):
    logout(request)
    return redirect(reverse_lazy("core:login"))


class RegisterFormView(FormView):
    template_name = "core/register.html"
    form_class = RegisterForm
    success_url = "core:login"

    def get(self, form):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy("core:index"))
        return render(
            self.request,
            self.template_name,
            {
                "title": "Регистрация",
                "form": self.form_class,
            },
        )

    def form_valid(self, form):
        if User.objects.filter(username=form.cleaned_data["username"]).first():
            return HttpResponse("Пользователь с таким именем уже существует")
        user = User(
            username=form.cleaned_data["username"],
        )
        user.set_password(form.cleaned_data["password"])
        user.save()
        return redirect(reverse_lazy(self.success_url))


class LoginFormView(FormView):
    template_name = "core/login.html"
    form_class = LoginForm
    success_url = "core:index"

    def get(self, form):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy("core:index"))
        return render(
            self.request,
            self.template_name,
            {
                "title": "Вход",
                "form": self.form_class,
            },
        )

    def form_valid(self, form):
        user = authenticate(
            self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )

        if user is not None:
            login(self.request, user)
            return redirect(reverse_lazy(self.success_url))

        return redirect(reverse_lazy("core:login"))
