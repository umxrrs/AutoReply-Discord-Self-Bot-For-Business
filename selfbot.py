import discord  # Changed from selfbot to discord
from discord.ext import commands
from datetime import datetime
import re
import asyncio

bot = commands.Bot(command_prefix='!', self_bot=True)

TOKEN = ''
GUILD_ID = UMXRRS SERVER LOL
NOTIFY_CHANNEL_ID = UMXRRS CHANNEL ID LOL
YOUR_USERNAME = 'umxrrs'

blocked_messages = [
    'fuck', 'shit', 'damn', 'ass', 'bitch',
    'https://discord.gg/',
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
]

responses = {
    1: "Hello! How can I help you?",
    2: """Selling:
Logos
Banners
Profile Pictures
Custom Designs""",
    3: """Payment methods:
BTC: [Your BTC Address]
LTC: [Your LTC Address]
ETH: [Your ETH Address]
Bank Transfer: [Your Bank Details]"""
}

greetings = ['hello', 'hi', 'hey', 'yo', 'sup']
menu_requests = ['what is ur menu', 'what are u selling', 'what u guys got', 'show me ur menu', 'show me the items ur selling', 'send me ur menu']
payment_requests = ['payment method', 'how to pay', 'what is ur payment method', 'payment options']

def is_blocked(message_content):
    message_content = message_content.lower()
    for blocked in blocked_messages:
        if blocked.startswith('http'):
            if re.search(blocked, message_content):
                return True
        elif blocked in message_content:
            return True
    return False

def extract_order(message_content, menu_items):
    message_content = message_content.lower().strip()
    items = [item.strip().lower() for item in menu_items.split('\n')[1:] if item.strip()]
    for item in items:
        if re.search(r'\b' + re.escape(item) + r'\b', message_content):
            return item.capitalize()
        if item.endswith('s'):
            singular = item[:-1]
            if re.search(r'\b' + re.escape(singular) + r'\b', message_content):
                return item.capitalize()
    return "Unknown"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user and isinstance(message.channel, discord.DMChannel):  # Changed to discord.DMChannel
        await bot.process_commands(message)
        return
    if not isinstance(message.channel, discord.DMChannel):  # Changed to discord.DMChannel
        return
    if is_blocked(message.content):
        return
    content = message.content.lower().strip()
    async with message.channel.typing():
        await asyncio.sleep(1)
        if any(greet in content for greet in greetings):
            await message.channel.send(responses[1])
        elif any(req in content for req in menu_requests):
            await message.channel.send(responses[2])
        elif any(req in content for req in payment_requests):
            await message.channel.send(responses[3])
        elif 'buy' in content:
            order = extract_order(content, responses[2])
            await message.channel.send(responses[3])
        elif 'transaction' in content or 'paid' in content or 'payment' in content:
            await message.channel.send("Give me 2-3 mins, I'll check and then let you know the update.")
            guild = bot.get_guild(GUILD_ID)
            if guild:
                channel = guild.get_channel(NOTIFY_CHANNEL_ID)
                if channel:
                    order = extract_order(content, responses[2])
                    notification = f"""
{YOUR_USERNAME}
Buyer DM Channel ID: {message.channel.id}
Buyer Username: {message.author}
Order: {order}
"""
                    await channel.send(notification)

@bot.command()
async def setmessage(ctx, message_number: int, *, new_message: str):
    if not isinstance(ctx.channel, discord.DMChannel):  # Changed to discord.DMChannel
        return
    if message_number not in [1, 2, 3]:
        await ctx.send("Invalid message number! Use 1 (greeting), 2 (menu), or 3 (payment methods).")
        return
    responses[message_number] = new_message
    await ctx.send(f"Message {message_number} updated to: {new_message}")

bot.run(TOKEN)
