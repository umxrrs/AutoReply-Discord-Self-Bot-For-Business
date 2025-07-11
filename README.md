# Discord Selfbot Autoreply
---

A Discord selfbot that autoreplies to DMs for a business, handling greetings, menu requests, payment methods, and transaction notifications.
---

**⚠️ Warning**: Selfbots violate Discord's Terms of Service and may lead to account bans. Use for educational purposes only. Consider using a proper bot account instead.
---

## Features
- Responds to greetings ("hello", "hi", etc.) with a customizable message.
- Sends a menu when asked ("what is ur menu", "show me the items ur selling", etc.).
- Provides payment methods for purchase requests or payment queries.
- Notifies the owner in a specified server when a transaction is reported.
- Blocks messages with swear words, Discord invites, or URLs.
- Uses typing indicators for natural responses.
- Supports `!setmessage` command to update responses dynamically.
---

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/umxrrs/AutoReply-Discord-Self-Bot-For-Business
   cd AutoReply-Discord-Self-Bot-For-Business
   ```
---

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
---

3. Configure the bot in `selfbot.py`:
- Replace `YOUR_DISCORD_USER_TOKEN` with your Discord user token.
- Replace `YOUR_GUILD_ID` with the server ID for notifications.
- Replace `YOUR_CHANNEL_ID` with the channel ID for notifications.
- Replace `YOUR_USERNAME` with your Discord username.
---
4. Run the bot:
   ```bash
   python selfbot.py 
   ```
---
   ```bash
   py selfbot.py
```
---
### Usage
- **Greetings:** Responds to "hello", "hi", etc., with "Hello! How can I help you?" (customizable).
- **Menu Requests:** Triggered by phrases like "what is ur menu" or "show me the items ur selling".
- **Payment Requests:** Triggered by phrases like "payment method" or "how to pay".
- **Purchase Handling:** Responds with payment methods for phrases like "buy logo".
- **Transaction Notification:** Sends a confirmation and notifies the owner in the specified server for transaction-related messages.
- **Blocked Messages:** Ignores messages with swear words, Discord invites, or URLs.
- **!setmessage Command:** Use !setmessage 1 <message> for greetings, 2 for menu, or 3 for payment methods (DMs only).
