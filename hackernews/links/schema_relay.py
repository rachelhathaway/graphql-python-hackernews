import graphene
import django_filters

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Link, Vote
from users.schema import get_user, UserType

class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = Link
        fields = ['url', 'description']


class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        interfaces = (graphene.relay.Node,)


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (graphene.relay.Node,)


class RelayCreateLink(graphene.relay.ClientIDMutation):
    link = graphene.Field(LinkNode)

    class Input:
        url = graphene.String()
        description = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = get_user(info)
        link = Link(
            url=input.get('url'),
            description=input.get('description'),
            posted_by=user,
        )
        return RelayCreateLink(link=link)


class RelayQuery(graphene.ObjectType):
    relay_link = graphene.relay.Node.Field(LinkNode)
    relay_links = DjangoFilterConnectionField(LinkNode, filterset_class=LinkFilter)


class RelayMutation(graphene.AbstractType):
    relay_create_link = RelayCreateLink.Field()
