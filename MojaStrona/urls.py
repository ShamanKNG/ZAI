"""
URL configuration for ZAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from MojaStrona import views
from django.urls import path
from .views import FilmView
from .views import FilmList, FilmRetrieve,FilmCreateList, UserList, UserCreateList
urlpatterns = [
    path('wszystkie/', views.wszystkie),
    path('filmy/', FilmList.as_view(), name='film-list'),
    path('filmy/<int:pk>/', FilmRetrieve.as_view(), name='film-detail'),
    path('filmy/create/', FilmCreateList.as_view(), name='film-create-list'),
    path('api/film/', FilmView.as_view(), name='film-api'),
    path('userlist/', UserList.as_view(), name='UserList'),
    path('usercreatelist/', UserCreateList.as_view(), name='UserCreateList')
]

