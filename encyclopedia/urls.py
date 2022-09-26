from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title_name>", views.title, name="title"),
    path("new_page", views.new_page, name="new_page")
]