"""DEIPaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""

from django.urls import path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda _: redirect("papers/"), name = "index"),
    path("papers/", views.list_papers, name = "list_papers_main"),
    path("papers/page=<int:page>&lines=<int:lines>", views.list_papers, name = "list_papers"),
    path("papers/new", views.new_paper, name = "new_paper"),
    path("paper/<int:paper_id>", views.show_paper, name = "show_paper"),
    path("paper/<int:paper_id>/update", views.update_paper, name = "update_paper"),
    path("paper/<int:paper_id>/delete", views.delete_paper, name = "delete_paper"),
]
