import datetime
import os
from typing import NamedTuple

from rest_framework.decorators import api_view
from rest_framework import serializers, status, generics
from rest_framework.response import Response

from .models import Player, Deck, Table, Week
from .scheduler import create_matchups


class Signup(NamedTuple):
    discord_id: str
    name: str
    signup: bool


class SignupSerializer(serializers.Serializer):
    discord_id = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    signup = serializers.BooleanField()

    def create(self, validated_data):
        return Signup(**validated_data)


def auth_required(func):
    def wrapper(request):
        if 'Authorization' in request.headers and request.headers['Authorization'] == os.environ['API_KEY']:
            return func(request)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    return wrapper


@api_view(['POST'])
@auth_required
def generate(request):
    week = Week(start=datetime.datetime.today().date())
    week.save()

    matchups = create_matchups()
    for m in matchups:
        Table(week=week, player1=m[0],
                player1_corp_deck=m[5],
                player1_runner_deck=m[2],
                player2=m[1],
                player2_corp_deck=m[3],
                player2_runner_deck=m[4]).save()

    return Response({'status': 'ok'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@auth_required
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    signup = serializer.save()
    player, _ = Player.objects.get_or_create(discord_id=signup.discord_id,
                                          defaults={'name': signup.name, 'signup': False})
    player.signup = signup.signup
    player.save()
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ['name', 'side', 'url', 'faction']


class DeckList(generics.ListAPIView):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer


class TablePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['discord_id', 'name']

class TableDeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ['name', 'url']

class TableSerializer(serializers.ModelSerializer):
    player1 = TablePlayerSerializer(read_only=True)
    player2 = TablePlayerSerializer(read_only=True)
    player1_corp_deck = TableDeckSerializer(read_only=True)
    player1_runner_deck = TableDeckSerializer(read_only=True)
    player2_corp_deck = TableDeckSerializer(read_only=True)
    player2_runner_deck = TableDeckSerializer(read_only=True)
    class Meta:
        model = Table
        fields = ['player1', 'player2', 'player1_corp_deck', 'player1_runner_deck', 'player2_corp_deck', 'player2_runner_deck']


class TableList(generics.ListAPIView):
    serializer_class = TableSerializer

    def get_queryset(request):
        return Table.objects.filter(week=Week.objects.order_by('-start').first()).all()


