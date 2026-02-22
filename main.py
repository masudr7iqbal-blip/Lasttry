import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# --- কনফিগারেশন ---
API_TOKEN = '8530900754:AAH-xyYJ1etm88QW2A_O3CabD5heC0-1Asc'
# আপনার চ্যানেল আইডিগুলো (নিশ্চিত করুন বট এখানে এডমিন)
CHANNELS = ['-1003731836152', '-1003831376808'] 
CHANNEL_LINKS = ['https://t.me/+YJGx3ZCvX1g5Yzlh', 'https://t.me/+YlNW7n3rYsE4M2Mx']
ADMIN_USERNAME = "Your_Telegram_Username" # @ ছাড়া আপনার ইউজারনেম দিন (প্রিমিয়াম কেনার জন্য)
STORAGE_BOT_URL = "https://t.me/AlphaStorageBot?start=demo123" # আপনার ডেমো ভিডিও লিঙ্ক

bot = telebot.TeleBot(API_TOKEN, threaded=False)

# --- রেন্ডার যাতে বন্ধ না হয় (Keep Alive) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- ফোর্স জয়েন চেক ফাংশন ---
def is_subscribed(user_id):
    for chat_id in CHANNELS:
        try:
            member = bot.get_chat_member(chat_id, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    return True

# --- স্টার্ট কমান্ড ---
@bot.message_handler(commands=['start'])
def welcome(message):
    if is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎬 Watch Demo", url=STORAGE_BOT_URL))
        markup.add(types.InlineKeyboardButton("💎 Buy Premium", callback_data="buy"))
        bot.send_message(message.chat.id, f"✅ **স্বাগতম {message.from_user.first_name}!**\n\nআপনার এক্সেস আনলক হয়েছে। নিচের বাটন থেকে ডেমো দেখুন বা প্রিমিয়াম কিনুন।", reply_markup=markup, parse_mode="Markdown")
    else:
        markup = types.InlineKeyboardMarkup()
        for i, link in enumerate(CHANNEL_LINKS):
            markup.add(types.InlineKeyboardButton(f"Join Channel {i+1} 📢", url=link))
        markup.add(types.InlineKeyboardButton("Joined ✅", callback_data="verify"))
        bot.send_message(message.chat.id, "⚠️ **এক্সেস ডিনাইড!**\n\nবটটি ব্যবহার করতে আমাদের নিচের চ্যানেলগুলোতে জয়েন থাকতে হবে।", reply_markup=markup, parse_mode="Markdown")

# --- বাটন হ্যান্ডলার ---
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.answer_callback_query(call.id, "ধন্যবাদ! ✅")
            welcome(call.message)
        else:
            bot.answer_callback_query(call.id, "⚠️ আপনি এখনো সব চ্যানেলে জয়েন করেননি!", show_alert=True)
    
    elif call.data == "buy":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💬 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}"))
        bot.send_message(call.message.chat.id, "💎 **Premium Features:**\n\n✅ Ad-free experience\n✅ Fast downloading\n✅ Unlimited access\n\nপ্রিমিয়াম কিনতে এডমিনের সাথে যোগাযোগ করুন।", reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    keep_alive() # সার্ভার চালু করবে
    print("Bot is starting...")
    bot.infinity_polling()
