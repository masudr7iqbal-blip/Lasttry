# ────────────────────────────────────────────────
#                  কনফিগারেশন
# ────────────────────────────────────────────────

API_TOKEN = '8530900754:AAFiFRX60Om1r485mTSdiEs37rvvjz78NbI'

CHANNELS = [
    '-1003708243060',
    '-1003831376808',
    # আরও চ্যানেল ID যোগ করতে পারো
]

CHANNEL_LINKS = [
    'https://t.me/+cv_IIV016XljNDMx',
    'https://t.me/+n46o9tlogDVhMDMx',
    'https://t.me/+YlNW7n3rYsE4M2Mx',
]

ADMIN_USERNAME = "XpremiumB"          # t.me/XpremiumB
ADMIN_ID = 8153774922                 # তোমার আসল টেলিগ্রাম আইডি

STORAGE_BOT_URL = "https://t.me/AlphaStorageBot?start=demo123"
BOT_USERNAME = "AlphapremiumB_bot"

# ────────────────────────────────────────────────
#               প্রিমিয়াম + এক্সক্লুসিভ টেক্সট
# ────────────────────────────────────────────────

WELCOME_TEXT = (
    "🌟 **WELCOME TO THE INNER CIRCLE** 🌟\n\n"
    "হ্যালো {name} —\n"
    "তুমি এখন শুধুমাত্র **সিলেক্টেড ফিউ** এর জন্য রাখা এক্সক্লুসিভ জোনের ভেতরে ঢুকে পড়েছ।\n\n"
    "এখান থেকে শুরু করো ↓"
)

FORCE_JOIN_TEXT = (
    "🔐 **VIP ACCESS LOCKED** 🔐\n\n"
    "এই এক্সক্লুসিভ কনটেন্ট শুধুমাত্র আমাদের **প্রাইভেট সার্কেল**-এর মেম্বারদের জন্য।\n"
    "নিচের চ্যানেলগুলোতে জয়েন করে **আনলক** করো।\n\n"
    "জয়েন শেষ হলে → **I'm Ready ✅** চাপো — অটো ভিতরে চলে আসবে!"
)

PREMIUM_TEXT = (
    "✦ **ELITE MEMBERSHIP** ✦\n\n"
    "• Zero Ads | Pure Experience\n"
    "• Lightning Fast Downloads\n"
    "• Unlimited Premium Files\n"
    "• Early Access to New Drops\n"
    "• Private Support Line\n\n"
    "এই লেভেলের এক্সেস চাও? → এডমিনের সাথে কথা বলো"
)

HELP_TEXT = (
    "🛠 **কমান্ড লিস্ট** 🛠\n\n"
    "/start  →  মূল মেনু + এক্সেস চেক\n"
    "/help   →  এই মেসেজটা দেখাবে\n\n"
    "💎 প্রিমিয়াম ফিচার চাও?\n"
    "→ /start চালিয়ে **প্রিমিয়াম কিনুন** বাটনে ক্লিক করো\n\n"
    "কোনো সমস্যা হলে → @{admin}\n"
    "Enjoy the exclusive zone 🔥"
)

# ────────────────────────────────────────────────

bot = telebot.TeleBot(API_TOKEN, threaded=False)

# Flask server to keep Render alive
app = Flask('')

@app.route('/')
def home():
    return "Telegram Bot is alive ✓"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run_flask, daemon=True).start()

# ────────────────────────────────────────────────
#             ফোর্স জয়েন চেক
# ────────────────────────────────────────────────

def is_user_subscribed(user_id: int) -> bool:
    for channel_id in CHANNELS:
        try:
            member = bot.get_chat_member(channel_id, user_id)
            if member.status not in ['member', 'administrator', 'creator', 'restricted']:
                return False
        except Exception as e:
            print(f"চ্যানেল চেক ত্রুটি {channel_id}: {e}")
            return False
    return True

# ────────────────────────────────────────────────
#               হ্যান্ডলার
# ────────────────────────────────────────────────

@bot.message_handler(commands=['start'])
def cmd_start(message):
    user = message.from_user
    name = user.first_name or "বন্ধু"

    if is_user_subscribed(user.id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("✨ Unlock Demo Vault", url=STORAGE_BOT_URL),
            types.InlineKeyboardButton("👑 Claim Elite Access", callback_data="premium")
        )
        bot.send_message(
            message.chat.id,
            WELCOME_TEXT.format(name=name),
            reply_markup=markup,
            parse_mode="Markdown"
        )
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, link in enumerate(CHANNEL_LINKS, 1):
            markup.add(types.InlineKeyboardButton(f"✦ Join Private Channel {i} ✦", url=link))
        
        markup.add(types.InlineKeyboardButton("I'm Ready ✅ | Unlock Now", callback_data="check_join"))
        
        bot.send_message(
            message.chat.id,
            FORCE_JOIN_TEXT,
            reply_markup=markup,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(
        message.chat.id,
        HELP_TEXT.format(admin=ADMIN_USERNAME),
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id

    if call.data == "check_join":
        if is_user_subscribed(user_id):
            bot.answer_callback_query(call.id, "🎉 আনলক সাকসেস! ভিতরে চলো 🔥", show_alert=False)
            
            name = call.from_user.first_name or "বন্ধু"
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("✨ Unlock Demo Vault", url=STORAGE_BOT_URL),
                types.InlineKeyboardButton("👑 Claim Elite Access", callback_data="premium")
            )
            # পুরোনো মেসেজ এডিট করে ওয়েলকাম দেখানো (ক্লিন অভিজ্ঞতা)
            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=WELCOME_TEXT.format(name=name),
                    reply_markup=markup,
                    parse_mode="Markdown"
                )
            except:
                # যদি এডিট না হয় (পুরোনো মেসেজ ডিলিট হয়ে গেলে)
                bot.send_message(
                    call.message.chat.id,
                    WELCOME_TEXT.format(name=name),
                    reply_markup=markup,
                    parse_mode="Markdown"
                )
        else:
            bot.answer_callback_query(
                call.id,
                "আপনি এখনো সব চ্যানেলে জয়েন করেননি 😕\nদয়া করে চেক করুন!",
                show_alert=True
            )

    elif call.data == "premium":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("👑 Talk to Elite Manager", url=f"https://t.me/{ADMIN_USERNAME}")
        )
        bot.send_message(
            call.message.chat.id,
            PREMIUM_TEXT,
            reply_markup=markup,
            parse_mode="Markdown"
        )
        bot.answer_callback_query(call.id)

# ────────────────────────────────────────────────

if __name__ == "__main__":
    keep_alive()
    print("Bot starting with updated design...")
    try:
        bot.infinity_polling(timeout=15, long_polling_timeout=10)
    except Exception as e:
        print(f"Polling stopped → {e}")
