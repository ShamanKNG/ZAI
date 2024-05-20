from django.contrib.auth.models import User
from django.db.models import Max

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Inne importy
from .models import Film, ExtraInfo, Ocena, Aktor
from .serializers import FilmModelSerializer, ExtraInfoSerializer, OcenaSerializer, AktorSerializer, UserSerializer, UserSerializerShort,statRezyser, statOceny
from rest_framework import generics, status

from django.db.models import Count, Q, Max, Min

class ListaUzytkownikow(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializerShort

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(data=None, status=status.HTTP_403_FORBIDDEN)

class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializerShort

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response(data=None, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
class FilmCreateList(generics.ListCreateAPIView):
    queryset = Film.objects.all().order_by('-rok', 'tytul')
    serializer_class = FilmModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Film.objects.all().order_by('-rok', 'tytul')
        tytul = self.request.query_params.get('tytul')
        id = self.request.query_params.get('id')
        if tytul is not None:
            queryset = queryset.filter(tytul__startswith=tytul)
        if id is not None:
            queryset = queryset.filter(id__exact=id)
        return queryset

class FilmRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class ExtraInfoCreateList(generics.ListCreateAPIView):
    queryset = ExtraInfo.objects.all()
    serializer_class = ExtraInfoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ExtraInfoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExtraInfo.objects.all()
    serializer_class = ExtraInfoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class OcenaCreateList(generics.ListCreateAPIView):
    queryset = Ocena.objects.all()
    serializer_class = OcenaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class OcenaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ocena.objects.all()
    serializer_class = OcenaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class AktorCreateList(generics.ListCreateAPIView):
    queryset = Aktor.objects.all()
    serializer_class = AktorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AktorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Aktor.objects.all()
    serializer_class = AktorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserCreateList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerShort
    permission_classes = [IsAuthenticated]

class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerShort
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# Nowy widok api_root
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'Użytkownicy': reverse('user-list', request=request, format=format),
        'Wszystkie filmy': reverse('film-list', request=request, format=format),
        'Informacje dodatkowe': reverse('extrainfo-list', request=request, format=format),
        'Wszystkie oceny': reverse('ocena-list', request=request, format=format),
        'Wszyscy aktorzy': reverse('aktor-list', request=request, format=format),
    })


class statRezyserLiczbaFilmow(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = statRezyser

    def get_queryset(self):
        rezyserzy = ExtraInfo.objects.values('rezyser').annotate(liczba_filmow=Count('filmy')).order_by('-liczba_filmow')
        return rezyserzy

class statFilmyLiczbaOcen(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = statOceny

    def get_queryset(self):
        filmy = Film.objects.annotate(liczba_ocen=Count('ocena')).order_by('-liczba_ocen')
        return filmy

class statFilmyKategorieDobrySlaby(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = statOceny

    def get_queryset(self):
        filmy = Film.objects.annotate(
            dobry=Count('ocena', filter=Q(ocena__gwiazdki__gt=5)),
            slaby=Count('ocena', filter=Q(ocena__gwiazdki__lte=5))
        ).order_by('-dobry')
        return filmy

class statFilmyGwiazdkiMaxMin(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = statOceny

    def get_queryset(self):
        filmy = Film.objects.annotate(
            max_gwiazdki=Max('ocena__gwiazdki'),
            min_gwiazdki=Min('ocena__gwiazdki')
        ).order_by('-max_gwiazdki')
        return filmy

class statFilmyBezOcen(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FilmModelSerializer

    def get_queryset(self):
        filmy_bez_ocen = Film.objects.filter(ocena__isnull=True)
        return filmy_bez_ocen

    @api_view(['GET'])
    def api_root(request, format=None):
        return Response({
            'Użytkownicy': reverse('user-list', request=request, format=format),
            'Wszystkie filmy': reverse('film-list', request=request, format=format),
            'Informacje dodatkowe': reverse('extrainfo-list', request=request, format=format),
            'Wszystkie oceny': reverse('ocena-list', request=request, format=format),
            'Wszyscy aktorzy': reverse('aktor-list', request=request, format=format),
            'Statystyki_rezyser_liczba_filmow': reverse('statRezyserLiczbaFilmow', request=request, format=format),
            'Statystyki_filmy_liczba_ocen': reverse('statFilmyLiczbaOcen', request=request, format=format),
            'Statystyki_filmy_bez_ocen': reverse('statFilmyBezOcen', request=request, format=format),
            'Statystyki_filmy_dobre_slabe': reverse('statFilmyKategorieDobrySlaby', request=request, format=format),
            'Statystyki_filmy_gwiazdki_max_min': reverse('statFilmyGwiazdkiMaxMin', request=request, format=format),
        })