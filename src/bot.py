import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# Inicialização do bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
bot.ROLEPLAY_CHANNEL_ID = 1082785898539786284  # ID do canal de roleplay

# Configuração do método de sincronização de comandos
async def setup_hook():
    # Sincronizar comandos globais e para o servidor específico
    bot.tree.copy_global_to(guild=discord.Object(id=1082785898539786280))
    await bot.tree.sync(guild=discord.Object(id=1082785898539786280))

# Configuração para executar o método de sincronização de comandos
@bot.event
async def on_ready():
    
    print(f'Logged on as {bot.user}!')
    await setup_hook()  # Sincroniza os comandos

async def load_extensions():
    # Carregar os cogs
    await bot.load_extension('cogs.buttons')
    await bot.load_extension('cogs.pokemon')
    await bot.load_extension('cogs.events')

async def main():
    # Carregar as extensões
    await load_extensions()
    # Rodar o bot
    await bot.start(TOKEN)

# Configuração do token
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Executar o bot usando asyncio.run
asyncio.run(main())
