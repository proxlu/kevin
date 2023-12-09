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

# Opcional
import configparser
config = configparser.ConfigParser()
config.read("config.ini")

# Carregamento
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
channel_id = ''

# Armazena os tokens
bot = config['tokens']['discord_token'] # Opcional
token = config['tokens']['bard_token'] # Opcional

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

  # Cria as principais variáveis
  texto = message.content
  for mencionado in message.mentions:
    if mencionado.bot:
      texto = texto.replace(f'<@{mencionado.id}>', '')
  canal = message.channel

  # Estrutura principal
  if texto:

    # Splash de carregamento
    splash = await canal.send(':hourglass:')

    # Verifica se deve apagar os dados do chat
    global channel_id
    if channel_id != canal.id:
      channel_id = canal.id
      global bard
      bard = Bard(token=token, session=session)

    # Checagem extra
    if message.attachments:
      anexo = message.attachments[0]
      extensao = anexo.filename.split('.')[-1]
      imagens_validas = ['jpg', 'jpeg', 'png', 'webp']

      # Verifica se tem anexo de imagem na mensagem
      if extensao in imagens_validas:
        nome_arquivo = f'.anexo.{anexo.filename}'
        with open(nome_arquivo, 'wb') as file:
          await anexo.save(file)
        with open(nome_arquivo, 'rb') as image_file:
          image = image_file.read()
        resposta_api = bard.ask_about_image(texto, image)
        os.remove(nome_arquivo)
      else:
        resposta_api = bard.get_answer(texto)
    else:
      resposta_api = bard.get_answer(texto)

    # Trata a resposta da API
    mensagem_api = resposta_api['content']
    links_api = resposta_api['links']
    links_mensagem = re.findall(r'\[http([^\]]*?)\]\(([^)]*?)\)', mensagem_api)
    
    # Interpreta as imagens
    for link in links_api:
      if re.search(r'\.(jpg|jpeg|png|webp)(?:[?#/].*)?$', link):
        mensagem_api = re.sub(r'\[Image of([^\]]*?)\]', link, mensagem_api, count=1, flags=re.UNICODE)
        
    # Interpreta as urls
    for link, parenteses in links_mensagem:
      mensagem_api = mensagem_api.replace(f'[http{link}]({parenteses})', parenteses)
    
    # Recebe a mensagem do usuário
    await splash.delete()
    while mensagem_api != '':
      await canal.send(mensagem_api[:2000])
      mensagem_api = mensagem_api[2000:]

client.run(bot)
