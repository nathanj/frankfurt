from django.db import connection
from django.db.models import Q
from pprint import pprint
from collections import defaultdict
from mytest import schedule_players, schedule_runner_deck, schedule_corp_deck
import random

from .models import Player, Deck, Week, Table


def create_matchups():
    signed_up_players = list(Player.objects.filter(signup=True).all())
    num_players = len(signed_up_players)
    matches = list(Table.objects.select_related().all())
    corp_decks = list(Deck.objects.filter(side='corp').all())
    runner_decks = list(Deck.objects.filter(side='runner').all())

    # shuffle otherwise it tends to assign in alphabetical order
    random.shuffle(corp_decks)
    random.shuffle(runner_decks)

    num_decks = len(corp_decks)

    played = []
    for p in signed_up_players:
        played.append([])
        for p2 in signed_up_players:
            played[-1].append(Table.objects.filter((Q(player1=p) & Q(player2=p2)) | (Q(player1=p2) & Q(player2=p))).count())

    # create the big list of costs
    runner_costs = [[0 for _ in range(num_decks)] for _ in range(num_players)]
    runner_vs_costs = [[0 for _ in range(num_decks)] for _ in range(num_players)]
    corp_costs = [[0 for _ in range(num_decks)] for _ in range(num_players)]
    corp_vs_costs = [[0 for _ in range(num_decks)] for _ in range(num_players)]
    global_runner_costs = [0 for _ in range(num_decks)]
    global_corp_costs = [0 for _ in range(num_decks)]
    deck_matchups = [[0 for _ in range(num_decks)] for _ in range(num_decks)]
    for m in matches:
        player1_id = signed_up_players.index(m.player1)
        player2_id = signed_up_players.index(m.player2)
        player1_corp_deck_id = corp_decks.index(m.player1_corp_deck)
        player1_runner_deck_id = runner_decks.index(m.player1_runner_deck)
        player2_corp_deck_id = corp_decks.index(m.player2_corp_deck)
        player2_runner_deck_id = runner_decks.index(m.player2_runner_deck)
        deck_matchups[player1_corp_deck_id][player2_runner_deck_id] += 1
        deck_matchups[player2_corp_deck_id][player1_runner_deck_id] += 1
        global_corp_costs[player1_corp_deck_id] += 1
        global_corp_costs[player2_corp_deck_id] += 1
        global_runner_costs[player1_runner_deck_id] += 1
        global_runner_costs[player2_runner_deck_id] += 1
        runner_costs[player1_id][player1_runner_deck_id] += 1
        runner_vs_costs[player1_id][player2_corp_deck_id] += 1
        runner_costs[player2_id][player2_runner_deck_id] += 1
        runner_vs_costs[player2_id][player1_corp_deck_id] += 1
        corp_costs[player1_id][player1_corp_deck_id] += 1
        corp_vs_costs[player1_id][player2_runner_deck_id] += 1
        corp_costs[player2_id][player2_corp_deck_id] += 1
        corp_vs_costs[player2_id][player1_runner_deck_id] += 1

    matchups = schedule_players(played)
    matchups2 = []
    seen = []
    for i, m in enumerate(matchups):
        if i in seen:
            continue
        seen.append(i)
        seen.append(m)
        matchups2.append( [signed_up_players[i], signed_up_players[m]] )

    for m in matchups2:
        player1_id = signed_up_players.index(m[0])
        player2_id = signed_up_players.index(m[1])

        runner_deck = schedule_runner_deck(num_players, runner_costs[player1_id], corp_vs_costs[player2_id], global_runner_costs)
        corp_deck = schedule_corp_deck(num_players, corp_costs[player2_id], runner_vs_costs[player1_id], global_corp_costs, deck_matchups[runner_deck])
        m.append(runner_decks[runner_deck])
        m.append(corp_decks[corp_deck])
        runner_costs[player1_id][runner_deck] += 1
        runner_vs_costs[player1_id][corp_deck] += 1
        corp_costs[player2_id][corp_deck] += 1
        corp_vs_costs[player2_id][runner_deck] += 1
        global_runner_costs[runner_deck] += 1
        global_corp_costs[corp_deck] += 1
        deck_matchups[runner_deck][corp_deck] += 1

        runner_deck = schedule_runner_deck(num_players, runner_costs[player2_id], corp_vs_costs[player1_id], global_runner_costs)
        corp_deck = schedule_corp_deck(num_players, corp_costs[player1_id], runner_vs_costs[player2_id], global_corp_costs, deck_matchups[runner_deck])
        m.append(runner_decks[runner_deck])
        m.append(corp_decks[corp_deck])
        runner_costs[player2_id][runner_deck] += 1
        runner_vs_costs[player2_id][corp_deck] += 1
        corp_costs[player1_id][corp_deck] += 1
        corp_vs_costs[player1_id][runner_deck] += 1
        global_runner_costs[runner_deck] += 1
        global_corp_costs[corp_deck] += 1
        deck_matchups[runner_deck][corp_deck] += 1

    return matchups2



