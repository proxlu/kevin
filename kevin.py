#!/bin/python3
# -*- coding: utf-8 -*-
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard
import requests
import discord

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
session.cookies.set("__Secure-1PSID", token)
session.cookies.set("__Secure-1PSIDTS", "<VALUE>")
session.cookies.set("__Secure-1PSIDCC", "<VALUE>")
# bard = Bard(token=token, session=session) # Descomente esse trecho para que o bot armazene histórico de chat

# Bot
@client.event
async def on_message(message):
	if message.author == client.user:
		return

	canal = message.channel
	texto = message.clean_content

	# Verifica se o bot foi mencionado
	bot_mention = f"<@{client.user.id}>"
	if bot_mention in texto:
		texto = texto.replace(bot_mention, "").strip()  # Remove a menção ao bot

	# Estrutura principal
	if texto.strip():
		
		# Splash de carregamento
		splash = await canal.send(':hourglass:')

		# Solicita a api
		bard = Bard(token=token, session=session) # Comente esse trecho para que o bot armazene histórico de chat
		saida_da_api = bard.get_answer(texto)['content']


		# Recebe a mensagem do usuário
		await splash.delete()
		while saida_da_api != '':
			await canal.send(saida_da_api[:2000])
			saida_da_api = saida_da_api[2000:]

client.run(config['tokens']['discord_token'])
