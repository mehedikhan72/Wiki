from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title_name>/", views.title, name="title"),
    path("new_page", views.new_page, name="new_page"),
    path("edit_page/<str:title_name>", views.edit_page, name="edit_page"),
    path("wiki/random", views.random_page, name="random_page")
]
