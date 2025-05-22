
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

# Bot token
TOKEN = '7640462025:AAHtwENanJ-UUenKeJA8YnFWetMrAplFq4A'

# Group chat IDs
group_chat_ids = [
    '-4938012309',
    '-4613148577',
    '-4829453971',
    '-4935109561',
    '-4917561606',
]

# Dictionary to store user-agent mapping
user_agent_mapping = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text('សូមផ្ញើសារមកខ្ញុំ!')

def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_message = update.message.text

    keyboard = [
        [InlineKeyboardButton("✅ Claim", callback_data=f"claim_{user_id}"),
         InlineKeyboardButton("💬 Reply", callback_data=f"reply_{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    for group_id in group_chat_ids:
        context.bot.send_message(
            chat_id=group_id,
            text=f"សារពីអ្នកប្រើ {user_id}: {user_message}",
            reply_markup=reply_markup
        )

def handle_callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data
    agent_id = query.from_user.id

    if query_data.startswith("claim_"):
        user_id = query_data.split("_")[1]
        user_agent_mapping[user_id] = {"agent_id": agent_id, "group_id": query.message.chat_id}
        query.answer(f"អ្នកបាន Claim សារពី user {user_id}។")
    elif query_data.startswith("reply_"):
        user_id = query_data.split("_")[1]
        if user_agent_mapping.get(user_id) and user_agent_mapping[user_id]["agent_id"] == agent_id:
            query.message.reply_text(f"សូមឆ្លើយតបទៅ user {user_id}:")
        else:
            query.answer("អ្នកត្រូវ Claim សារមុនសិន។")

def show_chat_id(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    update.message.reply_text(f"Chat ID: {chat_id}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("chatid", show_chat_id))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(handle_callback_query))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
