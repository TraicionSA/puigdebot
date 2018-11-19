import discord
import asyncio
import random
from random import randint
import time
import json
import os
import psycopg2
from psycopg2.extensions import AsIs
import requests
import mimetypes
import datetime
from time import sleep

# INFORMATION:
# SERVER.ID: '188966409672458241'
# SERVER.NAME: 'VANDALPC'

client = discord.Client()
global bot_status
bot_status = False
bot_analisis = False


@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='cocks.exe'))


@client.event
async def on_message(message):
    if message.content.startswith('.gif') or message.content.startswith('.tag'):
      await client.send_message(message.channel, ':octagonal_sign:NO ENCUENTRA EL GIF QUE BUSCAS:octagonal_sign:')

#RUN
client.run(os.environ.get('BOT_TOKEN'))
