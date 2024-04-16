from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Film
from .serializers import FilmModelSerializer, UserSerializerShort,UserSerializer
from django.contrib.auth.models import User



def wszystkie(request):
    return HttpResponse("Hello World")




class FilmView(APIView):
    def get(self, request, format=None):
        film_data = {
            'tytul': 'Incepcja',
            'rezyser': 'Christopher Nolan',
            'rok_produkcji': 2010,
            'ocena': 8.8,
            'gatunki': ['Akcja', 'Sci-Fi', 'Thriller']
        }
        serializer = FilmModelSerializer(data=film_data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class FilmList(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer

class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer

class FilmRetrieve(generics.RetrieveAPIView):
    """
    Retrieve a film instance.
    """
    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer

class FilmCreateList(generics.ListCreateAPIView):

    queryset = Film.objects.all()
    serializer_class = FilmModelSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerShort

class UserCreateList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer