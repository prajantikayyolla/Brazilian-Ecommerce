"""TrailProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import re
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from . import views
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.olisthome),
# ]

if settings.DEBUG:
    urlpatterns = [
                      path('admin/', admin.site.urls),
                      path('', views.olisthome),
        path('OlistExe.html', views.olistexe, name='OlistExe'),
        path('OlistHome.html', views.olisthome),
        path('Customer.html', views.customer, name='C'),
        path('CustomerProducts/', views.customer_products),
        path('CustomerCountMonthly/', views.customer_count_monthly),
        path('CustomerNext.html', views.customer_next, name='CN'),
        path('Facts.html', views.facts),
        path('Seller.html', views.seller, name='seller')
                      # ... the rest of your URLconf goes here ...
                  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
