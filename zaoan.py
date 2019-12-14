import discord
import logging
import re
import json
import jogador

logging.basicConfig(level=logging.INFO)

client = discord.Client()

with open('config.json', 'r') as configfile:
    config = json.load(configfile)

configfile.close()

jogadores = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.type == 'dm':
        return

    if message.content.startswith('!hello'):
        embed = discord.Embed(title="Title", description="Hello World", color=0x00ff00)
        embed.add_field(name="Field1", value="Hello", inline=False)
        embed.add_field(name="Field2", value="World", inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith('!calc'):
        adiciona_jogador(message.content)

        if len(jogadores) > 0:
            profit = calc_profit_total()

        profit_individual = round(profit/len(jogadores), 4)
        
        print(profit, profit_individual)

        jogadores.clear()

def adiciona_jogador(message):
    infos_jogador = []
    lista_jogadores = re.findall('.+\n\\s+.+\n\\s+.+\n\\s+.+', message)

    for char in lista_jogadores:
        infos_jogador.append(char.split('\n'))

    for i in range(len(infos_jogador)):
        jogadores.append(jogador.Jogador(i, infos_jogador[i][0].strip(), infos_jogador[i][3][infos_jogador[i][3].find(':')+1:].strip().replace(',',''), 0))

def calc_profit_total():
    calc_profit = 0
    for i in range(len(jogadores)):
        calc_profit = calc_profit + float(jogadores[i].loot)
    return calc_profit


client.run(config['token'])