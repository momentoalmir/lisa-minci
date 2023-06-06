import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_PREFIX = os.getenv('DISCORD_PREFIX', '!')

bot = commands.Bot(command_prefix=DISCORD_PREFIX, intents=discord.Intents.all())

@bot.event
async def on_ready():
    # Mostra no terminal quando o bot estiver pronto
    print(f'Conectado como {bot.user.name} - {bot.user.id}')

@bot.command()
async def ping(ctx):
    # Calcula a latência do bot
    latency = bot.latency * 1000
    # Envia a mensagem com a latência
    await ctx.send(f'Pong ❤️ {latency:.2f}ms')

@bot.command()
async def clear(ctx, amount=5):
    # Limpa as mensagens do canal
    if not ctx.author.guild_permissions.manage_messages:
        return await ctx.send('Você não tem permissão para usar esse comando!')

    return await ctx.channel.purge(limit=amount)

bot.run(DISCORD_TOKEN)
