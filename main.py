import config
import os
import discord
from discord.ext import commands

# TODO: make a separate file to setup logging?
import sys
import logging
log_handler = logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/frontend-discord.log", encoding='utf-8', mode='w'),
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


class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Valorant', description='Поддержка рейтинга, статистики'),
            discord.SelectOption(label='CS2', description='Подарок при привязке аккаунта!'),
            discord.SelectOption(label='DOTA 2', description='Yet another description'),
            discord.SelectOption(label="Нет в списке", description="Напишу название игры сам")
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Выбери игру из списка...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())


class RegisterModal(discord.ui.Modal, title='Регистрация'):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
    name = discord.ui.TextInput(
        label='Name',
        placeholder='Your name here...',
    )

    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    feedback = discord.ui.TextInput(
        label='Tell about yourself',
        style=discord.TextStyle.long,
        placeholder='Type here...',
        required=False,
        max_length=300,
    )

@bot.hybrid_command()
async def register(ctx):
    """Выполни, чтобы начать использовать бота"""
    view=DropdownView()
    await ctx.send("asc", view=view)
    await ctx.send("🔹 Дата рождения\nВведи дату рождения в формате DD.MM.YYYY (например, 06.02.2024)")
    birthday = (await bot.wait_message(ctx)).content
    await ctx.send("🔹 О себе\nНапиши ниже то, что стоит знать твоему тиммейту о тебе")
    about_me = (await bot.wait_message(ctx)).content

@bot.hybrid_command()
async def inputname(interaction: discord.Interaction, your_name: str):
    print(your_name)
    await interaction.response.send_message(f'you registered as {your_name}', ephemeral=True)

bot.run(config.token, log_handler=log_handler)