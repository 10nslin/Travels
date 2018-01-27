from django.conf.urls import url
from . import views          
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.travels),
    url(r'^add_plan$', views.add_plan),
    url(r'^add_trip$', views.add_trip),
    url(r'^travelers/(?P<id>\d+)$', views.travelers),
    url(r'^destination/(?P<id>\d+)$', views.destination),
 

]