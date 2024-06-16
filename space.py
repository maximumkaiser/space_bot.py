
import nextcord
from nextcord.ext import commands
import aiohttp
import random
from io import BytesIO
import base64
import time
import json
import asyncio
import requests
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle, Embed
from nextcord.ui import Button, View

api_key = 'your-api-key'
token = "your-token"


bot = commands.Bot()
client = nextcord.Client()


@bot.event
async def on_ready():
    print(f'bot online as {bot.user}')




            
@bot.slash_command(description= "version and changelog of bot")
async def version(interaction: nextcord.Interaction):
        embedVar = nextcord.Embed(title="Version and Changelog", description="space bot 0.6 beta", color=0x1395ec)
        embedVar.set_author(name = "space.py" , icon_url= "https://imgur.com/a/gqkJdO1")
        embedVar.add_field(name="Version", value="0.7 beta", inline=False)
        embedVar.add_field(name="Changelog", value="to be added", inline=False)
        embedVar.add_field(name="Release name", value="EXPLORER", inline=False)
        embedVar.set_footer(text= "Made by maximum_kaiser.")
        await interaction.send(embed=embedVar)

cf = 1,0
@bot.slash_command(description= "Heads or Tails?")
async def coinflip(interaction: nextcord.Interaction):
    if random.choice(cf) == 1:
        embed= nextcord.Embed(title = "Heads!!!" , description= " You  Got heads!")
        await interaction.send(embed= embed)
    else:
        embedVar= nextcord.Embed(title = "Tails!!" , description= "You  Got tails!")
        await interaction.send(embed= embedVar)

@bot.slash_command(description = "list of all commands")
async def help(interaction: nextcord.Interaction):
    embed= nextcord.Embed(title= "List of all commands" )
    embed.add_field(name= "/hello" , value= " says hello with your username" , inline= True)
    embed.add_field(name= "/version" , value= "Shows version and changelog" , inline= True)
    embed.add_field(name= "/motivate_me" , value= "motivates you with a quote" , inline = True)
    embed.add_field(name= "/coinflip" , value= "Flips a coin" , inline = True)
    embed.add_field(name= "/serverinfo" , value= "shows server info" , inline = True)
    embed.add_field(name= "/rememberemoji" , value= "start a minigame of remember a emoji" , inline = True)
    embed.aintdd_field(name= "/space" , value= "shows todays picture from nasa" , inline = True)eraction.send(embed= embed)
    await 
		

@bot.slash_command(name="space_image", description="Get the Astronomy Picture of the Day")
async def space_image(interaction: nextcord.Interaction): 
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

            # Print out the data dictionary to see what keys are available
            print(data)
            
            # Check if 'url' key exists in the response
            if 'url' in data:
                image_url = data['url']
                embed = nextcord.Embed(title="Space Image", description="Here's your beautiful picture from NASA!")
                embed.set_image(url=image_url)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("Sorry, no image URL found in NASA's response.")


motivational_quotes = [
    "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.",
    "Do not wait to strike till the iron is hot; but make it hot by striking.",
    "The best way to predict the future is to create it.",
    'The only way to do great work is to love what you do.',
    'Believe you can and you’re halfway there.',
    'Don’t watch the clock; do what it does. Keep going.',
    "Whatever makes you feel bad, leave it.",
    "Whatever makes you smile, keep it.",
    "Don’t lower your standards for anyone or anything; SELF-RESPECT is everything.",
    "If you see me LESS, I’m making some changes in life; you are one of them.",
    "Yes! I am a gamer, but I only play once I start gaming.",
    "When I play fighting games, I press random buttons and hope for the rest.",
    "Nobody is born an avid gamer.",
    "Heroes never die.",
    "Failure doesn't mean game over; it means trying again with experience.",
    "If you find yourself in a hole, the first thing to do is stop digging.",
    "If there is nothing in the chest, a chest doesn’t mean anything.",
    "Keep calm and game on.",
    "The harder you press the button, the stronger the attack.",
    "It’s dangerous to go alone, take this!",
    "The grass is growing, the birds are flying, the sun is rising, and brother, I am hurting people.",
    "Stay awhile and listen!",
    "Praise the sun!",
    "Hey! Look! Listen!",
    "There is no shame in being weak; shame is in staying weak.",
    "Be proud of your work, even if it’s not the best.",
    "Hope is the only thing stronger than fear.",
    "It doesn't matter if you win or lose because some people win by losing, and some win by losing.",
    "Hope is the only thing stronger than fear.",
    "You learn a lot about people when you play with them.",
    "Focus on yourself, play your game, and don’t be afraid to win.",
    "Keep calm and blame it on the lag.",
    "Do more of what makes you happy.",
    "We don't stop playing because we grow old; we grow old because we stop playing.",
    "You’re not too old, and it is not too late.",
    "Never give up; everyone has bad days. Pick yourself up and keep going.",
    "LESS PEOPLE, LESS NONSENSE.",
    "Be mature enough to accept rejections and failures.",
    "Life is all about balance.",
    "You don’t always need to be getting stuff done. Sometimes, it’s perfectly okay and necessary to shut down, kick back and do nothing.",
    "Every thought we think is creating our future.",
    "If you want light to come into your life, you must stand where it shines.",
    "Life has no remote. You have to get it and change it.",
    "The wiser you get, the less you speak.",
    "Your PRESENT is the PAST of your FUTURE.",
    "When you come out of the storm, you won’t be the same person that walked in. That is what the storm is all about.",
    "I am just striving to be more than I have ever been.",
    "I am learning to love the sound of my feet walking away from things not meant for me.",
    "If you want to know someone’s mind, listen to their words. If you want to know someone’s heart, listen to their actions.",
    "Those who judge will never understand, and those who understand will never judge.",
    "Learn to enjoy your company and stop waiting for someone else to make you happy.",
    "The three most important words you can say to yourself are, ‘Yes, I can.’"
]

@bot.slash_command(name="motivate_me", description="Get a motivational quote")
async def motivate_me(interaction: nextcord.Interaction):
    quote = random.choice(motivational_quotes)
    await interaction.response.send_message(quote)

@bot.slash_command(name='rememberemoji', description='Play a game of Remember the Emoji')
async def rememberemoji(interaction: nextcord.Interaction):
    emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇']
    correct_emoji = random.choice(emojis)
    
    await interaction.response.send_message(f'Remember this emoji: {correct_emoji}')
    
    # Wait for 5 seconds
    await asyncio.sleep(3)
    
    # Shuffle emojis and present as options
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


bot.run(token)
