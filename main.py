import telebot
from telebot import types

# আপনার টোকেন
API_TOKEN = '8530900754:AAH-xyYJ1etm88QW2A_O3CabD5heC0-1Asc'
# আপনার চ্যানেল আইডিগুলো
CHANNELS = ['-1003731836152', '-1003831376808'] 
CHANNEL_LINKS = ['https://t.me/+YJGx3ZCvX1g5Yzlh', 'https://t.me/+YlNW7n3rYsE4M2Mx']

bot = telebot.TeleBot(API_TOKEN)

def is_subscribed(user_id):
    for chat_id in CHANNELS:
        try:
            member = bot.get_chat_member(chat_id, user_id)
            if member.status in ['left', 'kicked']: return False
        except: return False
    return True

@bot.message_handler(commands=['start'])
def welcome(message):
    if is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎬 Watch Demo", callback_data="demo"))
        markup.add(types.InlineKeyboardButton("💎 Buy Premium", callback_data="buy"))
        bot.send_message(message.chat.id, f"স্বাগতম! আপনার এক্সেস আনলক হয়েছে। 🔥", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        for i, link in enumerate(CHANNEL_LINKS):
            markup.add(types.InlineKeyboardButton(f"Join Channel {i+1} 📢", url=link))
        markup.add(types.InlineKeyboardButton("Joined ✅", callback_data="verify"))
        bot.send_message(message.chat.id, "⚠️ আগে আমাদের চ্যানেলগুলোতে জয়েন করুন!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.answer_callback_query(call.id, "ধন্যবাদ! ✅")
            welcome(call.message)
        else:
            bot.answer_callback_query(call.id, "⚠️ আগে জয়েন করুন!", show_alert=True)

if __name__ == "__main__":
    bot.infinity_polling()
