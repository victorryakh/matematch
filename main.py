import config
import os
import discord
from discord.ext import commands

import sys
import logging
log_handler = logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("matematch.log", encoding='utf-8', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def setup_hook():
    bot.tree.copy_global_to(guild=discord.Object(id=config.guild_id))
    await bot.tree.sync(guild=discord.Object(id=config.guild_id))
    logging.info(f"Tree synced to guild {config.guild_id}")
bot.setup_hook = setup_hook

async def wait_message(context):
     def check(message):
        return message.channel == context.channel and message.author == context.author
     return await bot.wait_for('message', check=check)
bot.wait_message = wait_message


@bot.event
async def on_ready():
    logging.info('The bot is ready!')

@bot.check
def check_commands(ctx):
    logging.info(f"Context author is bot: {ctx.author.bot}")
    return ctx.author.bot == False

@bot.hybrid_command()
async def register(ctx):
    """Выполни, чтобы начать использовать бота"""
    await ctx.send("🔹 Дата рождения\nВведи дату рождения в формате DD.MM.YYYY (например, 06.02.2024)")
    birthday = (await bot.wait_message(ctx)).content
    await ctx.send("🔹 О себе\nНапиши ниже то, что стоит знать твоему тиммейту о тебе")
    about_me = (await bot.wait_message(ctx)).content
    

bot.run(config.token, log_handler=log_handler)