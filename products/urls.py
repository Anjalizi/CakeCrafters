from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'products'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    path('category1', views.category1, name='cat1'),
    path('category2', views.category2, name='cat2'),
    url(r'^(?P<pk>[0-9]+)/cart/$', views.cart, name='cart'),
    url(r'^(?P<pk>[0-9]+)/cart/(?P<pid>[0-9]+)/$', views.add2cart, name='add2cart'),
    url(r'^(?P<pk>[0-9]+)/cart/remove/(?P<pid>[0-9]+)/$', views.removeFromCart, name='removeFromCart'),
]