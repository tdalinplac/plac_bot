import os
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters, WebhookHandler
)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Load bot token from environment
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Group chat IDs
group_chat_ids = [
    '-4938012309',
    '-4613148577',
    '-4829453971',
    '-4935109561',
    '-4917561606',
]

# Store user-agent mapping
user_agent_mapping = {}

# Flask app
app = Flask(__name__)

# Telegram bot app
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
webhook_handler = WebhookHandler(bot_app)

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('សួស្តី! ខ្ញុំជាបុត Telegram របស់អ្នក។')

async def show_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Chat ID: {update.message.chat_id}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text

    keyboard = [
        [InlineKeyboardButton("✅ Claim", callback_data=f"claim_{user_id}"),
         InlineKeyboardButton("💬 Reply", callback_data=f"reply_{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if str(user_id) in user_agent_mapping:
        group_id = user_agent_mapping[str(user_id)]["group_id"]
        await context.bot.send_message(chat_id=group_id, text=f"សារថ្មីពី user {user_id}: {user_message}")
    else:
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

# Register handlers
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("chatid", show_chat_id))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
bot_app.add_handler(CallbackQueryHandler(handle_callback_query))

# Webhook route
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    try:
        await webhook_handler.handle_update(request)
    except Exception as e:
        logging.exception("Error while processing update:")
    return "ok"

@app.route("/")
def index():
    return "Bot is running!"
