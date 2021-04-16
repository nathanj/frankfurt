import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from league.models import *

runner_decks = (
["Afro Akiko", "https://netrunnerdb.com/en/decklist/64245/-frankfurt-collection-afro-akiko-v1-0", 'shaper', 'akiko.jpg'],
["Apex Toll the Hounds", "https://netrunnerdb.com/en/decklist/64239/-frankfurt-collection-apex-toll-the-hounds-v1-0", 'apex', 'apex.jpg'],
["Bad Pub Kim", "https://netrunnerdb.com/en/decklist/64257/-frankfurt-collection-bad-pub-kim-v1-0", 'anarch', 'kim.jpg'],
["Caissa Reina", "https://netrunnerdb.com/en/decklist/64256/-frankfurt-collection-caissa-reina-v1-0", 'anarch', 'reina.jpg'],
["Central Leela", "https://netrunnerdb.com/en/decklist/64251/-frankfurt-collection-central-leela-v1-0", 'criminal', 'leela.jpg'],
["Chameleon Hayley", "https://netrunnerdb.com/en/decklist/64244/-frankfurt-collection-chameleon-hayley-v1-0", 'shaper', 'hayley.jpg'],
["Deva Adam", "https://netrunnerdb.com/en/decklist/64238/-frankfurt-collection-deva-adam-v1-0", 'adam', 'adam.jpg'],
["Eater Alice", "https://netrunnerdb.com/en/decklist/64255/-frankfurt-collection-eater-alice-v1-0", 'anarch', 'alice.jpg'],
["Faust MaxX", "https://netrunnerdb.com/en/decklist/64254/-frankfurt-collection-faust-maxx-v1-0", 'anarch', 'maxx.jpg'],
["Ginger-Revior Andy", "https://netrunnerdb.com/en/decklist/64250/-frankfurt-collection-ginger-revoir-andy-v1-0", 'criminal', 'andy.jpg'],
["Khan Birdies", "https://netrunnerdb.com/en/decklist/64249/-frankfurt-collection-khan-birdies-v1-0", 'criminal', 'khan.jpg'],
["Los HQ Drill", "https://netrunnerdb.com/en/decklist/64248/-frankfurt-collection-los-hq-drill-v1-0", 'criminal', 'los.jpg'],
["Nasir's Workshop", "https://netrunnerdb.com/en/decklist/64243/-frankfurt-collection-nasir-s-workshop-v1-0", 'shaper', 'nasir.jpg'],
["Omar's Old Tricks", "https://netrunnerdb.com/en/decklist/64253/-frankfurt-collection-omar-s-old-tricks-v1-0", 'anarch', 'omar.jpg'],
["Oracle OverExile", "https://netrunnerdb.com/en/decklist/64242/-frankfurt-collection-oracle-overexile-v1-0", 'shaper', 'exile.jpg'],
["Plague Null", "https://netrunnerdb.com/en/decklist/64252/-frankfurt-collection-plague-null-v1-0", 'anarch', 'null.jpg'],
["Sifting Fisk", "https://netrunnerdb.com/en/decklist/64247/-frankfurt-collection-sifting-fisk-v1-0", 'criminal', 'fisk.jpg'],
["Smokeflash", "https://netrunnerdb.com/en/decklist/64241/-frankfurt-collection-smokeflash-v1-0", 'shaper', 'smoke.jpg'],
["Street Geist", "https://netrunnerdb.com/en/decklist/64246/-frankfurt-collection-street-geist-v1-0", 'criminal', 'geist.jpg'],
["Sunny and the Rachelrabbit", "https://netrunnerdb.com/en/decklist/64237/-frankfurt-collection-sunny-and-the-rachelrabbit-v1-0", 'sunny', 'sunny.jpg'],
["Surfer Kit", "https://netrunnerdb.com/en/decklist/64240/-frankfurt-collection-surfer-kit-v1-0", 'shaper', 'kit.jpg'],
)

corp_decks = (
["Acme JoyTag", "https://netrunnerdb.com/en/decklist/64226/-frankfurt-collection-acme-joytag-v1-0", 'nbn', 'acme.jpg'],
["Ambitious Outfit", "https://netrunnerdb.com/en/decklist/64221/-frankfurt-collection-ambitious-outfit-v1-0", 'weyland', 'outfit.jpg'],
["An Architect's Brain", "https://netrunnerdb.com/en/decklist/64236/-frankfurt-collection-an-architect-s-brain-v1-0", 'hb', 'architects.jpg'],
["Biotech Cloning", "https://netrunnerdb.com/en/decklist/64231/-frankfurt-collection-biotech-cloning-v1-0", 'jinteki', 'biotech.jpg'],
["Blue Barriers", "https://netrunnerdb.com/en/decklist/64220/-frankfurt-collection-blue-barriers-v1-0", 'weyland', 'blue.jpg'],
["Genesis Stronger Together", "https://netrunnerdb.com/en/decklist/64235/-frankfurt-collection-genesis-stronger-together-v1-0", 'hb', 'stronger.jpg'],
["Glacier RP", "https://netrunnerdb.com/en/decklist/64230/-frankfurt-collection-glacier-rp-v1-0", 'jinteki', 'rp.jpg'],
["Grail Foundry", "https://netrunnerdb.com/en/decklist/64234/-frankfurt-collection-grail-foundry-v1-0", 'hb', 'foundry.jpg'],
["Jemison Constellation", "https://netrunnerdb.com/en/decklist/64219/-frankfurt-collection-jemison-constellation-v1-0", 'weyland', 'jemison.jpg'],
["Meaty Builders", "https://netrunnerdb.com/en/decklist/64199/-frankfurt-collection-meaty-builders-v1-0", 'weyland', 'builder.jpg'],
["News Tracer", "https://netrunnerdb.com/en/decklist/64225/-frankfurt-collection-news-tracer-v1-0", 'nbn', 'news.jpg'],
["Nisei Ambush", "https://netrunnerdb.com/en/decklist/64229/-frankfurt-collection-nisei-ambush-v1-0", 'jinteki', 'nisei.jpg'],
["Psychographics Hub", "https://netrunnerdb.com/en/decklist/64224/-frankfurt-collection-psychographics-hub-v1-0", 'nbn', 'nearearthhub.jpg'],
["Punitive Argus", "https://netrunnerdb.com/en/decklist/64198/-frankfurt-collection-punitive-argus-v1-0", 'weyland', 'argus.jpg'],
["Sandburg Shadow", "https://netrunnerdb.com/en/decklist/64197/-frankfurt-collection-sandburg-shadow-v1-0", 'neutral', 'shadow.jpg'],
["Saraswati Traps", "https://netrunnerdb.com/en/decklist/64228/-frankfurt-collection-saraswati-traps-v1-0", 'jinteki', 'saraswati.jpg'],
["Self-Destruct Division", "https://netrunnerdb.com/en/decklist/64233/-frankfurt-collection-self-destruct-division-v1-0", 'hb', 'cybernetics.jpg'],
["Spark Mad Men", "https://netrunnerdb.com/en/decklist/64223/-frankfurt-collection-spark-mad-men-v1-0", 'nbn', 'spark.jpg'],
["Sportsmetal NEXT", "https://netrunnerdb.com/en/decklist/64232/-frankfurt-collection-sportsmetal-next-v1-0", 'hb', 'sportsmetal.jpg'],
["The Palana Code", "https://netrunnerdb.com/en/decklist/64227/-frankfurt-collection-the-palana-code-v1-0", 'jinteki', 'palana.jpg'],
["Tricky Haarpsichord", "https://netrunnerdb.com/en/decklist/64222/-frankfurt-collection-tricky-haarpsichord-v1-0", 'nbn', 'haarpsichord.jpg'],
)

class Command(BaseCommand):
    help = 'Seed the database'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        for d in runner_decks:
            Deck(name=d[0], side='runner', url=d[1], faction=d[2], image_url=d[3]).save()
        for d in corp_decks:
            Deck(name=d[0], side='corp', url=d[1], faction=d[2], image_url=d[3]).save()

        User.objects.create_superuser(username='admin', password='admin').save()

        Player(discord_id=125, signup=True, name='njj').save()
        Player(discord_id=123, signup=True, name='FatBuddha').save()
        Player(discord_id=124, signup=True, name='Furang').save()
        Player(discord_id=126, signup=True, name='Number Three').save()
        Player(discord_id=127, signup=True, name='rsh').save()
        Player(discord_id=128, signup=True, name='Semicolon42').save()
        Player(discord_id=129, signup=True, name='Shaz').save()
        Player(discord_id=133, signup=True, name='somomos').save()
        Player(discord_id=134, signup=True, name='Spraybizzle').save()
        Player(discord_id=135, signup=True, name='Tesseract').save()
        Player(discord_id=136, signup=True, name='Volitar').save()
        Player(discord_id=137, signup=True, name='Wandalfthegizard').save()
        Player(discord_id=138, signup=True, name='Zylyz').save()
        Player(discord_id=139, signup=True, name='K4RL').save()

        today = datetime.datetime.today().date()
        while today.weekday() != 0:
            today += datetime.timedelta(days=1)

        w = Week(start=today)
        w.save()

        #t = Table(number=1, week=w, player1=Player.objects.filter(name='njj').first(), player2=Player.objects.filter(name='rsh').first())
        #t.save()
        #t2 = Table(number=2, week=w, player1=Player.objects.filter(name='somomos').first(), player2=Player.objects.filter(name='Spraybizzle').first())
        #t2.save()
        #t3 = Table(number=2, week=w, player1=Player.objects.filter(name='Volitar').first(), player2=Player.objects.filter(name='Semicolon42').first())
        #t3.save()
        #t4 = Table(number=2, week=w, player1=Player.objects.filter(name='Furang').first(), player2=Player.objects.filter(name='Shaz').first())
        #t4.save()
        #t5 = Table(number=2, week=w, player1=Player.objects.filter(name='Tesseract').first(), player2=Player.objects.filter(name='FatBuddha').first())
        #t5.save()

        #Match(table=t,
        #    corp_player=Player.objects.filter(name='njj').first(),
        #    corp_deck=Deck.objects.filter(name='An Architect\'s Brain').first(),
        #    runner_player=Player.objects.filter(name='rsh').first(),
        #    runner_deck=Deck.objects.filter(name='Eater Alice').first()).save()
        #Match(table=t,
        #    corp_player=Player.objects.filter(name='rsh').first(),
        #    corp_deck=Deck.objects.filter(name='Blue Barriers').first(),
        #    runner_player=Player.objects.filter(name='njj').first(),
        #    runner_deck=Deck.objects.filter(name='Oracle OverExile').first()).save()
        #Match(table=t2,
        #    corp_player=Player.objects.filter(name='somomos').first(),
        #    corp_deck=Deck.objects.filter(name='Acme JoyTag').first(),
        #    runner_player=Player.objects.filter(name='Spraybizzle').first(),
        #    runner_deck=Deck.objects.filter(name='Afro Akiko').first()).save()
        #Match(table=t2,
        #    corp_player=Player.objects.filter(name='Spraybizzle').first(),
        #    corp_deck=Deck.objects.filter(name='Ambitious Outfit').first(),
        #    runner_player=Player.objects.filter(name='somomos').first(),
        #    runner_deck=Deck.objects.filter(name='Sifting Fisk').first()).save()
        #Match(table=t3,
        #    corp_player=Player.objects.filter(name='Volitar').first(),
        #    corp_deck=Deck.objects.filter(name='Grail Foundry').first(),
        #    runner_player=Player.objects.filter(name='Semicolon42').first(),
        #    runner_deck=Deck.objects.filter(name='Deva Adam').first()).save()
        #Match(table=t3,
        #    corp_player=Player.objects.filter(name='Semicolon42').first(),
        #    corp_deck=Deck.objects.filter(name='Meaty Builders').first(),
        #    runner_player=Player.objects.filter(name='Volitar').first(),
        #    runner_deck=Deck.objects.filter(name='Surfer Kit').first()).save()
        #Match(table=t4,
        #    corp_player=Player.objects.filter(name='Furang').first(),
        #    corp_deck=Deck.objects.filter(name='Tricky Haarpsichord').first(),
        #    runner_player=Player.objects.filter(name='Shaz').first(),
        #    runner_deck=Deck.objects.filter(name='Bad Pub Kim').first()).save()
        #Match(table=t4,
        #    corp_player=Player.objects.filter(name='Shaz').first(),
        #    corp_deck=Deck.objects.filter(name='Blue Barriers').first(),
        #    runner_player=Player.objects.filter(name='Furang').first(),
        #    runner_deck=Deck.objects.filter(name='Los HQ Drill').first()).save()
        #Match(table=t5,
        #    corp_player=Player.objects.filter(name='Tesseract').first(),
        #    corp_deck=Deck.objects.filter(name='Biotech Cloning').first(),
        #    runner_player=Player.objects.filter(name='FatBuddha').first(),
        #    runner_deck=Deck.objects.filter(name='Nasir\'s Workshop').first()).save()
        #Match(table=t5,
        #    corp_player=Player.objects.filter(name='FatBuddha').first(),
        #    corp_deck=Deck.objects.filter(name='Jemison Constellation').first(),
        #    runner_player=Player.objects.filter(name='Tesseract').first(),
        #    runner_deck=Deck.objects.filter(name='Omar\'s Old Tricks').first()).save()

        self.stdout.write(self.style.SUCCESS('Seeded database'))
