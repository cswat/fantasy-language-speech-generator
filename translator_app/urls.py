from django.urls import path
from translator_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("translator", views.translation_form, name="translation_form"),
]