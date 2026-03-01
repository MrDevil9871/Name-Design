import os
import json
import time
from threading import Thread
from flask import Flask
import telebot
from telebot import types
from dotenv import load_dotenv

# .env file load karna (Sirf local testing ke liye, Render par Env Vars use honge)
load_dotenv()

# ===============================
# WEB SERVER FOR RENDER (Keep-Alive)
# ===============================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Uptimerobot favicon error fix

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ===============================
# CONFIGURATION FROM ENV
# ===============================
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

bot = telebot.TeleBot(TOKEN)
DESIGNS_FILE = "my_designs.json"
USERS_FILE = "users.json"

# ===============================
# DATA SYSTEM
# ===============================
default_designs = {
    "1": [

"🤍 ⍣⃪‌ {} ❛𝆺𝅥𓆪ꪾ™",
"🔥 {} 🝐",
"➺ {} ✦",
"❛ {} 💗",
"🐼 {}",
"🦁 {} ⚡",
"𓆰⎯꯭꯭֯‌{}𓂃ֶꪳ 𓆩〭〬🔥𓆪ꪾ",
".𝁘ໍ⎯꯭‌- {} ⌯ 𝘅𝗗 𓂃⎯꯭‌ ִֶָ ֺ🎀",
"𓂃❛ ⟶‌{} ❜ 🌙⤹🌸",
"🍹𝆺𝅥⃝🤍 ‌⃪‌ ᷟ●{}🤍᪳𝆺꯭𝅥⎯꯭‌⎯꯭",
"⋆⎯፝֟፝֟⎯᪵ 𝆺꯭𝅥{} ᭄꯭🦋꯭᪳᪳᪻⎯‌⎯🐣",
"⟶‌ꭙ⋆🔥𓆩〬 {}⎯᳝֟፝֟⎯‌ꭙ⋆🔥",
"❛ .𝁘ໍ{}ꨄ 🦋𓂃•",
"⏤‌‌ {}𓂃 🔥𝆺𝅥 🜲 ⌯",
"ᯓ𓆰𝅃🔥{}⍣꯭꯭𓆪꯭🝐",
"➺ ‌⃪⃜ {}✦ 𝆺𝅥⎯ꨄ",
"𓆩❥⃝🌸{}🌸⃝❥𓆪",
"◄⏤❥⃝🦋{}🦋⃝❥⏤►",
"𓄂𝆺𝅥⃝🥀{}🥀⃝𝆺𝅥𓄂",
"❍─⃜𓆩🤍{}🤍𓆪⃜─❍",
"🦋⃟≛⃝⋆ {} ⋆⃝≛⃟🦋",
"𓆩🔥⃝ {} ⃝🔥𓆪",
"𓆩⍣⃝💖{}💖⃝⍣𓆪",
"❍⏤● {} ●───♫▷",
"⛦⃕𝄟🦋{}🦋𝄟⃕⛦",
"◄⏤🝛꯭ {} ꯭🝛⏤►",
"𓆩❤️🔥 {} 🔥❤️𓆪",
"••ᯓ❥๋{}࿐❥ᯓ••",
"❝🍷{}🍷❞",
"𓍼💗 {} 💗⌯™",
"𓆰꯭❛ {} ❜꯭𓆪",
"❍─⃜𓆩👑 {} 👑𓆪⃜─❍",
"°ꗝ༎ࠫ {} ࠫ༎ꗝ°",
"◄⏤🫧⃝ {} ⃝🫧⏤►",
"𓆩🪽⃝ {} ⃝🪽𓆪",
"𓆩🥀⃝ {} ⃝🥀𓆪",
"𓄂─⃛𓆩✨ {} ✨𓆪⃛─𓄂",
"◄⏤🖤⃝ {} ⃝🖤⏤►",
"𓆩🦚⃝ {} ⃝🦚𓆪",
"❥⃝꯭✿ {} ✿꯭⃝❥",
"𓆩🌙⃝ {} ⃝🌙𓆪",
"◄⏤⚡⃝ {} ⃝⚡⏤►",
"𓆩🎧⃝ {} ⃝🎧𓆪",
"𓆩💫⃝ {} ⃝💫𓆪",
"◄⏤👑⃝ {} ⃝👑⏤►",
"𓆩🕊⃝ {} ⃝🕊𓆪",
"❍─⃜𓆩💎 {} 💎𓆪⃜─❍",
"◄⏤💥⃝ {} ⃝💥⏤►",
"𓆩🍷⃝ {} ⃝🍷𓆪",
"❥⃝🔥 {} 🔥⃝❥",
"𓆩😈⃝ {} ⃝😈𓆪",
"◄⏤😎⃝ {} ⃝😎⏤►",
"𓆩💀⃝ {} ⃝💀𓆪",
"◄⏤☠⃝ {} ⃝☠⏤►",
"𓆩🌹⃝ {} ⃝🌹𓆪",
"◄⏤🌸⃝ {} ⃝🌸⏤►",
"𓆩🦅⃝ {} ⃝🦅𓆪"

],
    "2": [
        "🔥 {} ⚔️ {} 🔥", "👑 {} ✨ {} 👑", "꧁ {} 💎 {} ꧂", 
        "⚡ {} 🦁 {} ⚡", "🦅 {} 🌀 {} 🦅", "💀 {} 🐉 {} 💀",
        "🌙 {} 🌸 {} 🌙", "🚀 {} 🛸 {} 🚀", "🦁 {} 🦁 {} 🦁", "💎 {} 💎 {} 💎"
    ]
}

def load_data(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return default
    return default

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

designs = load_data(DESIGNS_FILE, default_designs)
users = load_data(USERS_FILE, [])
user_sessions = {}

def add_user(user_id):
    if user_id not in users:
        users.append(user_id)
        save_data(USERS_FILE, users)

# ===============================
# FONT ENGINE (5 FONTS)
# ===============================
def apply_font(text, font_type):
    text = text.lower()
    m = {
        "block": {'a': '🅻', 'b': '🅱️', 'c': '🅲', 'd': '🅳', 'e': '🅴', 'f': '🅵', 'g': '🅶', 'h': '🅷', 'i': '🅸', 'j': '🅹', 'k': '🅺', 'l': '🅻', 'm': '🅼', 'n': '🅽', 'o': '🅾️', 'p': '🅿️', 'q': '🆀', 'r': '🆁', 's': '🆂', 't': '🆃', 'u': '🆄', 'v': '🆅', 'w': '🆆', 'x': '🆇', 'y': '🆈', 'z': '🆉', '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'},
        "circle": {'a': '🅐', 'b': '🅑', 'c': '🅒', 'd': '🅓', 'e': '🅔', 'f': '🅕', 'g': '🅖', 'h': '🅗', 'i': '🅘', 'j': '🅙', 'k': '🅚', 'l': '🅛', 'm': '🅜', 'n': '🅝', 'o': '🅞', 'p': '🅟', 'q': '🅠', 'r': '🅡', 's': '🅢', 't': '🅣', 'u': '🅤', 'v': '🅥', 'w': '🅦', 'x': '🅧', 'y': '🅨', 'z': '🅩', '0': '⓿', '1': '❶', '2': '❷', '3': '❸', '4': '❹', '5': '❺', '6': '❻', '7': '❼', '8': '❽', '9': '❾'},
        "square": {'a': '🄰', 'b': '🄱', 'c': '🄲', 'd': '🄳', 'e': '🄴', 'f': '🄵', 'g': '🄶', 'h': '🄷', 'i': '🄸', 'j': '🄹', 'k': '🄺', 'l': '🄻', 'm': '🄼', 'n': '🄽', 'o': '🄾', 'p': '🄿', 'q': '🅀', 'r': '🅁', 's': '🅂', 't': '🅃', 'u': '🅄', 'v': '🅅', 'w': '🅆', 'x': '🅇', 'y': '🅈', 'z': '🅉', '0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9'},
        "small": {'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'},
        "wild": {'a': 'ค', 'b': '๒', 'c': 'ς', 'd': '๔', 'e': 'є', 'f': 'Ŧ', 'g': 'ﻮ', 'h': 'ђ', 'i': 'เ', 'j': 'ן', 'k': 'к', 'l': 'ɭ', 'm': '๓', 'n': 'ภ', 'o': '๏', 'p': 'ק', 'q': 'ợ', 'r': 'г', 's': 'ร', 't': 'Շ', 'u': 'ย', 'v': 'ง', 'w': 'ฬ', 'x': 'א', 'y': 'ץ', 'z': 'չ'}
    }
    target = m.get(font_type, {})
    return "".join(target.get(c, c) for c in text)

# ===============================
# BOT HANDLERS
# ===============================

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    add_user(message.from_user.id)
    bot.send_message(message.chat.id, "✨ **Stylish Name Editor Online!**\n\nUse `/name [your name]` to get started.\n*Example:* `/name Rahul` or `/name Rahul King`", parse_mode="Markdown")

@bot.message_handler(commands=['name'])
def name_cmd(message):
    if message.chat.type != "private":
        return bot.reply_to(message, "❌ Use me in Private Chat!")
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return bot.reply_to(message, "❗ Please provide a name. Example: `/name Rahul`")
    
    user_sessions[message.from_user.id] = {"text": args[1], "page": 0}
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("1️⃣ One Word Filter", callback_data="sel_1"),
        types.InlineKeyboardButton("2️⃣ Two Word Filter", callback_data="sel_2")
    )
    bot.send_message(message.chat.id, f"👤 **Input:** `{args[1]}`\nSelect Filter Type:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("sel_"))
def select_filter(call):
    mode = call.data.split("_")[1]
    u_id = call.from_user.id
    if u_id not in user_sessions: return
    user_sessions[u_id]["mode"] = mode
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🅰️ Block", callback_data="f_block"),
        types.InlineKeyboardButton("🟢 Circle", callback_data="f_circle"),
        types.InlineKeyboardButton("⬜ Square", callback_data="f_square"),
        types.InlineKeyboardButton("ᴛɪɴʏ Small", callback_data="f_small"),
        types.InlineKeyboardButton("ค๒ Wild", callback_data="f_wild")
    )
    bot.edit_message_text("🎨 **Select Font Style:**", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("f_"))
def handle_font(call):
    font = call.data.split("_")[1]
    u_id = call.from_user.id
    if u_id not in user_sessions: return
    user_sessions[u_id]["font"] = font
    user_sessions[u_id]["page"] = 0
    show_designs(call.message, u_id)

def show_designs(message, u_id):
    data = user_sessions.get(u_id)
    text, font, page, mode = data["text"], data["font"], data["page"], data["mode"]
    words = text.split()
    
    if mode == "1": styled = [apply_font(text, font)]
    else:
        if len(words) < 2:
            return bot.send_message(message.chat.id, "⚠️ Need at least 2 words for this filter.")
        styled = [apply_font(words[0], font), apply_font(" ".join(words[1:]), font)]

    target_list = designs.get(mode, [])
    start, end = page * 10, (page + 1) * 10
    current = target_list[start:end]

    if not current:
        return bot.send_message(message.chat.id, "🏁 No more designs available!")

    try: bot.delete_message(message.chat.id, message.message_id)
    except: pass

    for d in current:
        try: bot.send_message(message.chat.id, f"`{d.format(*styled)}`", parse_mode="Markdown")
        except: continue

    if len(target_list) > end:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Next 10 Designs ➡️", callback_data="next_p"))
        bot.send_message(message.chat.id, f"Page {page+1} finished.", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "🏁 End of list.")

@bot.callback_query_handler(func=lambda call: call.data == "next_p")
def next_page(call):
    u_id = call.from_user.id
    if u_id in user_sessions:
        user_sessions[u_id]["page"] += 1
        show_designs(call.message, u_id)

# Admin Broadcast
@bot.message_handler(func=lambda m: m.text.startswith("!message") and m.from_user.id == OWNER_ID)
def broadcast(message):
    msg_text = message.text.replace("!message", "").strip()
    if not msg_text: return
    sent = 0
    for u in users:
        try:
            bot.send_message(u, msg_text)
            sent += 1
        except: continue
    bot.reply_to(message, f"✅ Broadcast sent to {sent} users.")

# Admin Add/Remove
@bot.message_handler(func=lambda m: (m.text.startswith("!add") or m.text.startswith("!remove")) and m.from_user.id == OWNER_ID)
def admin_manage(message):
    try:
        parts = message.text.split(maxsplit=2)
        cmd, mode, content = parts[0], parts[1], parts[2]
        if cmd == "!add":
            designs[mode].append(content)
            save_data(DESIGNS_FILE, designs)
            bot.reply_to(message, f"✅ Added to Filter {mode}")
        else:
            designs[mode].remove(content)
            save_data(DESIGNS_FILE, designs)
            bot.reply_to(message, "🗑️ Removed successfully.")
    except Exception as e: bot.reply_to(message, f"❌ Error: {str(e)}")

# ===============================
# MAIN EXECUTION (Updated for Gunicorn)
# ===============================

# Ye function bot ko alag se chalayega
def start_bot():
    print("🤖 Bot Polling Started...")
    bot.infinity_polling(skip_pending=True)

# Gunicorn jab 'app' ko load karega, tabhi bot start ho jaye
from threading import Thread
bot_thread = Thread(target=start_bot)
bot_thread.daemon = True
bot_thread.start()

if __name__ == "__main__":
    # Local testing ke liye (Render par gunicorn ise ignore karta hai)
    app.run(host='0.0.0.0', port=8080)
                     
