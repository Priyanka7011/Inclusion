from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('',views.index,name='homepage'),
    path('', TemplateView.as_view(template_name = 'index.html'), name = 'index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('logout',views.logout_view,name='logout'),
    path('repo/<str:sortid>',views.repo_rec,name='repo_rec'),
    path('repo',views.repo_rec,name='repo_rec'),
    
    path("form", views.form_res, name="form_res"),
    path("contriform", views.form_contributors_res, name="form_contributors_res"),
    path("user", views.user_rec, name="user_rec"),
    path("orgs", views.org_recs, name="org_recs"),
]
