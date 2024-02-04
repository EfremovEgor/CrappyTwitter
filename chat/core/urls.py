from django.urls import path, re_path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.LoginFormView.as_view(), name="login"),
    path("register/", views.RegisterFormView.as_view(), name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("profile_list/", views.profile_list, name="profile_list"),
    path("profile/<int:pk>", views.profile, name="profile"),
]
