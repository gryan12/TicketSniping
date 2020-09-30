"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from api import views as api_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from sniping_site import views

router = routers.DefaultRouter()
router.register(r'theatres', views.theatreView, 'Theatre')
router.register(r'play', views.playView, 'Play')
router.register(r'section', views.sectionView, 'Section')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('formSearch/', views.formSearch),
    path('checkAlerts/', views.checkAlerts),
    path('emailAlert/', views.emailAlert),
    url(r'^admin/', admin.site.urls),
    url(r'^', api_views.ReactAppView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
