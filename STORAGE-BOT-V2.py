import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot Token
BOT_TOKEN = "7673094518:AAFq1wAix5NBiQBIlf6Y-W5xMC_k_k_yrxI"
bot = telebot.TeleBot(BOT_TOKEN)

# Admin ID
ADMIN_ID = 6043602577

# Global File Storage (Accessible by all users)
global_storage = {}

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    # Inline keyboard
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("📁 My Storage", callback_data='my_storage'))
    markup.row(InlineKeyboardButton("💎 Subscription", callback_data='subscription'))
    markup.row(InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/CN_X_OWNER"))
    markup.row(InlineKeyboardButton("📢 Developer Channel", url="https://t.me/ChiragNetwork_930"))
    markup.row(InlineKeyboardButton("💽 Database: CR INNOVATIONS PVT LTD CRR CLOUD STORE V2", callback_data='database'))

    bot.send_message(user_id, "🚀 Welcome to CR Cloud Store V2! Manage your files easily and securely.", reply_markup=markup)

# File Upload and Code Generation
@bot.message_handler(content_types=["document", "photo", "video", "audio"])
def save_file(message):
    # Unique short file code
    file_code = str(abs(hash(str(message.message_id))))[:6]

    # Identify file type and get file_id
    file_id = None
    file_type = None

    if message.document:
        file_id = message.document.file_id
        file_type = 'document'
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = 'photo'
    elif message.video:
        file_id = message.video.file_id
        file_type = 'video'
    elif message.audio:
        file_id = message.audio.file_id
        file_type = 'audio'

    if not file_id:
        bot.send_message(message.chat.id, "❌ Unable to save the file. Unsupported file type.")
        return

    # Save file globally
    global_storage[file_code] = {
        "file_id": file_id,
        "file_type": file_type
    }

    # Confirming file saved
    bot.send_message(message.chat.id, f"✅ File saved successfully!\n\n`'{file_code}'`\n\n📝 Use Command: `/getfile '{file_code}'`\n\n📤 Share this code to access your file easily!")

# Get File by Code
@bot.message_handler(commands=['getfile'])
def get_file(message):
    try:
        file_code = message.text.split()[1].strip("'")

        file_data = global_storage.get(file_code)

        if not file_data:
            bot.send_message(message.chat.id, "❌ File not found or invalid code.")
            return

        if file_data['file_type'] == 'document':
            bot.send_document(message.chat.id, file_data['file_id'])
        elif file_data['file_type'] == 'photo':
            bot.send_photo(message.chat.id, file_data['file_id'])
        elif file_data['file_type'] == 'video':
            bot.send_video(message.chat.id, file_data['file_id'])
        elif file_data['file_type'] == 'audio':
            bot.send_audio(message.chat.id, file_data['file_id'])

    except IndexError:
        bot.send_message(message.chat.id, "⚠️ Please use the correct format: `/getfile 'CODE'`")

# Admin-Only Upgrade Command
@bot.message_handler(commands=['upgrade'])
def upgrade(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "🚫 You are not authorized to use this command.")
        return

    try:
        _, user_id, plan = message.text.split()
        user_id = int(user_id)
        bot.send_message(user_id, f"🎉 Congratulations! Your storage plan has been upgraded to **{plan}**!")
        bot.send_message(message.chat.id, f"✅ User `{user_id}` successfully upgraded to **{plan}**.")
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Usage: `/upgrade <user_id> <plan>`\nExample: `/upgrade 123456789 2GB`")

# Callbacks for Inline Buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'my_storage':
        files = global_storage.keys()
        if not files:
            bot.send_message(call.from_user.id, "📂 Storage is empty.")
        else:
            for code in files:
                markup = InlineKeyboardMarkup()
                markup.row(
                    InlineKeyboardButton("🗑 Delete", callback_data=f"delete_{code}"),
                    InlineKeyboardButton("📋 File Code", callback_data=f"code_{code}")
                )
                bot.send_message(call.from_user.id, f"📁 File Code: `{code}`", reply_markup=markup)

    elif call.data == 'subscription':
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("💼 1GB Plan - ₹50", callback_data='plan_1gb'))
        markup.row(InlineKeyboardButton("📦 2GB Plan - ₹100", callback_data='plan_2gb'))
        markup.row(InlineKeyboardButton("📲 Contact Admin", url="https://t.me/CN_X_OWNER"))
        bot.send_message(call.from_user.id, "💎 Choose a subscription plan or contact admin for custom plans.", reply_markup=markup)

    elif call.data.startswith("delete_"):
        code = call.data.split("_")[1]
        if code in global_storage:
            del global_storage[code]
            bot.send_message(call.from_user.id, f"🗑 File `{code}` deleted successfully.")

    elif call.data.startswith("code_"):
        code = call.data.split("_")[1]
        bot.send_message(call.from_user.id, f"📋 File Code: `{code}`")

    elif call.data == 'database':
        bot.send_message(call.from_user.id, "💽 Database: **CR INNOVATIONS PVT LTD CRR CLOUD STORE V2**")

# Polling the bot
bot.polling()