import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id, to_global_id
from .models import Film, ExtraInfo, Ocena, Aktor



class ExtraInfoNode(DjangoObjectType):
    class Meta:
        model = ExtraInfo
        interfaces = (relay.Node, )
        fields = ("id", "czas_trwania", "gatunek", "rezyser", "filmy", "owner")

class OcenaNode(DjangoObjectType):
    class Meta:
        model = Ocena
        interfaces = (relay.Node, )
        fields = ("id", "gwiazdki", "recenzja", "film", "owner")

class AktorNode(DjangoObjectType):
    class Meta:
        model = Aktor
        interfaces = (relay.Node, )
        fields = ("id", "imie", "nazwisko", "filmy")

class FilmNode(DjangoObjectType):
    class Meta:
        model = Film
        filter_fields = {
            'tytul': ['exact', 'contains', 'startswith'],
            'rok': ['exact']
        }
        interfaces = (relay.Node, )

    extrainfo = graphene.List(ExtraInfoNode)
    aktorzy = graphene.List(AktorNode)

    def resolve_extrainfo(self, info):
        return self.extrainfo_set.all()

    def resolve_aktorzy(self, info):
        return self.aktor_set.all()

class Query(graphene.ObjectType):
    filmy = DjangoFilterConnectionField(FilmNode)
    film_wg_id = relay.Node.Field(FilmNode)

class FilmCreateMutation(graphene.Mutation):
    class Arguments:
        tytul = graphene.String(required=True)
        opis = graphene.String()
        rok = graphene.String()
        imdb_points = graphene.Decimal()
        owner_id = graphene.ID()

    film = graphene.Field(FilmNode)

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

    film = graphene.Field(FilmNode)

    @classmethod
    def mutate(cls, root, info, id, tytul, opis, rok, imdb_points, premiera, owner_id):
        film = Film.objects.get(pk=from_global_id(id)[1])
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

    film = graphene.List(FilmNode)

    @classmethod
    def mutate(cls, root, info, id):
        Film.objects.get(pk=from_global_id(id)[1]).delete()
        filmy = Film.objects.all()
        return FilmDeleteMutation(film=filmy)

class FilmUpdateMutationRelay(relay.ClientIDMutation):
    class Input:
        tytul = graphene.String(required=True)
        id = graphene.ID()

    film = graphene.Field(FilmNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, tytul, id):
        film = Film.objects.get(pk=from_global_id(id)[1])
        film.tytul = tytul
        film.save()
        return FilmUpdateMutationRelay(film=film)

class Mutation(graphene.ObjectType):
    update_film = FilmUpdateMutation.Field()
    create_film = FilmCreateMutation.Field()
    delete_film = FilmDeleteMutation.Field()
    update_film_relay = FilmUpdateMutationRelay.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)