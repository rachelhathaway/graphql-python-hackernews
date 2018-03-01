import graphene

from django.contrib.auth import authenticate
from graphene_django import DjangoObjectType

from users.models import User


def get_user(info):
    token = info.context.session.get('token')
    if token:
        try:
            return User.objects.get(token=token)
        except:
            raise Exception('User not found')
    else:
        return


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_me(self, info):
        user = get_user(info)
        if not user:
            raise Exception('Not logged in')
        return user

    def resolve_users(self, info):
        return User.objects.all()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class Login(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            raise Exception('Invalid username or password')
        info.context.session['token'] = user.token
        return Login(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login = Login.Field()
