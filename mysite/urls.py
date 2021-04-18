"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from league import api
from league import views

urlpatterns = [
    path('hq/', admin.site.urls),

    path('api/generate', api.generate),
    path('api/signup', api.signup),
    path('api/decks', api.DeckList.as_view()),
    path('api/tables', api.TableList.as_view()),
    path('api/matches', api.TableList.as_view()),

    path('', views.index),

    path('__debug__/', include(debug_toolbar.urls)),
]
