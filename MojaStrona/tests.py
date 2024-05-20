from django.urls import path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .views import FilmCreateList, FilmRetrieveUpdateDestroy, ExtraInfoCreateList, ListaUzytkownikow, UserRetrieveUpdateDestroy, statRezyserLiczbaFilmow, statFilmyLiczbaOcen, statFilmyBezOcen, statFilmyKategorieDobrySlaby, statFilmyGwiazdkiMaxMin
from .models import Film

class TestyURL(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('filmy/', FilmCreateList.as_view(), name='ListaFilmow'),
        path('filmy/<int:pk>/', FilmRetrieveUpdateDestroy.as_view(), name='film-detail'),
        path('extrainfo/', ExtraInfoCreateList.as_view(), name='InformacjeDodatkowe'),
        path('user/', ListaUzytkownikow.as_view(), name='ListaUzytkownikow'),
        path('user/<pk>/', UserRetrieveUpdateDestroy.as_view(), name='UserRetrieveUpdateDestroy'),
        path('statRezyserLiczbaFilmow/', statRezyserLiczbaFilmow.as_view(), name='statRezyserLiczbaFilmow'),
        path('statFilmyLiczbaOcen/', statFilmyLiczbaOcen.as_view(), name='statFilmyLiczbaOcen'),
        path('statFilmyBezOcen/', statFilmyBezOcen.as_view(), name='statFilmyBezOcen'),
        path('statFilmyDobrySlaby/', statFilmyKategorieDobrySlaby.as_view(), name='statFilmyKategorieDobrySlaby'),
        path('statFilmyGwiazdkiMaxMin/', statFilmyGwiazdkiMaxMin.as_view(), name='statFilmyGwiazdkiMaxMin'),
    ]

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        User.objects.create_superuser(username='admin', password='admin')

    def test_FilmCreateList(self):
        url = reverse('ListaFilmow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_FilmRetrieveUpdateDestroy(self):
        url = reverse('film-detail', args=[1])
        Film.objects.create(tytul="Film testowy", rok=2024, opis="opis")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ExtraInfoCreateList(self):
        self.client.login(username='admin', password='admin')
        url = reverse('InformacjeDodatkowe')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ListaUzytkownikow(self):
        self.client.login(username='admin', password='admin')
        url = reverse('ListaUzytkownikow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_UserRetrieveUpdateDestroy(self):
        self.client.login(username='admin', password='admin')
        url = reverse('UserRetrieveUpdateDestroy', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statRezyserLiczbaFilmow(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statRezyserLiczbaFilmow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyLiczbaOcen(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statFilmyLiczbaOcen')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyBezOcen(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statFilmyBezOcen')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyDobrySlaby(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statFilmyKategorieDobrySlaby')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyGwiazdkiMaxMin(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statFilmyGwiazdkiMaxMin')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class Testy_Widokow(APITestCase):

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        User.objects.create_superuser(username='admin', password='admin')

    def test_FilmCreateList_List(self):
        url = reverse('ListaFilmow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_FilmCreateList_Create(self):
        self.client.login(username='admin', password='admin')
        url = reverse('ListaFilmow')
        film = {'tytul': 'Film testowy', 'rok': 2024, 'opis': 'opis'}
        response = self.client.post(url, film, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')
        self.assertEqual(Film.objects.get().rok, 2024)
        self.assertEqual(Film.objects.get().opis, 'opis')

    def test_FilmRetrieveUpdateDestroy_Retrieve(self):
        Film.objects.create(tytul="Film testowy", rok=2024, opis="opis")
        url = reverse('film-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')

    def test_FilmRetrieveUpdateDestroy_Update(self):
        self.client.login(username='admin', password='admin')
        Film.objects.create(tytul="Film testowy 2", rok=2024, opis="opis", owner=User.objects.get(id=1))
        url = reverse('film-detail', args=[1])
        film = {'tytul': 'Film testowy', 'rok': 2020, 'opis': 'opis opis'}
        response = self.client.put(url, film, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().rok, 2020)
        self.assertEqual(Film.objects.get().tytul, 'Film testowy')
        self.assertEqual(Film.objects.get().opis, 'opis opis')

    def test_FilmRetrieveUpdateDestroy_Destroy(self):
        self.client.login(username='admin', password='admin')
        Film.objects.create(tytul="Film testowy", rok=2024, opis="opis", owner=User.objects.get(id=1))
        url = reverse('film-detail', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Film.objects.count(), 0)

    def test_statRezyserLiczbaFilmow(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statRezyserLiczbaFilmow')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyLiczbaOcen(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statFilmyLiczbaOcen')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyBezOcen(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statFilmyBezOcen')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyDobrySlaby(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statFilmyKategorieDobrySlaby')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statFilmyGwiazdkiMaxMin(self):
        self.client.login(username='admin', password='admin')
        url = reverse('statFilmyGwiazdkiMaxMin')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
