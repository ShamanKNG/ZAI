from django.urls import path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .views import (
    FilmCreateList, FilmRetrieveUpdateDestroy, ExtraInfoCreateList, ExtraInfoRetrieveUpdateDestroy,
    OcenaCreateList, OcenaRetrieveUpdateDestroy, AktorCreateList, AktorRetrieveUpdateDestroy,
    ListaUzytkownikow, UserRetrieveUpdateDestroy, statRezyserLiczbaFilmow, statFilmyLiczbaOcen,
    statFilmyBezOcen, statFilmyKategorieDobrySlaby, statFilmyGwiazdkiMaxMin, api_root
)
from .models import Film


class TestyURL(APITestCase, URLPatternsTestCase):
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

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_FilmCreateList(self):
        url = reverse('film-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_FilmRetrieveUpdateDestroy(self):
        film = Film.objects.create(tytul="Film testowy", rok=2024, opis="opis")
        url = reverse('film-detail', args=[film.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ExtraInfoCreateList(self):
        url = reverse('extrainfo-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ListaUzytkownikow(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_UserRetrieveUpdateDestroy(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statRezyserLiczbaFilmow(self):
        url = reverse('statRezyserLiczbaFilmow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyLiczbaOcen(self):
        url = reverse('statFilmyLiczbaOcen')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyBezOcen(self):
        url = reverse('statFilmyBezOcen')
        response = self.client.get(url, format='json')
        self.assertEqual

    def test_statFilmyDobrySlaby(self):
        url = reverse('statFilmyKategorieDobrySlaby')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyGwiazdkiMaxMin(self):
        url = reverse('statFilmyGwiazdkiMaxMin')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_FilmCreateList_List(self):
        url = reverse('film-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_FilmCreateList_Create(self):
        url = reverse('film-list')
        film_data = {'tytul': 'Film testowy', 'rok': 2024, 'opis': 'opis'}
        response = self.client.post(url, film_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')
        self.assertEqual(Film.objects.get().rok, 2024)
        self.assertEqual(Film.objects.get().opis, 'opis')

    def test_FilmRetrieveUpdateDestroy_Retrieve(self):
        film = Film.objects.create(tytul="Film testowy", rok=2024, opis="opis")
        url = reverse('film-detail', args=[film.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')

    def test_FilmRetrieveUpdateDestroy_Update(self):
        film = Film.objects.create(tytul="Film testowy 2", rok=2024, opis="opis", owner=self.user)
        url = reverse('film-detail', args=[film.id])
        updated_film = {'tytul': 'Film testowy', 'rok': 2020, 'opis': 'opis opis'}
        response = self.client.put(url, updated_film, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().rok, 2020)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')
        self.assertEqual(Film.objects.get().opis, 'opis opis')

    def test_FilmRetrieveUpdateDestroy_Destroy(self):
        film = Film.objects.create(tytul="Film testowy", rok=2024, opis="opis", owner=self.user)
        url = reverse('film-detail', args=[film.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Film.objects.count(), 0)

    def test_statRezyserLiczbaFilmow(self):
        url = reverse('statRezyserLiczbaFilmow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyLiczbaOcen(self):
        url = reverse('statFilmyLiczbaOcen')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyBezOcen(self):
        url = reverse('statFilmyBezOcen')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyDobrySlaby(self):
        url = reverse('statFilmyKategorieDobrySlaby')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyGwiazdkiMaxMin(self):
        url = reverse('statFilmyGwiazdkiMaxMin')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

