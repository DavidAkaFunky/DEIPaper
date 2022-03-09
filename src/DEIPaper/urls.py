"""DEIPaper URL Configuration. As it only contains
one app, the main page was chosen to automatically
redirect to the app's main page."""

from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("DEIPaper/"), name = "index"),
    path("DEIPaper/", include("DEIPaperApp.urls"))
]
