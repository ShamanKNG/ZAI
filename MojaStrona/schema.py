import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Film, ExtraInfo, Ocena, Aktor
from django.db.models import Count
from graphql_jwt.decorators import login_required

# Typy

class FilmType(DjangoObjectType):
    class Meta:
        model = Film
        fields = ("id", "tytul", "rok", "opis", "premiera", "imdb_points", "owner", "extrainfo")

    stary_nowy_film = graphene.String(default_value="")
    rok2 = graphene.Int()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"

class ExtraInfoType(DjangoObjectType):
    class Meta:
        model = ExtraInfo
        convert_choices_to_enum = False
        fields = ("id", "czas_trwania", "gatunek", "rezyser", "filmy", "owner")

class OcenaType(DjangoObjectType):
    class Meta:
        model = Ocena
        fields = "__all__"

class AktorType(DjangoObjectType):
    class Meta:
        model = Aktor
        fields = "__all__"

# Filtry

class Filters(graphene.InputObjectType):
    tytul_zawiera = graphene.String(default_value="")
    rok_mniejszy_od = graphene.Int(default_value=2000)
    nazwisko_aktora = graphene.String(default_value="")

# Query

class Query(graphene.ObjectType):
    filmy = graphene.List(FilmType, filters=Filters())
    aktorzy = graphene.List(AktorType, filters=Filters())

    @login_required
    def resolve_filmy(root, info, filters):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Nie dostarczono danych uwierzytelniających')

        filmy = Film.objects.all()
        for f in filmy:
            if f.rok < filters.rok_mniejszy_od:
                f.stary_nowy_film = "Stary film"
            else:
                f.stary_nowy_film = "Nowy film"
        if len(filters.tytul_zawiera) > 0:
            films = Film.objects.filter(tytul__contains=filters.tytul_zawiera)
            for f in films:
                if f.rok < filters.rok_mniejszy_od:
                    f.stary_nowy_film = "Stary film"
                else:
                    f.stary_nowy_film = "Nowy film"
            return films
        return filmy

    def resolve_aktorzy(root, info, filters):
        aktorzy = Aktor.objects.all()
        if len(filters.nazwisko_aktora) > 0:
            aktor = Aktor.objects.filter(nazwisko__contains=filters.nazwisko_aktora)
            return aktor
        return aktorzy

# Mutacje

class FilmCreateMutation(graphene.Mutation):
    class Arguments:
        tytul = graphene.String(required=True)
        opis = graphene.String()
        rok = graphene.String()
        imdb_points = graphene.Decimal()
        owner_id = graphene.ID()

    film = graphene.Field(FilmType)

    @classmethod
    def mutate(cls, root, info, tytul, opis, rok, imdb_points, owner_id):
        film = Film.objects.create(tytul=tytul, opis=opis, rok=rok, imdb_points=imdb_points, owner_id=owner_id)
        return FilmCreateMutation(film=film)

class FilmUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tytul = graphene.String(required=True)
        opis = graphene.String()
        rok = graphene.String()
        imdb_points = graphene.Decimal()
        premiera = graphene.Date(default_value=None)
        owner_id = graphene.ID()

    film = graphene.Field(FilmType)

    @classmethod
    def mutate(cls, root, info, id, tytul, opis, rok, imdb_points, premiera, owner_id):
        film = Film.objects.get(pk=id)
        film.opis = opis
        film.rok = rok
        film.premiera = premiera
        film.imdb_points = imdb_points
        film.owner_id = owner_id
        film.save()
        return FilmUpdateMutation(film=film)

class FilmDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    film = graphene.List(FilmType)

    @classmethod
    def mutate(cls, root, info, id):
        Film.objects.get(pk=id).delete()
        filmy = Film.objects.all()
        return FilmDeleteMutation(film=filmy)

class Mutation(graphene.ObjectType):
    create_film = FilmCreateMutation.Field()
    update_film = FilmUpdateMutation.Field()
    delete_film = FilmDeleteMutation.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
