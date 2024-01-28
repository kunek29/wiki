from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:result>/", views.entry_page, name="entry_page"),
    path("results", views.results, name="results"),
    path("create_page", views.create_page, name="create_page"),
    path("error_page", views.error_page, name='error_page')
]
