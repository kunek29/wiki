from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:result>/", views.entry_page, name="entry_page"),
    path("results", views.results, name="results")
]
