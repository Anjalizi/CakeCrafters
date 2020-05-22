"""shopbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.views.static import serve

# to load images
from django.conf.urls.static import static
from django.conf import settings

import products.views as product_views

urlpatterns = [
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('checkout/',product_views.checkout, name='checkout'),
    path('', product_views.index, name='index'),
    path('', include('payments.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
