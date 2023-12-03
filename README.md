# kevin
IA/AI.
# Passos 

## Dependências

* run ```pip3 install -r requirements.txt```

## Passo 1: Crie um bot no Discord

1. Visite https://discord.com/developers/applications e crie um aplicativo
2. Crie um bot para seu aplicativo
3. Copie o token do bot nas configurações do bot, clicando em `Reset Token`.

   ![image](https://user-images.githubusercontent.com/89479282/205949161-4b508c6d-19a7-49b6-b8ed-7525ddbef430.png)
4. cole o token no `config.ini` após `discord_token =`

   <img height="190" width="390" alt="image" src="https://user-images.githubusercontent.com/89479282/222661803-a7537ca7-88ae-4e66-9bec-384f3e83e6bd.png">

5. Ligue MESSAGE CONTENT INTENT

   ![image](https://user-images.githubusercontent.com/89479282/205949323-4354bd7d-9bb9-4f4b-a87e-deb9933a89b5.png)

6. Convide seu bot pelo OAuth2 URL Generator

   ![image](https://user-images.githubusercontent.com/89479282/205949600-0c7ddb40-7e82-47a0-b59a-b089f929d177.png)

## Passo 2: Autenticação
1. Visite https://bard.google.com/
2. Tecle F12
3. Navegue por: Applicativo → Cookies → copie o valor de `__Secure-1PSID`.

## Passo 3: Executar o bot

1. Abra o terminal

2. Navegue até o diretório em que você instalou o kevin

3. Execute `python3 kevin.py` ou `./kevin.py` para iniciar o bot

![bard_api](https://github.com/proxlu/kevin/assets/105125779/6e6f18cc-b5f1-44a1-a570-0d981eb4a3c1)

