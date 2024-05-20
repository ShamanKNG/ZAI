from django.urls import path
from .views import FilmCreateList, FilmRetrieveUpdateDestroy, ExtraInfoCreateList, ExtraInfoRetrieveUpdateDestroy, OcenaCreateList, OcenaRetrieveUpdateDestroy, AktorCreateList, AktorRetrieveUpdateDestroy, ListaUzytkownikow, UserRetrieveUpdateDestroy, api_root, statRezyserLiczbaFilmow, statFilmyLiczbaOcen, statFilmyBezOcen, statFilmyKategorieDobrySlaby, statFilmyGwiazdkiMaxMin


urlpatterns = [
    path('', api_root, name='api-root'),
    path('filmy/', FilmCreateList.as_view(), name='film-list'),
    path('filmy/<int:pk>/', FilmRetrieveUpdateDestroy.as_view(), name='film-detail'),
    path('extrainfo/', ExtraInfoCreateList.as_view(), name='extrainfo-list'),
    path('extrainfo/<int:pk>/', ExtraInfoRetrieveUpdateDestroy.as_view(), name='extrainfo-detail'),
    path('ocena/', OcenaCreateList.as_view(), name='ocena-list'),
    path('ocena/<int:pk>/', OcenaRetrieveUpdateDestroy.as_view(), name='ocena-detail'),
    path('aktor/', AktorCreateList.as_view(), name='aktor-list'),
    path('aktor/<int:pk>/', AktorRetrieveUpdateDestroy.as_view(), name='aktor-detail'),
    path('user/', ListaUzytkownikow.as_view(), name='user-list'),
    path('user/<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name='user-detail'),
    path('statRezyserLiczbaFilmow/', statRezyserLiczbaFilmow.as_view(), name='statRezyserLiczbaFilmow'),
    path('statFilmyLiczbaOcen/', statFilmyLiczbaOcen.as_view(), name='statFilmyLiczbaOcen'),
    path('statFilmyBezOcen/', statFilmyBezOcen.as_view(), name='statFilmyBezOcen'),
    path('statFilmyDobrySlaby/', statFilmyKategorieDobrySlaby.as_view(), name='statFilmyKategorieDobrySlaby'),
    path('statFilmyGwiazdkiMaxMin/', statFilmyGwiazdkiMaxMin.as_view(), name='statFilmyGwiazdkiMaxMin'),
]
