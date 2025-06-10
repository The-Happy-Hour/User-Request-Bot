from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import info
from info import *

app = Client("request_bot", api_id=info.API_ID, api_hash=info.API_HASH, bot_token=info.BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_hendle(client, message):
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("The Happy Hour 🌿", url="https://t.me/The_Happy_Hours")]
    ])
    message.reply("**I am the bot who send your request to my admin and infrom you when admin infrom me...\n\nExample: /request Avatar or #request Avatar 2009**", reply_markup=button)
    return

@app.on_message(filters.command("request") | filters.regex(r"#request"))
def handle_request(client, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username or "Unknown"
    request_text = message.text.split(" ", 1)[-1] if " " in message.text else None

    if not request_text:
        message.reply_text("Example: /request Avatar movie or #request Avatar 2009")
        return

    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Accepted", callback_data=f"accepted_{message.chat.id}_{user_id}"),
         InlineKeyboardButton("❌ Invalide", callback_data=f"invalide_{message.chat.id}_{user_id}")],
        [InlineKeyboardButton("⚠️ Seplling", callback_data=f"spelling_{message.chat.id}_{user_id}"),
         InlineKeyboardButton("🗑️ Unavailabe", callback_data=f"unavailable_{message.chat.id}_{user_id}")]
    ])

    client.send_message(ADMIN_ID, f"🎏 **User**: [{name}](tg://user?id={user_id})\n🪪 **Userid**: {user_id}\n👤 **Username**: @{username}\n📌 **Request**: `{request_text}`", reply_markup=button)
    message.reply_text("**Your request has been sent to <a href='http://67.220.85.157:6245/twTeEV'>admin</a>**")

@app.on_callback_query()
def handle_response(client, callback_query):
    data, chat_id, user_id = callback_query.data.split("_")
    user_id = int(user_id)
    chat_id = int(chat_id)

    response_messages = {
        "accepted": "**Your requested file has been added on <a href='http://67.220.85.157:6245/X9bpVE'>bot</a>**",
        "invalide": "**Your requests is not in <a href='http://67.220.85.157:6245/52Lhxy'>valide formate</a>**",
        "spelling": "**We found seplling mistek on your request\nso <a href='http://67.220.85.157:6245/GQ7aw0'>please check your speliing</a>**",
        "unavailable": "**Your requested file is <a href='http://67.220.85.157:6245/GQ7aw0'>not available</a>**",
    }

    if data in response_messages:
        if chat_id < 0:  
            client.send_message(chat_id, f"Admin: [{callback_query.from_user.first_name}](tg://user?id={user_id})\nText: {response_messages[data]}")
        else:
            client.send_message(user_id, response_messages[data])
    callback_query.answer("Done ✅")

app.run()
print("Bot Started ✅")