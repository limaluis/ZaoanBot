import discord
import logging
import re
import json
import jogador
import math

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
        embed = discord.Embed(title="Title", description="Hello World", color=discord.Color.dark_grey)
        embed.add_field(name="Field1", value="Hello", inline=False)
        embed.add_field(name="Field2", value="World", inline=False)
        emoji = '\U0001F4F0'
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction(emoji)

    if message.content.startswith('!calc'):
        adiciona_jogador(message.content)

        if len(jogadores) > 0:
            profit = calc_profit_total()

            profit_individual = round(profit/len(jogadores), 4)

            transfer_msg = discord.Embed(title='Profit: {:,}'.format(profit), description='Por pessoa: {:,}'.format(profit_individual))

            calcula_transfers(profit, profit_individual, transfer_msg)

            await message.channel.send(embed=transfer_msg)
            jogadores.clear()
        else:
            await message.channel.send('Não foi possível adicionar os jogadores.')

def adiciona_jogador(message):
    infos_jogador = []
    lista_jogadores = re.findall('.+\n\\s+.+\n\\s+.+\n\\s+.+', message)

    for char in lista_jogadores:
        infos_jogador.append(char.split('\n'))

    for i in range(len(infos_jogador)):
        if ('(Leader)' in infos_jogador[i][0]):
            nome = infos_jogador[i][0][:infos_jogador[i][0].find('(')].strip()
        else:
            nome = infos_jogador[i][0].strip()

        balance = infos_jogador[i][3][infos_jogador[i][3].find(':')+1:].strip().replace(',','')

        jogadores.append(jogador.Jogador(i, nome, float(balance), float(balance)))
        logging.info('Adicionando jogador - Nome do jogador: {}; balance: {}; waste: {};'.format(jogadores[i].nome, jogadores[i].balance, jogadores[i].waste))

def calc_profit_total():
    calc_profit = 0
    for i in range(len(jogadores)):
        calc_profit = calc_profit + float(jogadores[i].balance)
    return math.floor(calc_profit)

def calcula_transfers(profit, profit_individual, transfer_msg):
    for i in range(len(jogadores)):
        if jogadores[i].waste <= profit_individual:
            continue

        if (profit > 0):
            transferirValor = round(jogadores[i].balance - profit_individual, 4)
        else:
            transferirValor = round(jogadores[i].waste + abs(profit_individual), 4)

        for x in range(len(jogadores)):
            if (i != x and jogadores[x].waste < profit_individual):
                if (transferirValor + jogadores[x].waste <= profit_individual):
                    logging.info('Tranferindo tudo menos profit_individual')
                    transfer_msg.add_field(name=jogadores[i].nome, value='transfer {} to {}'.format(abs(math.floor(transferirValor)), jogadores[x].nome))
                    jogadores[i].waste -= transferirValor
                    logging.info('Jogador que transferiu: {}, novo waste: {}.'.format(jogadores[i].nome, jogadores[i].waste))
                    jogadores[x].waste += transferirValor
                    logging.info('Jogador que recebeu: {}, novo waste: {}.'.format(jogadores[x].nome, jogadores[x].waste))
                else:
                    logging.info('Transferir parte')
                    logging.info('Jogador que deve transferir - {}, waste: {}.'.format(jogadores[i].nome, jogadores[i].waste))
                    logging.info('Jogador que deve receber - {}, waste: {}.'.format(jogadores[x].nome, jogadores[x].waste))
                    transferir = round(abs(jogadores[x].waste - profit_individual), 4)
                    logging.info('Transferir: {}.'.format(transferir))
                    transfer_msg.add_field(name=jogadores[i].nome, value='transfer {} to {}'.format(abs(math.floor(transferir)), jogadores[x].nome))
                    jogadores[i].waste -= transferir
                    logging.info('Jogador que transferiu: {}, novo waste: {}.'.format(jogadores[i].nome, jogadores[i].waste))
                    jogadores[x].waste += transferir
                    logging.info('Jogador que recebeu: {}, novo waste: {}.'.format(jogadores[x].nome, jogadores[x].waste))


client.run(config['token'])