import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Film, ExtraInfo, Ocena, Aktor
from graphql_relay import from_global_id

class ExtraInfoType(DjangoObjectType):
    class Meta:
        model = ExtraInfo
        fields = "__all__"

class OcenaType(DjangoObjectType):
    class Meta:
        model = Ocena
        fields = "__all__"

class AktorType(DjangoObjectType):
    class Meta:
        model = Aktor
        fields = "__all__"

class FilmNode(DjangoObjectType):
    class Meta:
        model = Film
        filter_fields = {
            'tytul': ['exact', 'contains', 'startswith'],
            'rok': ['exact']
        }
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    filmy = DjangoFilterConnectionField(FilmNode)
    film_wg_id = relay.Node.Field(FilmNode)

    def resolve_filmy(root, info, **kwargs):
        return Film.objects.all()

    def resolve_film_wg_id(root, info, id):
        film_id = from_global_id(id)[1]
        return Film.objects.get(pk=film_id)

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

class FilmUpdateMutationRelay(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()
        tytul = graphene.String(required=True)

    film = graphene.Field(FilmNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, tytul, id):
        film = Film.objects.get(pk=from_global_id(id)[1])
        film.tytul = tytul
        film.save()
        return FilmUpdateMutationRelay(film=film)

class Mutation(graphene.ObjectType):
    create_film = FilmCreateMutation.Field()
    update_film_relay = FilmUpdateMutationRelay.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
