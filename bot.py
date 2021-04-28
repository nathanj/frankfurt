import os
import discord
import random
import requests
import aiohttp
import asyncio
import datetime
import textwrap
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client}')


async def get_decks():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/api/decks') as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(await response.text())


async def display_help(message):
    await message.channel.send("""
```Hi, I'm the Frankfurt Bot. My commands are:

!help        Display this help
!pickdecks   Pick a random corp and runner deck matchup
!signup      Sign up for the Frankfurt casual league
!drop        Drop out of the Frankfurt casual league

You can either post the command in this channel or message me directly.```""".strip())


def deck_with_url(deck):
    return f"[{deck['name']}]({deck['url']})"


async def pick_decks(message):
    decks = await get_decks()
    runner = random.choice([d for d in decks if d['side'] == 'runner'])
    corp = random.choice([d for d in decks if d['side'] == 'corp'])
    if random.randint(0, 1) == 1:
        embed = discord.Embed(description=f"{deck_with_url(runner)} vs {deck_with_url(corp)}")
    else:
        embed = discord.Embed(description=f"{deck_with_url(corp)} vs {deck_with_url(runner)}")
    await message.channel.send(embed=embed)


async def do_signup(message, json):
    async with aiohttp.ClientSession(headers={'Authorization': os.environ['API_KEY']}) as session:
        async with session.post('http://localhost:8000/api/signup', json=json) as response:
            if response.status == 200:
                if json['signup']:
                    await message.add_reaction('🏃')
                else:
                    await message.add_reaction('🗑️')
            else:
                await message.add_reaction('❌')
                print('status = ', response.status)
                print(await response.text())


async def signup(message):
    json = {'discord_id': message.author.id,
            'name': message.author.name,
            'signup': True,
            }
    print('signing up ', json)
    await do_signup(message, json)


async def drop(message):
    json = {'discord_id': message.author.id,
            'name': message.author.name,
            'signup': False,
            }
    print('dropping out ', json)
    await do_signup(message, json)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('-help') or message.content.startswith('!help'):
        await display_help(message)
    elif message.content.startswith('-pickdecks') or message.content.startswith('!pickdecks'):
        await pick_decks(message)
    elif message.content.startswith('-signup') or message.content.startswith('!signup'):
        await signup(message)
    elif message.content.startswith('-drop') or message.content.startswith('!drop'):
        await drop(message)
    elif message.content.startswith('-dropout') or message.content.startswith('!dropout'):
        await drop(message)

async def weekly_match_generator():
    while True:
        now = datetime.datetime.now()
        monday_10am = now.replace(hour=10, minute=0, second=0, microsecond=0)
        while monday_10am.weekday() != 0 or monday_10am < now:
            monday_10am += datetime.timedelta(days=1)
        delta = monday_10am - now
        print('generating matches in ', delta)
        await asyncio.sleep(delta.total_seconds())
        print('generating matches')
        channel = client.get_channel(int(os.environ['DISCORD_CHANNEL']))
        async with aiohttp.ClientSession(headers={'Authorization': os.environ['API_KEY']}) as session:
            async with session.post('http://localhost:8000/api/generate') as response:
                if response.status == 200:
                    print('getting tables')
                    async with session.get('http://localhost:8000/api/tables') as response:
                        if response.status == 200:
                            await channel.send(embed=discord.Embed(description=textwrap.dedent(f"""\
                            **League matchups have been generated for the week of {monday_10am.strftime("%B %-e")}**.
                            You should have received a DM from me with your match if you were signed up. You can also view the matchups on the [Frankfurt League Website](https://frankfurt.bitcrafter.net).
                            As a reminder, you can always signup or dropout for next week by sending me `!signup` or `!drop`.""")))
                            tables = await response.json()
                            for table in tables:
                                player1_id = table['player1']['discord_id']
                                player1_name = table['player1']['name']
                                player2_id = table['player2']['discord_id']
                                player2_name = table['player2']['name']
                                p1_corp = table['player1_corp_deck']
                                p2_corp = table['player2_corp_deck']
                                p1_runner = table['player1_runner_deck']
                                p2_runner = table['player2_runner_deck']
                                content = f"Your Frankfurt match this week:"
                                embed = discord.Embed(description=textwrap.dedent(f"""\
                                        ({player1_name}) {deck_with_url(p1_corp)} vs {deck_with_url(p2_runner)} ({player2_name})
                                        ({player1_name}) {deck_with_url(p1_runner)} vs {deck_with_url(p2_corp)} ({player2_name})"""))
                                try:
                                    print(f'sending msg to {player1_name} ({player1_id})')
                                    user = await client.fetch_user(int(player1_id))
                                    await user.send(content=content, embed=embed)
                                except Exception as ex:
                                    print(ex)
                                try:
                                    print(f'sending msg to {player2_name} ({player2_id})')
                                    user = await client.fetch_user(int(player2_id))
                                    await user.send(content=content, embed=embed)
                                except Exception as ex:
                                    print(ex)
                        else:
                            raise Exception(await response.text())
                else:
                    raise Exception(await response.text())
        await asyncio.sleep(60)

client.loop.create_task(weekly_match_generator())
client.run(os.environ['DISCORD_KEY'])
