from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Film

def wszystkie(request):
    return HttpResponse("Hello World")




class FilmView(APIView):
    def get(self, request, format=None):
        przykladowy_film = Film("Incepcja", "Christopher Nolan", 2010, 8.8, ["Akcja", "Sci-Fi", "Thriller"])
        return Response(przykladowy_film.__dict__)