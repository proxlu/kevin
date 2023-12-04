#!/bin/python3
# -*- coding: utf-8 -*- 
import re
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard
import requests
import discord

# Remover menção ao bot
def remover_mencoes(message, texto):
  for mencionado in message.mentions:
    if mencionado.bot:
      texto = texto.replace(f'<@{mencionado.id}>', '')
  return texto

# carrega as chaves em config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Carregamento
intents = discord.Intents.default()
intents.messages = True  # Habilita a intenção de mensagens de guilda
client = discord.Client(intents=intents)

# Token da sessão do Bard
token = config['tokens']['bard_token']

# Requisição dos cabeçalhos/cookies
session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.set('__Secure-1PSID', token)
session.cookies.set('__Secure-1PSIDTS', '<VALUE>')
session.cookies.set('__Secure-1PSIDCC', '<VALUE>')

# Bot
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  canal = message.channel
  texto = remover_mencoes(message, message.content)  # Remove as menções de bots

  # Estrutura principal
  if texto:

    # Splash de carregamento
    splash = await canal.send(':hourglass:')

    # Solicita a api
    bard = Bard(token=token, session=session)
    resposta_api = bard.get_answer(texto)

    # Trata a resposta da API
    if isinstance(resposta_api, str):
      saida_da_api = resposta_api
    else:
      saida_da_api = resposta_api['content']

    # Recebe a mensagem do usuário
    await splash.delete()
    while saida_da_api != '':
      await canal.send(saida_da_api[:2000])
      saida_da_api = saida_da_api[2000:]

client.run(config['tokens']['discord_token'])
