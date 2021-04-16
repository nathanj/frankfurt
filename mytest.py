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
