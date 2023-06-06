import discord
import random
import os

from discord.ext import commands
from dotenv import load_dotenv
from models.weather import Weather

from quotes.weather import messages as quotes_weather

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_PREFIX = os.getenv('DISCORD_PREFIX', '!')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=DISCORD_PREFIX, intents=intents)

@bot.event
async def on_ready():
    # Mostra no terminal quando o bot estiver pronto
    print(f'Conectado como {bot.user.name} - {bot.user.id}')

    # Set the bot's status
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="Meu querido(a) ❤️"
    ))

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

@bot.command()
async def clima(ctx, *, cidade=None):
    if not cidade:
        return await ctx.send('Você precisa informar uma cidade, exemplo: !clima São Paulo, querido(a) ❤️')

    weather = Weather(WEATHER_API_KEY)

    # Get the city's coordinates
    coordenates = weather.get_location(cidade)
    lat, lon = coordenates

    # Get the weather
    clima = weather.get_weather(lat, lon, cidade)

    embed = discord.Embed(
        title=f"Clima em {clima['city']}, {clima['country']}",
        description=f"{clima['description']}",
        color=discord.Color.blue()
    )

    embed.add_field(name="Temperatura atual", value=f"{clima['current']}°C")
    embed.add_field(name="Temperatura mínima", value=f"{clima['min']}°C")
    embed.add_field(name="Temperatura máxima", value=f"{clima['max']}°C")

    embed.set_thumbnail(
        url=f"http://openweathermap.org/img/wn/{clima['icon']}.png")

    footer_text = "Que tal um clima quente entre nós? ❤️"

    if clima["description"] in quotes_weather:
        footer_text = f"{random.choice(quotes_weather[clima['description']])} ❤️"

    embed.set_footer(text=footer_text)


    return await ctx.send(embed=embed)


bot.run(DISCORD_TOKEN)
