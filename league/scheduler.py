from ortools.linear_solver import pywraplp
from django.db import connection
from django.db.models import Q
from pprint import pprint
from collections import defaultdict
import random

from .models import Player, Deck, Week, Table


def schedule_players(played):
    """
    Return a schedule of who should play who.

    @param played  the matrix of how many times a player has played another player
    """
    num_players = len(played) # todo: assuming even
    if num_players % 2 != 0:
        raise 'num_players must be even'

    # Solver
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # x[i, j] is an array of 0-1 variables, which will be 1
    # if player i is scheduled with player j.
    x = {}
    for i in range(num_players):
        for j in range(num_players):
            x[i, j] = solver.IntVar(0, 1, '')

    # Constraints
    # A player cannot play himself
    for i in range(num_players):
        solver.Add(x[i, i] == 0)
    # Players must be paired up
    for i in range(num_players):
        for j in range(num_players):
            solver.Add(x[i, j] == x[j, i])
    # A player can only play one other player
    for i in range(num_players):
        solver.Add(solver.Sum([x[i, j] for j in range(num_players)]) == 1)
    for j in range(num_players):
        solver.Add(solver.Sum([x[i, j] for i in range(num_players)]) == 1)

    # Objective
    # Minimize repeat matchups
    objective_terms = []
    for i in range(num_players):
        for j in range(num_players):
            objective_terms.append(played[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Solve
    status = solver.Solve()

    # Print solution.
    if not (status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE):
        raise 'could not solve schedule'

    matchups = [0 for _ in range(num_players)]
    for i in range(num_players):
        for j in range(num_players):
            if x[i, j].solution_value() == 1:
                matchups[i] = j
    return matchups


def schedule_runner_deck(num_players, runner_played, corp_vs_costs, global_played):
    num_decks = len(runner_played)

    # Solver
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # x[i] will be set to 1 if playing that runner deck
    x = [solver.IntVar(0, 1, '') for i in range(num_decks)]

    # Constraints
    # players can only play one deck
    solver.Add(solver.Sum(x) == 1)

    # Objective
    # Top priority: minimize a player playing a repeat deck
    objective_terms = []
    for i in range(num_decks):
        objective_terms.append(runner_played[i] * num_players * x[i])
    # Second priority: minimize a player playing against a repeat deck
    objective_terms3 = []
    for i in range(num_decks):
        objective_terms3.append(corp_vs_costs[i] * num_players / 3 * x[i])
    # Last priority: minimize repeat decks across all players
    objective_terms2 = []
    for i in range(num_decks):
        objective_terms2.append(global_played[i] * x[i])
    solver.Minimize(solver.Sum(objective_terms) + solver.Sum(objective_terms2) + solver.Sum(objective_terms3))

    # Solve
    status = solver.Solve()

    # Print solution.
    if not (status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE):
        raise 'could not solve decks'

    for i in range(num_decks):
        if x[i].solution_value() == 1:
            runner_deck = i

    return runner_deck


def schedule_corp_deck(num_players, corp_played, runner_vs_costs, global_played, deck_matchups):
    num_decks = len(corp_played)

    # Solver
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # x[i] will be set to 1 if playing that runner deck
    x = [solver.IntVar(0, 1, '') for i in range(num_decks)]

    # Constraints
    # players can only play one deck
    solver.Add(solver.Sum(x) == 1)

    # Objective
    # Top priority: minimize a player playing a repeat deck
    objective_terms = []
    for i in range(num_decks):
        objective_terms.append(corp_played[i] * num_players * x[i])
    # Second priority: minimize a player playing against a repeat deck
    objective_terms4 = []
    for i in range(num_decks):
        objective_terms4.append(runner_vs_costs[i] * num_players / 3 * x[i])
    # Last priority: minimize repeat decks across all players
    objective_terms2 = []
    for i in range(num_decks):
        objective_terms2.append(global_played[i] * x[i])
    # Last priority: minimize repeat decks matchups
    objective_terms3 = []
    for i in range(num_decks):
        objective_terms3.append(deck_matchups[i] * x[i])
    solver.Minimize(solver.Sum(objective_terms) + solver.Sum(objective_terms2) + solver.Sum(objective_terms3) + solver.Sum(objective_terms4))

    # Solve
    status = solver.Solve()

    # Print solution.
    if not (status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE):
        raise 'could not solve decks'

    for i in range(num_decks):
        if x[i].solution_value() == 1:
            corp_deck = i

    return corp_deck


def create_matchups():
    signed_up_players = list(Player.objects.filter(signup=True).all())
    num_players = len(signed_up_players)
    # make sure even
    if num_players % 2 != 0:
        signed_up_players = [p for p in signed_up_players if p.name != 'njj']
        num_players -= 1
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



