
from django.contrib import admin
from django.urls import path, include
from django.views.defaults import permission_denied, page_not_found
from pages import views

handler403 = permission_denied
handler404 = page_not_found

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.ServiceListView.as_view(), name='home'),
    path('vetKod/', include('pages.urls')),
    path('vetKod/', include('django.contrib.auth.urls')),
]
