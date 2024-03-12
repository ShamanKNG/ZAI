import json
from django.db import models

# Create your models here.
class Film:
    def __init__(self, tytul, rezyser, rok_produkcji, ocena, gatunki):
        self.tytul = tytul
        self.rezyser = rezyser
        self.rok_produkcji = rok_produkcji
        self.ocena = ocena
        self.gatunki = gatunki


# Przykładowy obiekt klasy Film
przykladowy_film = Film("Incepcja", "Christopher Nolan", 2010, 8.8, ["Akcja", "Sci-Fi", "Thriller"])

# Serializacja obiektu do formatu JSON
film_json = json.dumps(przykladowy_film.__dict__)

# Zapis serializowanego obiektu do zmiennej
film_json_zmienna = film_json

# Deserializacja z JSON do obiektu klasy Film
film_dict = json.loads(film_json_zmienna)
przywrocony_film = Film(**film_dict)

# Sprawdzenie wyników
print(film_json_zmienna, przywrocony_film.__dict__)