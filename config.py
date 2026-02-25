# config.py - তোমার সম্পূর্ণ কনফিগ (এটাই paste করো)

API_ID = 38193466
API_HASH = "1adc121d2a3cb83d6ab2e42222777312"
BOT_TOKEN = "8312471333:AAGv-khgZKCcSugeOowEKUsyih2exWPpZaM"

OWNER_ID = 8153774922
ADMINS = [OWNER_ID]

CHANNEL_ID = -1003574306216
LOG_CHANNEL = -1003574306216

FORCE_SUB = True
FORCE_SUB_CHANNEL = "-1003731836152,-1008312471333"  # comma দিয়ে দুটো চ্যানেল

MONGO_URL = "mongodb+srv://masudr7iqbal_db_user:VCewSYPaiIxlnjz6@cluster0.mp2hbsi.mongodb.net/masudr7iqbal?retryWrites=true&w=majority"

# যদি repo-তে DATABASE_URL নামে variable থাকে তাহলে এটাও যোগ করো
DATABASE_URL = MONGO_URL

# Render-এর জন্য (যদি লাগে)
PORT = 8080
DEBUG = False
