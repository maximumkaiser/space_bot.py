import nextcord
from nextcord.ext import commands
import aiohttp
import random
from datetime import datetime
import pytz
import requests

# Initialize bot
bot = commands.Bot()

# Replace with your bot token (keep it secure)
TOKEN = "your-bot-token"

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Bot online as {bot.user}')

# Command: /version
@bot.slash_command(description="Version and changelog of bot")
async def version(interaction: nextcord.Interaction):
    embedVar = nextcord.Embed(title="Version and Changelog", description="space bot 0.8.2 beta", color=0x1395ec)
    embedVar.set_author(name="space.py", icon_url="https://imgur.com/a/gqkJdO1")
    embedVar.add_field(name="Version", value="0.8.2 beta", inline=False)
    embedVar.add_field(name="Changelog", value="to be added", inline=False)
    embedVar.add_field(name="Release name", value="EXPLORER", inline=False)
    embedVar.set_footer(text="Made by maximum_kaiser.")
    await interaction.send(embed=embedVar)

# Command: /help
@bot.slash_command(description="List of all commands")
async def help(interaction: nextcord.Interaction):
    embed = nextcord.Embed(title="List of all commands")
    embed.add_field(name="/version", value="Shows version and changelog", inline=True)
    embed.add_field(name="/motivate_me", value="Motivates you with a quote", inline=True)
    embed.add_field(name="/coinflip", value="Flips a coin", inline=True)
    embed.add_field(name="/serverinfo", value="Shows server info", inline=True)
    embed.add_field(name="/rememberemoji", value="Start a minigame of remember an emoji", inline=True)
    embed.add_field(name="/space", value="Shows today's picture from NASA", inline=True)
    embed.add_field(name="/user_details", value="Shows details of a user in the server", inline=True)
    embed.add_field(name="/convert_time", value="Converts current time from one timezone to another", inline=True)
    embed.add_field(name="/convert_date", value="Converts date from one timezone to another (YY-MM-DD)", inline=True)
    embed.add_field(name="/joke", value="Tells you a joke", inline=True)
    embed.add_field(name="/dadjoke", value="Tells you a dad joke", inline=True)
    embed.add_field(name="/dark_humor", value="Tells you an offensive joke", inline=True)
    await interaction.send(embed=embed)

# Command: /space_image
@bot.slash_command(name="space_image", description="Get the Astronomy Picture of the Day")
async def space_image(interaction: nextcord.Interaction):
    api_key = 'your-api-key'
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            
            if 'url' in data:
                image_url = data['url']
                embed = nextcord.Embed(title="Space Image", description="Here's your beautiful picture from NASA!")
                embed.set_image(url=image_url)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("Sorry, no image URL found in NASA's response.")

# Command: /motivate_me
def get_motivational_quote():
    response = requests.get('https://type.fit/api/quotes')  
    if response.status_code == 200:
        quotes = response.json()
        quote = random.choice(quotes)  
        return f"{quote['text']} - {quote['author']}"
    else:
        return "I couldn't fetch a quote at the moment, sorry!"

@bot.slash_command(name="motivate_me", description="Gives you a motivational quote")
async def motivate(interaction: nextcord.Interaction):
    quote = get_motivational_quote()
    embed = nextcord.Embed(title="Motivational Quote", description=quote, color=0x1F8B4C)
    await interaction.response.send_message(embed=embed)

# Command: /rememberemoji
@bot.slash_command(name='rememberemoji', description='Play a game of Remember the Emoji')
async def rememberemoji(interaction: nextcord.Interaction):
    emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇']
    correct_emoji = random.choice(emojis)
    
    await interaction.response.send_message(f'Remember this emoji: {correct_emoji}')
    
    await asyncio.sleep(3)
    
    random.shuffle(emojis)
    options = [nextcord.SelectOption(label=emoji, value=emoji) for emoji in emojis]
    
    select = nextcord.ui.Select(
        placeholder='Choose the correct emoji',
        min_values=1,
        max_values=1,
        options=options,
    )
    
    async def select_callback(interaction: nextcord.Interaction):
        if interaction.data['values'][0] == correct_emoji:
            await interaction.response.send_message('Correct! 🎉')
        else:
            await interaction.response.send_message('Oops! That was not the correct emoji. 😓')
    
    select.callback = select_callback
    
    view = nextcord.ui.View()
    view.add_item(select)
    
    await interaction.edit_original_message(content='Which one was it?', view=view)

# Command: /convert_time
@bot.slash_command(name="convert_time", description="Converts current time from one timezone to another")
async def convert_time(interaction: nextcord.Interaction, source_timezone: str, target_timezone: str):
    utc_now = datetime.now(pytz.utc)
    source_time = utc_now.astimezone(pytz.timezone(source_timezone))
    target_time = source_time.astimezone(pytz.timezone(target_timezone))
    embed = nextcord.Embed(title="Timezone Conversion", color=nextcord.Color.blue())
    embed.add_field(name="Source Timezone", value=f"{source_timezone}: {source_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}", inline=False)
    embed.add_field(name="Target Timezone", value=f"{target_timezone}: {target_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}", inline=False)
    await interaction.response.send_message(embed=embed)

# Command: /user_details
@bot.slash_command(name="user_details", description="Shows details of a user in the server")
async def user_details(interaction: nextcord.Interaction, member: nextcord.Member):
    embed = nextcord.Embed(title=f"User Details - {member.display_name}", color=nextcord.Color.green())
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Joined Server On", value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name="Top Role", value=member.top_role.name, inline=False)
    await interaction.response.send_message(embed=embed)

# Command: /convert_date
@bot.slash_command(name="convert_date", description="Converts a given date from one timezone to another (YY-MM-DD)")
async def convert_date(interaction: nextcord.Interaction, date: str, source_timezone: str, target_timezone: str):
    input_date = datetime.strptime(date, '%Y-%m-%d')
    source_time = pytz.timezone(source_timezone).localize(input_date)
    target_time = source_time.astimezone(pytz.timezone(target_timezone))
    embed = nextcord.Embed(title="Date Timezone Conversion", color=nextcord.Color.blue())
    embed.add_field(name="Source Timezone", value=f"{source_timezone}: {source_time.strftime('%Y-%m-%d %Z%z')}", inline=False)
    embed.add_field(name="Target Timezone", value=f"{target_timezone}: {target_time.strftime('%Y-%m-%d %Z%z')}", inline=False)
    await interaction.response.send_message(embed=embed)

# Command: /dadjoke
def get_dad_joke():
    response = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
    if response.status_code == 200:
        joke = response.json().get('joke')
        return joke
    else:
        return "I couldn't fetch a joke at the moment, sorry!"

@bot.slash_command(name="dadjoke", description="Tells a random dad joke")
async def dadjoke(interaction: nextcord.Interaction):
    joke = get_dad_joke()
    embed = nextcord.Embed(title="Dad Joke", description=joke, color=0x00ff00)
    await interaction.response.send_message(embed=embed)

# Command: /joke
@bot.slash_command(name="joke", description="Get a random joke")
async def joke(interaction: nextcord.Interaction):
    response = requests.get("https://v2.jokeapi.dev/joke/Any")
    joke_data = response.json()

    embed = nextcord.Embed(color=nextcord.Color.random())

    if joke_data["type"] == "single":
        embed.add_field(name="Joke", value=joke_data["joke"], inline=False)
    else:
        embed.add_field(name="Setup", value=joke_data["setup"], inline=False)
        embed.add_field(name="Delivery", value=joke_data["delivery"], inline=False)

    await interaction.response.send_message(embed=embed)

# Command: /dark_humor
@bot.slash_command(name="dark_humor", description="Warning: joke may be offensive")
async def dark_humor(interaction: nextcord.Interaction):
    response = requests.get("https://v2.jokeapi.dev/joke/Dark?blacklistFlags=explicit")
    joke_data = response.json()

    embed = nextcord.Embed(color=nextcord.Color.random())

    if joke_data["type"] == "single":
        embed.add_field(name="Joke", value=joke_data["joke"], inline=False)
    else:
        embed.add_field(name="Setup", value=joke_data["setup"], inline=False)
        embed.add_field(name="Delivery", value=joke_data["delivery"], inline=False)

    await interaction.response.send_message(embed=embed)

# Run the bot
bot.run(TOKEN)
