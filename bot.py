# MADE BY UMXRRS
import discord
from discord.ext import commands
from datetime import datetime
import re
import asyncio
import json
import aiohttp
import random

bot = commands.Bot(command_prefix=',', self_bot=True)

TOKEN = 'token here'
WEBHOOK_URL = 'webhook urls'
YOUR_USER_ID = 'uid here'

# Bot status - controls whether the bot responds to messages
bot_active = True

# Store conversation states for each channel
conversation_states = {}
# Store conversation history 
conversation_history = {}

blocked_messages = [
    'fuck', 'shit', 'damn', 'ass', 'bitch',
    'https://discord.gg/',
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
]

responses = {
    1: "How are u?",
    2: """actually sorry for disturbing ik i bother you but i just need your some precious time bcuz i wanna ask you something if you allow me to do so?""",
    3: """Actually I wanted to ask since you can see from my profile that I do commission art I just wanted to know if you might consider giving me a small commission because last month I had set a goal to complete at least fifteen commissions in order to cover my household expenses such as groceries but unfortunately I was only able to get two commissions which was not enough to meet my needs so now I am trying to get as many commissions as possible and I was wondering if you would be interested in having something designed by me at a reasonable price""",
    4: "I have good payment policy if ur interested ill let u know the payment policy",
    5: "oh okay tell me the payment policy + the starting price is 30$ (ill edit it by my own)",
    6: {
        "interested": "Okay thank u show me the art or design u want me to do the prices will be on ur requirements since the starting price are 30$",
        "not_interested": "Okay thank u have a nice day. Let me know if any of ur friend is interested and wanting to commission"
    }
}

# More comprehensive keyword lists
positive_responses = ['yes', 'go ahead', 'ask away', 'yep', 'sure', 'yeah', 'ok', 'okay', 'alright', 'fine', 'go on', 'continue', 'proceed']
negative_responses = ['no', 'nah', 'nope', 'sorry no', 'no thanks', 'not really', 'dont want', "don't want", 'not now', 'maybe later']

# Interest responses - things that show they want to know more
interest_responses = [
    'im interested', 'interested', 'yes im interested', 'sure why not', 'why not', 
    'tell me', 'payment policy', 'show me', 'how much', 'price', 'cost', 'pricing',
    'what are your prices', 'whats the price', "what's the price", 'budget', 
    'affordable', 'cheap', 'expensive', 'rates', 'fee', 'charge'
]

# Uninterest responses - things that show they're not interested
uninterest_responses = [
    'not interested', 'im not interested', "i'm not interested", 'no thanks', 'not really', 
    'nah', 'nope', 'no thank you', 'not for me', 'not right now', 'maybe later',
    'cant afford', "can't afford", 'too expensive', 'no money', 'broke', 'poor',
    'not looking', 'dont need', "don't need", 'not buying', 'pass', 'skip',
    'not today', 'another time', 'not now', 'busy', 'no funds', 'tight budget'
]

greetings = ['hello', 'hi', 'hey', 'yo', 'sup', 'hii', 'hiii', 'heyyy']
good_responses = ['im good', 'good', 'great', 'amazing', 'fine', 'okay', 'alright', 'doing good', 'im fine', 'im okay']

def check_interest_level(content):
    """Check if message shows interest, disinterest, or neutral"""
    content_lower = content.lower().strip()
    
    # Check for clear disinterest first (priority)
    for unint in uninterest_responses:
        if unint in content_lower:
            return "not_interested"
    
    # Check for clear interest
    for int_res in interest_responses:
        if int_res in content_lower:
            return "interested"
    
    # Default to neutral
    return "neutral"

def is_blocked(message_content):
    message_content = message_content.lower()
    for blocked in blocked_messages:
        if blocked.startswith('http'):
            if re.search(blocked, message_content):
                return True
        elif blocked in message_content:
            return True
    return False

async def send_webhook_notification(channel_id, username, user_id, order):
    try:
        embed_data = {
            "embeds": [{
                "title": "New Commission Inquiry",
                "description": f"<@{YOUR_USER_ID}>\nBuyer Channel ID: {channel_id}\nBuyer Username: {username}\nBuyer User ID: {user_id}\nOrder: {order}",
                "color": 15258703
            }]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK_URL, json=embed_data) as resp:
                if resp.status in [200, 204]:  # Both are success statuses
                    print(f"Webhook sent successfully - Status: {resp.status}")
                else:
                    print(f"Webhook failed with status {resp.status}")
                    error_text = await resp.text()
                    print(f"Error response: {error_text}")
    except Exception as e:
        print(f"Webhook error: {e}")

def get_conversation_state(channel_id):
    if channel_id not in conversation_states:
        conversation_states[channel_id] = {"step": 0, "last_bot_message": None}
    return conversation_states[channel_id]

def set_conversation_state(channel_id, step, last_message=None):
    conversation_states[channel_id] = {"step": step, "last_bot_message": last_message}

def mark_conversation_complete(channel_id, username, user_id, final_result):
    """Mark conversation as completed and move to history"""
    if channel_id in conversation_states:
        del conversation_states[channel_id]
    
    conversation_history[channel_id] = {
        "username": username,
        "user_id": user_id,
        "final_result": final_result,
        "completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "inactive"
    }

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Bot status: {"Active" if bot_active else "Inactive"}')

@bot.event
async def on_message(message):
    # Skip if it's our own message and process commands
    if message.author == bot.user:
        if isinstance(message.channel, discord.DMChannel):
            await bot.process_commands(message)
        return
    
    # Only respond in DMs
    if not isinstance(message.channel, discord.DMChannel):
        return
    
    # Check if bot is active - if not, ignore all messages except commands
    if not bot_active:
        return
    
    # Skip blocked messages
    if is_blocked(message.content):
        return
    
    content = message.content.lower().strip()
    channel_id = message.channel.id
    state = get_conversation_state(channel_id)
    
    # Add typing indicator
    async with message.channel.typing():
        await asyncio.sleep(random.uniform(1, 3))
        
        # Don't start new conversations with people who already completed one
        if channel_id in conversation_history:
            return  # Ignore messages from completed conversations
        
        # Step 0: Initial greeting
        if state["step"] == 0:
            if any(greet in content for greet in greetings) or message.stickers:
                await message.channel.send(responses[1])
                set_conversation_state(channel_id, 1, responses[1])
                return
        
        # Step 1: After "How are u?" - waiting for response
        elif state["step"] == 1:
            if any(good in content for good in good_responses):
                await asyncio.sleep(random.uniform(1, 2))
                await message.channel.send(responses[2])
                set_conversation_state(channel_id, 2, responses[2])
                return
        
        # Step 2: After asking permission - waiting for yes/no
        elif state["step"] == 2:
            if any(pos in content for pos in positive_responses):
                await asyncio.sleep(random.uniform(60, 120))  # 1-2 minute delay
                await message.channel.send(responses[3])
                set_conversation_state(channel_id, 3, responses[3])
                return
            elif any(neg in content for neg in negative_responses):
                await message.channel.send("Okay, have a great day!")
                set_conversation_state(channel_id, 0)  # Reset conversation
                return
        
        # Step 3: After commission pitch - waiting for interest/disinterest
        elif state["step"] == 3:
            interest_level = check_interest_level(content)
            if interest_level == "not_interested":
                await message.channel.send(responses[4])
                set_conversation_state(channel_id, 4, responses[4])
                return
            elif interest_level == "interested":
                await message.channel.send(responses[5])
                await send_webhook_notification(channel_id, message.author.name, message.author.id, "Direct Yes")
                set_conversation_state(channel_id, 5, responses[5])
                return
        
        # Step 4: After "I have good payment policy" - waiting for interest
        elif state["step"] == 4:
            interest_level = check_interest_level(content)
            if interest_level == "interested":
                await asyncio.sleep(random.uniform(2, 5))
                await message.channel.send(responses[5])
                await send_webhook_notification(channel_id, message.author.name, message.author.id, "Yes")
                set_conversation_state(channel_id, 5, responses[5])
                return
            elif interest_level == "not_interested":
                await asyncio.sleep(random.uniform(2, 4))
                await message.channel.send(responses[6]["not_interested"])
                await send_webhook_notification(channel_id, message.author.name, message.author.id, "No")
                mark_conversation_complete(channel_id, message.author.name, message.author.id, "Rejected")
                return
        
        # Step 5: After showing policy/price - final responses
        elif state["step"] == 5:
            interest_level = check_interest_level(content)
            if interest_level == "interested":
                await asyncio.sleep(random.uniform(2, 4))
                await message.channel.send(responses[6]["interested"])
                await send_webhook_notification(channel_id, message.author.name, message.author.id, "Final Yes")
                mark_conversation_complete(channel_id, message.author.name, message.author.id, "Commissioned")
                return
            elif interest_level == "not_interested":
                await asyncio.sleep(random.uniform(2, 4))
                await message.channel.send(responses[6]["not_interested"])
                await send_webhook_notification(channel_id, message.author.name, message.author.id, "Final No")
                mark_conversation_complete(channel_id, message.author.name, message.author.id, "Rejected")
                return
        
        # Special case: if someone mentions "buy" at any point
        if 'buy' in content and state["step"] < 3:
            await asyncio.sleep(random.uniform(2, 4))
            await message.channel.send(responses[3])
            set_conversation_state(channel_id, 3, responses[3])
            return
        
        # If no specific response matched, handle greetings at any step
        if any(greet in content for greet in greetings) and state["step"] == 0:
            await message.channel.send(responses[1])
            set_conversation_state(channel_id, 1, responses[1])

# ON/OFF TOGGLE COMMANDS
@bot.command(name='ar')
async def toggle_bot(ctx, action: str = None):
    """Toggle bot on/off with ,ar on or ,ar off"""
    if not isinstance(ctx.channel, discord.DMChannel):
        return
    
    global bot_active
    
    if action is None:
        # Show current status
        status = "🟢 ON" if bot_active else "🔴 OFF"
        await ctx.send(f"Bot is currently: {status}")
        return
    
    action = action.lower()
    
    if action in ['on', 'start', 'enable', 'activate']:
        if bot_active:
            await ctx.send("🟢 Bot is already ON")
        else:
            bot_active = True
            await ctx.send("🟢 Bot turned ON - Will now respond to messages")
    
    elif action in ['off', 'stop', 'disable', 'deactivate']:
        if not bot_active:
            await ctx.send("🔴 Bot is already OFF")
        else:
            bot_active = False
            await ctx.send("🔴 Bot turned OFF - Will not respond to messages")
    
    else:
        await ctx.send("Usage: `,ar on` to turn on, `,ar off` to turn off, or `,ar` to check status")

@bot.command()
async def setmessage(ctx, message_number: int, *, new_message: str):
    if not isinstance(ctx.channel, discord.DMChannel):
        return
    
    if message_number not in [1, 2, 3, 4, 5, 6]:
        await ctx.send("Invalid message number! Use 1-6.")
        return
    
    if message_number == 6:
        try:
            data = json.loads(new_message)
            responses[message_number] = {
                "interested": data.get("interested", responses[6]["interested"]), 
                "not_interested": data.get("not_interested", responses[6]["not_interested"])
            }
        except json.JSONDecodeError:
            await ctx.send("Invalid JSON format for message 6. Use: {\"interested\": \"text\", \"not_interested\": \"text\"}")
            return
    else:
        responses[message_number] = new_message
    
    await ctx.send(f"Message {message_number} updated successfully!")

@bot.command()
async def complete(ctx, channel_id: int, result: str = "Completed"):
    """Manually mark a conversation as complete (for when commission work is done)"""
    if not isinstance(ctx.channel, discord.DMChannel):
        return
    
    if channel_id in conversation_states:
        # Get user info from conversation state or history
        username = "Unknown"
        user_id = "Unknown"
        
        # Try to find the channel and get user info
        try:
            channel = bot.get_channel(channel_id)
            if channel and hasattr(channel, 'recipient'):
                username = channel.recipient.name
                user_id = channel.recipient.id
        except:
            pass
            
        mark_conversation_complete(channel_id, username, user_id, result)
        await ctx.send(f"Conversation {channel_id} marked as complete with result: {result}")
    elif channel_id in conversation_history:
        await ctx.send(f"Conversation {channel_id} is already marked as complete")
    else:
        await ctx.send(f"No conversation found for channel {channel_id}")

@bot.command()
async def clear_history(ctx):
    """Clear all conversation history"""
    if not isinstance(ctx.channel, discord.DMChannel):
        return
    
    conversation_history.clear()
    await ctx.send("All conversation history cleared")

@bot.command()
async def reset(ctx, channel_id: int = None):
    """Reset conversation state for a specific channel or current channel"""
    if not isinstance(ctx.channel, discord.DMChannel):
        return
    
    target_channel = channel_id if channel_id else ctx.channel.id
    
    # Remove from active conversations
    if target_channel in conversation_states:
        del conversation_states[target_channel]
        await ctx.send(f"Active conversation reset for channel {target_channel}")
    
    # Remove from history to allow new conversations
    if target_channel in conversation_history:
        del conversation_history[target_channel]
        await ctx.send(f"Conversation history cleared for channel {target_channel}")
    
    if target_channel not in conversation_states and target_channel not in conversation_history:
        await ctx.send("No conversation data found for that channel")

@bot.command()
async def status(ctx):
    """Check current conversation states and history"""
    if not isinstance(ctx.channel, discord.DMChannel):
        return
    
    # Show bot active status first
    bot_status = "🟢 ON" if bot_active else "🔴 OFF"
    status_msg = f"**Bot Status: {bot_status}**\n\n"
    
    # Active conversations
    if conversation_states:
        status_msg += "**Active Conversations:**\n"
        for channel_id, state in conversation_states.items():
            status_msg += f"Channel {channel_id}: Step {state['step']}\n"
        status_msg += "\n"
    else:
        status_msg += "**Active Conversations:** None\n\n"
    
    # Inactive/completed conversations
    if conversation_history:
        status_msg += "**Inactive Conversations:**\n"
        for channel_id, history in conversation_history.items():
            status_msg += f"Channel {channel_id}: {history['username']} - {history['final_result']} ({history['completed_at']})\n"
    else:
        status_msg += "**Inactive Conversations:** None"
    
    # Split message if too long
    if len(status_msg) > 2000:
        parts = [status_msg[i:i+2000] for i in range(0, len(status_msg), 2000)]
        for part in parts:
            await ctx.send(part)
    else:
        await ctx.send(status_msg)

bot.run(TOKEN)
