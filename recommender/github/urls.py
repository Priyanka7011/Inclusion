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

]