from ortools.linear_solver import pywraplp

runner_decks = (
"Bad Pub Kim",
"Caissa Reina",
"Eater Alice",
"Faust MaxX",
"Omar's Old Tricks",
"Plague Null",
"Central Leela",
"Ginge",
"Khan Birdies",
"Los HQ Drill",
"Sifting Fisk",
"Street Geist",
"Afro Akiko",
"Chameleon Hayley",
"Nasir's Workshop",
"Oracle OverExile",
"Smokeflash",
"Surfer Kit",
"Apex Toll the Hounds",
"Deva Adam",
"Sunny and the Rachelrabbit"
)

corp_decks = (
"An Architect's Brain",
"Genesis Stronger Together",
"Grail Foundry",
"Sel",
"Sportsmetal NEXT",
"Biotech Cloning",
"Glacier RP",
"Nisei Ambush",
"Saraswati Traps",
"The Palana Code",
"Acme JoyTag",
"News Tracer",
"Psychographics Hub",
"Spark Mad Men",
"Tricky Haarpsichord",
"Ambitious Outfit",
"Blue Barriers",
"Jemison Constellation",
"Meaty Builders",
"Punitive Argus",
"Sandburg Shadow",
)



def schedule_players(played):
    """
    Return a schedule of who should play who.

    @param played  the matrix of how many times a player has played another player
    """
    num_players = len(played) # todo: assuming even
    assert num_players % 2 == 0

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

def schedule_runner_deck(num_players, runner_played, global_played):
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
    # Minimize repeat decks
    objective_terms = []
    for i in range(num_decks):
        objective_terms.append(runner_played[i] * num_players * x[i])
    objective_terms2 = []
    for i in range(num_decks):
        objective_terms2.append(global_played[i] * x[i])
    solver.Minimize(solver.Sum(objective_terms) + solver.Sum(objective_terms2))

    # Solve
    status = solver.Solve()

    # Print solution.
    if not (status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE):
        raise 'could not solve decks'

    for i in range(num_decks):
        if x[i].solution_value() == 1:
            runner_deck = i

    return runner_deck

def schedule_corp_deck(num_players, corp_played, global_played, deck_matchups):
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
    # Minimize repeat decks
    objective_terms = []
    for i in range(num_decks):
        objective_terms.append(corp_played[i] * num_players * x[i])
    objective_terms2 = []
    for i in range(num_decks):
        objective_terms2.append(global_played[i] * x[i])
    objective_terms3 = []
    for i in range(num_decks):
        objective_terms3.append(deck_matchups[i] * x[i])
    solver.Minimize(solver.Sum(objective_terms) + solver.Sum(objective_terms2) + solver.Sum(objective_terms3))

    # Solve
    status = solver.Solve()

    # Print solution.
    if not (status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE):
        raise 'could not solve decks'

    for i in range(num_decks):
        if x[i].solution_value() == 1:
            corp_deck = i

    return corp_deck


def main():
    players = [
    'FatBuddha',
    'Furang',
    'njj',
    'Number Three',
    'rsh',
    'Semicolon42',
    'Shaz',
    'somomos',
    'Spraybizzle',
    'Tesseract',
    'Volitar',
    'Wandalfthegizard',
    'Zylyz',
    'K4RL',
    ]
    num_players = len(players)
    num_decks = 21
    played = [[0 for j in range(num_players)] for i in range(num_players)]
    deck_matchups = [[0 for _ in range(num_decks)] for _ in range(num_decks)]
    runner_costs = [[0 for _ in range(num_decks)] for _ in range(num_players)]
    corp_costs = [[0 for _ in range(num_decks)] for _ in range(num_players)]
    global_costs = [0 for _ in range(num_decks)]
    for j in range(20):
        print(f"round {j}")
        matchups = schedule_players(played)
        for i, opponent in enumerate(matchups):
            played[i][opponent] += 1
            runner_deck = schedule_runner_deck(num_players, runner_costs[i], global_costs)
            corp_deck = schedule_corp_deck(num_players, corp_costs[opponent], global_costs, deck_matchups[runner_deck])
            runner_costs[i][runner_deck] += 1
            corp_costs[opponent][corp_deck] += 1
            global_costs[runner_deck] += 1
            global_costs[corp_deck] += 1
            deck_matchups[runner_deck][corp_deck] += 1
            print(f"  {players[i]} vs {players[opponent]}")
            print(f"    {runner_decks[runner_deck]} vs {corp_decks[corp_deck]}")
    print(deck_matchups)



if __name__ == '__main__':
    main()
