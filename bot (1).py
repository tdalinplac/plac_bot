import os
import zipfile

# Create the project folder structure
os.makedirs("my-telegram-bot", exist_ok=True)

# Create bot.py with updated claim logic
bot_code = """
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("7640462025:AAHtwENanJ-UUenKeJA8YnFWetMrAplFq4A")

# Group chat IDs
group_chat_ids = [
    '-4938012309',
    '-4613148577',
    '-4829453971',
    '-4935109561',
    '-4917561606'
]

# Dictionary to store user-agent mapping
user_agent_mapping = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('សួស្តី! ខ្ញុំជាបុត Telegram របស់អ្នក។')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text

    keyboard = [
        [InlineKeyboardButton("✅ Claim", callback_data=f"claim_{user_id}"),
         InlineKeyboardButton("💬 Reply", callback_data=f"reply_{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Add logic to check if user_id is already claimed
    if str(user_id) in user_agent_mapping:
        # Send message to the claimed group only
        group_id = user_agent_mapping[str(user_id)]["group_id"]
        await context.bot.send_message(
            chat_id=group_id,
            text=f"សារថ្មីពី user {user_id}: {user_message}",
        )
    else:
        # Send message to all groups
        for group_id in group_chat_ids:
            await context.bot.send_message(
                chat_id=group_id,
                text=f"សារពីអ្នកប្រើ {user_id}: {user_message}",
                reply_markup=reply_markup
            )

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query_data = query.data
    agent_id = query.from_user.id

    if query_data.startswith("claim_"):
        user_id = query_data.split("_")[1]
        user_agent_mapping[user_id] = {"agent_id": agent_id, "group_id": query.message.chat_id}
        await query.answer(f"អ្នកបាន Claim សារពី user {user_id}។")
    elif query_data.startswith("reply_"):
        user_id = query_data.split("_")[1]
        if user_agent_mapping.get(user_id) and user_agent_mapping[user_id]["agent_id"] == agent_id:
            await query.message.reply_text(f"សូមឆ្លើយសារទៅ user {user_id}:")
        else:
            await query.answer("អ្នកត្រូវ Claim សារមុនសិន។")

async def show_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Chat ID: {chat_id}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("chatid", show_chat_id))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback_query))

    app.run_polling()

if __name__ == '__main__':
    main()
"""

with open("my-telegram-bot/bot.py", "w") as f:
    f.write(bot_code)

# Create requirements.txt
requirements = """
python-telegram-bot==20.7
"""

with open("my-telegram-bot/requirements.txt", "w") as f:
    f.write(requirements)

# Create render.yaml
render_yaml = """
services:
  - type: web
    name: telegram-bot
    env: python
    plan: free
    buildCommand: ""
    startCommand: "python bot.py"
"""

with open("my-telegram-bot/render.yaml", "w") as f:
    f.write(render_yaml)

# Create README.txt
readme_content = """
# Telegram Bot Deployment on Render

## Project Structure


