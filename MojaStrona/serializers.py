from rest_framework import serializers
from django.contrib.auth.models import User
class FilmModelSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Film  # Import umieszczony wewnątrz klasy
        model = Film
        fields = ['tytul', 'rezyser', 'rok_produkcji', 'ocena', 'gatunki']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'is_superuser', 'email', 'is_staff', 'is_active']
