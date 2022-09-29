from django.urls import path

from . import views

app_name ="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.page, name="page"),
    path("search/", views.search, name="search"),
    path("new", views.new, name="new"),
    path("random", views.random_entry, name="random_entry"),
    path("edit/<str:entry>", views.edit, name="edit"),
]
