import graphene

import links.schema
import links.schema_relay
import users.schema

query_args = (
    users.schema.Query,
    links.schema.Query,
    links.schema_relay.RelayQuery,
    graphene.ObjectType,
)

mutation_args = (
    users.schema.Mutation,
    links.schema.Mutation,
    links.schema_relay.RelayMutation,
    graphene.ObjectType,
)

class Query(*query_args):
    pass


class Mutation(*mutation_args):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
