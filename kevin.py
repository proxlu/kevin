#!/bin/python3
# -*- coding: utf-8 -*-
#
# kevin.py - by:proxlu
import re
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard
import requests
import discord
import asyncio
import json

# Carregamento
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Token da sessão do Bard
token = config['tokens']['bard_token']

# Requisição dos cabeçalhos/cookies
session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.set('__Secure-1PSID', token)
session.cookies.set('__Secure-1PSIDTS', '<VALUE>')
session.cookies.set('__Secure-1PSIDCC', '<VALUE>')

# Bot (Token do Discord na ultima linha desse bloco)
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # Cria as principais variáveis
  texto = message.content
  for mencionado in message.mentions:
    if mencionado.bot:
      texto = texto.replace(f'<@{mencionado.id}>', '')
  canal = message.channel
  global channel_id
  channel_id = ''

  # Estrutura principal
  if texto:

    # Splash de carregamento
    splash = await canal.send(':hourglass:')

    # Verifica se deve apagar os dados do chat
    if channel_id != canal.id:
      channel_id = canal.id
      global bard
      bard = Bard(token=token, session=session)

    # Verifica se tem anexo de imagem na mensagem
    if message.attachments:
      anexo = message.attachments[0]
      with open(anexo.filename, 'rb') as file:
        image = discord.Image(file)
        resposta_api = bard.ask_about_image(texto, image)
    else:
      resposta_api = bard.get_answer(texto)

    # Trata a resposta da API
    mensagem_api = resposta_api['content']
    links_api = resposta_api['links']

    # Interpreta as imagens
    for link in links_api:
      mensagem_api = re.sub(r'\[Image of(.*?)\]', link, mensagem_api, count=1)

    # Recebe a mensagem do usuário
    await splash.delete()
    while mensagem_api != '':
      await canal.send(mensagem_api[:2000])
      mensagem_api = mensagem_api[2000:]

client.run(config['tokens']['discord_token'])
