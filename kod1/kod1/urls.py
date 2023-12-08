
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from pages import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.homePageView, name='home'),
    path('about/', views.aboutPageView, name='about'),
    path('vetKod/', include('pages.urls')),
    path('vetKod/', include('django.contrib.auth.urls')),
]
