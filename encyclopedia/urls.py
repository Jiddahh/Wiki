from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/edit_page", views.edit_page, name="edit_page"),
    path("wiki/random_page", views.random_page, name="random_page"),
    path("wiki/create_new_page", views.create_new_page, name="create_new_page"),
    path("wiki/<str:title>/", views.get_entries, name="get_entries")
]
