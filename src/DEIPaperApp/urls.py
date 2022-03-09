"""DEIPaperApp URL Configuration."""

from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect("papers/"), name = "index"),
    path("papers/", views.list_papers, name = "list_papers"),
    path("papers/offset=<int:offset>&lines=<int:lines>", views.list_papers, name = "list_papers"),
    path("papers/new", views.new_paper, name = "new_paper"),
    path("paper/<int:paper_id>", views.show_paper, name = "show_paper"),
    path("paper/<int:paper_id>/update", views.update_paper, name = "update_paper"),
    path("paper/<int:paper_id>/delete", views.delete_paper, name = "delete_paper"),
]
