from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", views.index, name="homepage"),
    path("form", views.form_res, name="form_res"),
    path("contriform", views.form_contributors_res, name="form_contributors_res"),
]
