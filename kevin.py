#!/bin/python3
# -*- coding: utf-8 -*-
# 
# kevin.py - by:proxlu

# Configurações
nome = 'kevin' # Nome do bot
criador = 'proxlu' # Criador do bot

import re
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard
import requests
import discord
import asyncio
import json
import time

# Opcional para não expor os tokens
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

# Carregamento
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
channel_id = ''

# Armazena os tokens
bot = config['tokens']['discord_token'] # Opcional para não expor o token
token = config['tokens']['bard_token'] # Opcional para não expor o token

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
  conteudo = message.content
  texto = conteudo.replace(nome, 'Bard').replace(nome.lower(), 'bard').sub(nome.upper(), 'BARD')
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
      timestamp = time.time()
      extensao = anexo.filename.split('.')[-1]
      imagens_validas = ['jpg', 'jpeg', 'png', 'webp', 'JPG', 'JPEG', 'PNG', 'WEBP']

      # Verifica se tem anexo de imagem na mensagem
      if extensao in imagens_validas:
        nome_arquivo = f'.{timestamp}.{anexo.filename}'
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

    # Trata a resposta da api
    mensagem_api = resposta_api['content']
    links_api = resposta_api['links']
    links_mensagem = re.findall(r'\[http([^\]]*?)\]\(([^)]*?)\)', mensagem_api)
    if not links_api:
      links_api = [':frame_photo:']
    
    # Interpreta as imagens
    for link in links_api:
      if re.search(r'\.(jpg|jpeg|png|webp|JPG|JPEG|PNG|WEBP)(?:[?#/].*)?$', link):
        mensagem_api = re.sub(r'\[Image([^\]]*?)\]', link, mensagem_api, count=1, flags=re.UNICODE)
      else:
        mensagem_api = re.sub(r'\[Video([^\]]*?)\]', link, mensagem_api, count=1, flags=re.UNICODE)
        youtube_content = True
    if youtube_content:
      mensagem_api = re.sub(r'http://googleusercontent\.com/youtube_content/([^\]]*?)$', '', mensagem_api, flags=re.UNICODE)
    
    # Interpreta as urls
    for link, parenteses in links_mensagem:
      mensagem_api = mensagem_api.replace(f'[http{link}]({parenteses})', parenteses)

    # Substitui o nome e o criador
    if 'bard' not in conteudo.casefold() and 'google ai' not in conteudo.casefold():
      mensagem_api = mensagem_api.replace('Bard', nome).replace('bard', nome).replace('BARD', nome)
      mensagem_api = mensagem_api.replace('Google AI', criador).replace('google ai', criador).replace('GOOGLE AI', criador)

    # Envia a resposta do usuário
    await splash.delete()
    while mensagem_api != '':
      await canal.send(mensagem_api[:2000])
      mensagem_api = mensagem_api[2000:]

client.run(bot)
