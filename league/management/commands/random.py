import random
from django.core.management.base import BaseCommand

from league.models import Deck

class Command(BaseCommand):
    help = 'Random deck'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        corp_decks = Deck.objects.filter(side='corp')
        runner_decks = Deck.objects.filter(side='runner')
        runner = runner_decks[random.randint(0, len(runner_decks)-1)]
        corp = corp_decks[random.randint(0, len(corp_decks)-1)]
        if random.randint(0, 1) == 0:
            print(f"{runner} vs {corp}")
        else:
            print(f"{corp} vs {runner}")
