import os
import discord
import random

runner_decks = (
["Bad Pub Kim", "https://netrunnerdb.com/en/decklist/64257/-frankfurt-collection-bad-pub-kim-v1-0"],
["Caissa Reina", "https://netrunnerdb.com/en/decklist/64256/-frankfurt-collection-caissa-reina-v1-0"],
["Eater Alice", "https://netrunnerdb.com/en/decklist/64255/-frankfurt-collection-eater-alice-v1-0"],
["Faust MaxX", "https://netrunnerdb.com/en/decklist/64254/-frankfurt-collection-faust-maxx-v1-0"],
["Omar's Old Tricks", "https://netrunnerdb.com/en/decklist/64253/-frankfurt-collection-omar-s-old-tricks-v1-0"],
["Plague Null", "https://netrunnerdb.com/en/decklist/64252/-frankfurt-collection-plague-null-v1-0"],
["Central Leela", "https://netrunnerdb.com/en/decklist/64251/-frankfurt-collection-central-leela-v1-0"],
["Ginger-Revior Andy", "https://netrunnerdb.com/en/decklist/64250/-frankfurt-collection-ginger-revoir-andy-v1-0"],
["Khan Birdies", "https://netrunnerdb.com/en/decklist/64249/-frankfurt-collection-khan-birdies-v1-0"],
["Los HQ Drill", "https://netrunnerdb.com/en/decklist/64248/-frankfurt-collection-los-hq-drill-v1-0"],
["Sifting Fisk", "https://netrunnerdb.com/en/decklist/64247/-frankfurt-collection-sifting-fisk-v1-0"],
["Street Geist", "https://netrunnerdb.com/en/decklist/64246/-frankfurt-collection-street-geist-v1-0"],
["Afro Akiko", "https://netrunnerdb.com/en/decklist/64245/-frankfurt-collection-afro-akiko-v1-0"],
["Chameleon Hayley", "https://netrunnerdb.com/en/decklist/64244/-frankfurt-collection-chameleon-hayley-v1-0"],
["Nasir's Workshop", "https://netrunnerdb.com/en/decklist/64243/-frankfurt-collection-nasir-s-workshop-v1-0"],
["Oracle OverExile", "https://netrunnerdb.com/en/decklist/64242/-frankfurt-collection-oracle-overexile-v1-0"],
["Smokeflash", "https://netrunnerdb.com/en/decklist/64241/-frankfurt-collection-smokeflash-v1-0"],
["Surfer Kit", "https://netrunnerdb.com/en/decklist/64240/-frankfurt-collection-surfer-kit-v1-0"],
["Apex Toll the Hounds", "https://netrunnerdb.com/en/decklist/64239/-frankfurt-collection-apex-toll-the-hounds-v1-0"],
["Deva Adam", "https://netrunnerdb.com/en/decklist/64238/-frankfurt-collection-deva-adam-v1-0"],
["Sunny and the Rachelrabbit", "https://netrunnerdb.com/en/decklist/64237/-frankfurt-collection-sunny-and-the-rachelrabbit-v1-0"],
)

corp_decks = (
["An Architect's Brain", "https://netrunnerdb.com/en/decklist/64236/-frankfurt-collection-an-architect-s-brain-v1-0"],
["Genesis Stronger Together", "https://netrunnerdb.com/en/decklist/64235/-frankfurt-collection-genesis-stronger-together-v1-0"],
["Grail Foundry", "https://netrunnerdb.com/en/decklist/64234/-frankfurt-collection-grail-foundry-v1-0"],
["Self-destruct Division", "https://netrunnerdb.com/en/decklist/64233/-frankfurt-collection-self-destruct-division-v1-0"],
["Sportsmetal NEXT", "https://netrunnerdb.com/en/decklist/64232/-frankfurt-collection-sportsmetal-next-v1-0"],
["Biotech Cloning", "https://netrunnerdb.com/en/decklist/64231/-frankfurt-collection-biotech-cloning-v1-0"],
["Glacier RP", "https://netrunnerdb.com/en/decklist/64230/-frankfurt-collection-glacier-rp-v1-0"],
["Nisei Ambush", "https://netrunnerdb.com/en/decklist/64229/-frankfurt-collection-nisei-ambush-v1-0"],
["Saraswati Traps", "https://netrunnerdb.com/en/decklist/64228/-frankfurt-collection-saraswati-traps-v1-0"],
["The Palana Code", "https://netrunnerdb.com/en/decklist/64227/-frankfurt-collection-the-palana-code-v1-0"],
["Acme JoyTag", "https://netrunnerdb.com/en/decklist/64226/-frankfurt-collection-acme-joytag-v1-0"],
["News Tracer", "https://netrunnerdb.com/en/decklist/64225/-frankfurt-collection-news-tracer-v1-0"],
["Psychographics Hub", "https://netrunnerdb.com/en/decklist/64224/-frankfurt-collection-psychographics-hub-v1-0"],
["Spark Mad Men", "https://netrunnerdb.com/en/decklist/64223/-frankfurt-collection-spark-mad-men-v1-0"],
["Tricky Haarpsichord", "https://netrunnerdb.com/en/decklist/64222/-frankfurt-collection-tricky-haarpsichord-v1-0"],
["Ambitious Outfit", "https://netrunnerdb.com/en/decklist/64221/-frankfurt-collection-ambitious-outfit-v1-0"],
["Blue Barriers", "https://netrunnerdb.com/en/decklist/64220/-frankfurt-collection-blue-barriers-v1-0"],
["Jemison Constellation", "https://netrunnerdb.com/en/decklist/64219/-frankfurt-collection-jemison-constellation-v1-0"],
["Meaty Builders", "https://netrunnerdb.com/en/decklist/64199/-frankfurt-collection-meaty-builders-v1-0"],
["Punitive Argus", "https://netrunnerdb.com/en/decklist/64198/-frankfurt-collection-punitive-argus-v1-0"],
["Sandburg Shadow", "https://netrunnerdb.com/en/decklist/64197/-frankfurt-collection-sandburg-shadow-v1-0"],
)


client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('-pickdecks') or message.content.startswith('!pickdecks'):
        runner = random.choice(runner_decks)
        corp = random.choice(corp_decks)
        if random.randint(0, 1) == 1:
            embed = discord.Embed(description=f"[{runner[0]}]({runner[1]}) vs [{corp[0]}]({corp[1]})")
        else:
            embed = discord.Embed(description=f"[{corp[0]}]({corp[1]}) vs [{runner[0]}]({runner[1]})")
        await message.channel.send(embed=embed)

client.run(os.environ['DISCORD_KEY'])
