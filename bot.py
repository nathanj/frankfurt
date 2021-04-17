import os
import discord
import random
import requests
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client}')


def get_decks():
    return requests.get('http://localhost:8000/api/decks/').json()


async def display_help(message):
    await message.channel.send("""
```Hi, I'm the Frankfurt Bot. My commands are:

!help        Display this help
!pickdecks   Pick a random corp and runner deck matchup
!fr-signup   Sign up for the Frankfurt casual league
!fr-drop     Drop out of the Frankfurt casual league```""".strip())


async def pick_decks(message):
    decks = get_decks()
    runner = random.choice([d for d in decks if d['side'] == 'runner'])
    corp = random.choice([d for d in decks if d['side'] == 'corp'])
    if random.randint(0, 1) == 1:
        embed = discord.Embed(description=f"[{runner['name']}]({runner['url']}) vs [{corp['name']}]({corp['url']})")
    else:
        embed = discord.Embed(description=f"[{corp['name']}]({corp['url']}) vs [{runner['name']}]({runner['url']})")
    await message.channel.send(embed=embed)


async def do_signup(message, json):
    async with aiohttp.ClientSession(headers={'Authorization': os.environ['API_KEY']}) as session:
        async with session.post('http://localhost:8000/api/signup', json=json) as response:
            if response.status == 200:
                await message.add_reaction('✔️')
            else:
                await message.add_reaction('❌')
                print('status = ', response.status)
                print(await response.text())


async def signup(message):
    json = {'discord_id': message.author.id,
            'name': message.author.name,
            'signup': True,
            }
    await do_signup(message, json)


async def drop(message):
    json = {'discord_id': message.author.id,
            'name': message.author.name,
            'signup': False,
            }
    await do_signup(message, json)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('-help') or message.content.startswith('!help'):
        await display_help(message)
    elif message.content.startswith('-pickdecks') or message.content.startswith('!pickdecks'):
        await pick_decks(message)
    elif message.content.startswith('-fr-signup') or message.content.startswith('!fr-signup'):
        await signup(message)
    elif message.content.startswith('-fr-drop') or message.content.startswith('!fr-drop'):
        await drop(message)


client.run(os.environ['DISCORD_KEY'])
