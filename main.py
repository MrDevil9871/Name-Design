import os
import json
import time
from threading import Thread
from flask import Flask
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

# ===============================
# CONFIGURATION
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
        "🤍 ⍣⃪‌ {} ❛𝆺𝅥𓆪ꪾ™", "🔥 {} 🝐", "➺ {} ✦", "❛ {} 💗", "🐼 {}", "🦁 {} ⚡",
        "𓆰⎯꯭꯭֯‌{}𓂃ֶꪳ 𓆩〭〬🔥𓆪ꪾ", ".𝁘ໍ⎯꯭‌- {} ⌯ 𝘅𝗗 𓂃⎯꯭‌ ִֶָ ֺ🎀", "𓂃❛ ⟶‌{} ❜ 🌙⤹🌸",
        "🍹𝆺𝅥⃝🤍 ‌⃪‌ ᷟ●{}🤍᪳𝆺꯭𝅥⎯꯭‌⎯꯭", "⋆⎯፝֟፝֟⎯᪵ 𝆺꯭𝅥{} ᭄꯭🦋꯭᪳᪳᪻⎯‌⎯🐣", "⟶‌ꭙ⋆🔥𓆩〬 {}⎯᳝֟፝֟⎯‌ꭙ⋆🔥"
    ],
    "2": [
        "🔥 {} ⚔️ {} 🔥", "👑 {} ✨ {} 👑", "꧁ {} 💎 {} ꧂", 
        "⚡ {} 🦁 {} ⚡", "🦁 {} 🦁 {} 🦁"
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

# ===============================
# FONT ENGINE (All 19 Styles)
# ===============================
def apply_font(text, font_type):
    text = text.lower()
    m = {
        "block": {'a': '🅻', 'b': '🅱️', 'c': '🅲', 'd': '🅳', 'e': '🅴', 'f': '🅵', 'g': '🅶', 'h': '🅷', 'i': '🅸', 'j': '🅹', 'k': '🅺', 'l': '🅻', 'm': '🅼', 'n': '🅽', 'o': '🅾️', 'p': '🅿️', 'q': '🆀', 'r': '🆁', 's': '🆂', 't': '🆃', 'u': '🆄', 'v': '🆅', 'w': '🆆', 'x': '🆇', 'y': '🆈', 'z': '🆉'},
        "circle": {'a': '🅐', 'b': '🅑', 'c': '🅒', 'd': '🅓', 'e': '🅔', 'f': '🅕', 'g': '🅖', 'h': '🅗', 'i': '🅘', 'j': '🅙', 'k': '🅚', 'l': '🅛', 'm': '🅜', 'n': '🅝', 'o': '🅞', 'p': '🅟', 'q': '🅠', 'r': '🅡', 's': '🅢', 't': '🅣', 'u': '🅤', 'v': '🅥', 'w': '🅦', 'x': '🅧', 'y': '🅨', 'z': '🅩'},
        "square": {'a': '🄰', 'b': '🄱', 'c': '🄲', 'd': '🄳', 'e': '🄴', 'f': '🄵', 'g': '🄶', 'h': '🄷', 'i': '🄸', 'j': '🄹', 'k': '🄺', 'l': '🄻', 'm': '🄼', 'n': '🄽', 'o': '🄾', 'p': '🄿', 'q': '🅀', 'r': '🅁', 's': '🅂', 't': '🅃', 'u': '🅄', 'v': '🅅', 'w': '🅆', 'x': '🅇', 'y': '🅈', 'z': '🅉'},
        "small": {'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'},
        "wild": {'a': 'ค', 'b': '๒', 'c': 'ς', 'd': '๔', 'e': 'є', 'f': 'Ŧ', 'g': 'ﻮ', 'h': 'ђ', 'i': 'เ', 'j': 'ן', 'k': 'к', 'l': 'ɭ', 'm': '๓', 'n': 'ภ', 'o': '๏', 'p': 'ק', 'q': 'ợ', 'r': 'г', 's': 'ร', 't': 'Շ', 'u': 'ย', 'v': 'ง', 'w': 'ฬ', 'x': 'א', 'y': 'ץ', 'z': 'չ'},
        "bold_script": {'a': '𝓪', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮', 'f': '𝓯', 'g': '𝓰', 'h': '𝓱', 'i': '𝓲', 'j': '𝓳', 'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷', 'o': '𝓸', 'p': '𝓹', 'q': '𝓺', 'r': '𝓻', 's': '𝓼', 't': '𝓽', 'u': '𝓾', 'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃'},
        "monospace": {'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎', 'f': '𝚏', 'g': '𝚐', 'h': '𝚑', 'i': '𝚒', 'j': '𝚓', 'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗', 'o': '𝚘', 'p': '𝚙', 'q': '', 'r': '𝚛', 's': '𝚜', 't': '𝚝', 'u': '𝚞', 'v': '𝚟', 'w': '𝚠', 'x': '𝚡', 'y': '𝚢', 'z': '𝚣'},
        "double_struck": {'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖', 'f': '𝕗', 'g': '𝕘', 'h': '𝕙', 'i': '𝕚', 'j': '𝕛', 'k': '𝕜', 'l': '𝕝', 'm': '𝕞', 'n': '𝕟', 'o': '𝕠', 'p': '𝕡', 'q': '𝕢', 'r': '𝕣', 's': '𝕤', 't': '𝕥', 'u': '𝕦', 'v': '𝕧', 'w': '𝕨', 'x': '𝕩', 'y': '𝕪', 'z': '𝕫'},
        "italic_bold": {'a': '𝙖', 'b': '𝙗', 'c': '𝙘', 'd': '𝙙', 'e': '𝙚', 'f': '𝙛', 'g': '𝙜', 'h': '𝙝', 'i': '𝙞', 'j': '𝙟', 'k': '𝙠', 'l': '𝙡', 'm': '𝙢', 'n': '𝙣', 'o': '𝙤', 'p': '𝙥', 'q': '𝙦', 'r': '𝙧', 's': '𝙨', 't': '𝙩', 'u': '𝙪', 'v': '𝙫', 'w': '𝙬', 'x': '𝙭', 'y': '𝙮', 'z': '𝙯'},
        "bubble": {'a': 'ⓐ', 'b': 'ⓑ', 'c': 'ⓒ', 'd': 'ⓓ', 'e': 'ⓔ', 'f': 'ⓕ', 'g': 'ⓖ', 'h': 'ⓗ', 'i': 'ⓘ', 'j': 'ⓙ', 'k': 'ⓚ', 'l': 'ⓛ', 'm': 'ⓜ', 'n': 'ⓝ', 'o': 'ⓞ', 'p': 'ⓟ', 'q': 'ⓠ', 'r': 'ⓡ', 's': 'ⓢ', 't': 'ⓣ', 'u': 'ⓤ', 'v': 'ⓥ', 'w': 'ⓦ', 'x': 'ⓧ', 'y': 'ⓨ', 'z': 'ⓩ'},
        "greek": {'a': 'α', 'b': 'β', 'c': 'ψ', 'd': 'δ', 'e': 'ε', 'f': 'φ', 'g': 'γ', 'h': 'η', 'i': 'ι', 'j': 'ξ', 'k': 'κ', 'l': 'λ', 'm': 'μ', 'n': 'ν', 'o': 'ο', 'p': 'π', 'q': 'χ', 'r': 'ρ', 's': 'σ', 't': 'τ', 'u': 'υ', 'v': 'ω', 'w': 'ω', 'x': 'χ', 'y': 'υ', 'z': 'ζ'},
        "currency": {'a': '₳', 'b': '฿', 'c': '₵', 'd': 'Đ', 'e': 'Ɇ', 'f': '₣', 'g': '₲', 'h': 'Ⱨ', 'i': 'ł', 'j': 'J', 'k': '₭', 'l': 'Ⱡ', 'm': '₥', 'n': '₦', 'o': 'Ø', 'p': '₱', 'q': 'Q', 'r': 'Ɽ', 's': '₴', 't': '₮', 'u': 'Ʉ', 'v': 'V', 'w': '₩', 'x': 'Ӿ', 'y': 'Ɏ', 'z': 'Ƶ'},
        "paren": {'a': '⒜', 'b': '⒝', 'c': '⒞', 'd': '⒟', 'e': '⒠', 'f': '⒡', 'g': '⒢', 'h': '⒣', 'i': '⒤', 'j': '⒥', 'k': '⒦', 'l': '⒧', 'm': '⒨', 'n': '⒩', 'o': '⒪', 'p': '⒫', 'q': '⒬', 'r': '⒭', 's': '⒮', 't': '⒯', 'u': '⒰', 'v': '⒱', 'w': '⒲', 'x': '⒳', 'y': '⒴', 'z': '⒵'},
        "bold_sans": {'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻', 'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇'},
        "thin": {'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖', 'f': '𝕗', 'g': '𝕘', 'h': '𝕙', 'i': '𝕚', 'j': '𝕛', 'k': '𝕜', 'l': '𝕝', 'm': '𝕞', 'n': '𝕟', 'o': '𝕠', 'p': '𝕡', 'q': '𝕢', 'r': '𝕣', 's': '𝕤', 't': '𝕥', 'u': '𝕦', 'v': '𝕧', 'w': '𝕨', 'x': '𝕩', 'y': '𝕪', 'z': '𝕫'},
        "serif": {'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠', 'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧', 'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳'},
        "gothic": {'a': '𝖇', 'b': '𝖇', 'c': '𝖈', 'd': '𝖉', 'e': '𝖊', 'f': '𝖋', 'g': '𝖌', 'h': '𝖍', 'i': '𝖎', 'j': '𝖏', 'k': '𝖐', 'l': '𝖑', 'm': '𝖒', 'n': '𝖓', 'o': '𝖔', 'p': '𝖕', 'q': '𝖖', 'r': '𝖗', 's': '𝖘', 't': '𝖙', 'u': '𝖚', 'v': '𝖛', 'w': '𝖜', 'x': '𝖝', 'y': '𝖞', 'z': '𝖟'},
        "slant": {'a': '𝘢', 'b': '𝘣', 'c': '𝘤', 'd': '𝘥', 'e': '𝘦', 'f': '𝘧', 'g': '𝘨', 'h': '𝘩', 'i': '𝘪', 'j': '𝘫', 'k': '𝘬', 'l': '𝘭', 'm': '𝘮', 'n': '𝘯', 'o': '𝘰', 'p': '𝘱', 'q': '𝘲', 'r': '𝘳', 's': '𝘴', 't': '𝘵', 'u': '𝘶', 'v': '𝘷', 'w': '𝘸', 'x': '𝘹', 'y': '𝘺', 'z': '𝘻'},
        "comic": {'a': '𝓬', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮', 'f': '𝓯', 'g': '𝓰', 'h': '𝓱', 'i': '𝓲', 'j': '𝓳', 'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷', 'o': '𝓸', 'p': '𝓹', 'q': '𝓺', 'r': '𝓻', 's': '𝓼', 't': '𝓽', 'u': '𝓾', 'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃'}
    }
    target = m.get(font_type, {})
    return "".join(target.get(c, c) for c in text)

# ===============================
# BOT HANDLERS
# ===============================

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    add_user(message.from_user.id)
    first_name = message.from_user.first_name if message.from_user.first_name else "User"
    
    welcome_text = (
        f"👋 **Hey, {first_name}!**\n\n"
        "Welcome to the **Name Designer Bot**. ✨\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "📖 **Kaise Use Karein (How to Use):**\n\n"
        "1️⃣ **Single Name ke liye:**\n"
        "Type: `/name Jass` \n\n"
        "2️⃣ **Double Name (VIP Style) ke liye:**\n"
        "Type: `/name Jass Manak` \n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "🎨 *Bas apna naam bhejiye aur stylish designs paaiye!*"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['name'])
def start_name(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return bot.reply_to(message, "⚠️ **Khali naam mat bhejiye!**\nSahi tarika: `/name Jass` ya `/name Jass Manak`", parse_mode="Markdown")
    
    u_id = message.from_user.id
    user_name = args[1]
    
    # Session initialize karna
    user_sessions[u_id] = {
        "text": user_name,
        "font": "small",
        "page": 0,
        "mode": "1"
    }
    
    markup = types.InlineKeyboardMarkup()
    # Check karna agar name double hai ya single
    words = user_name.split()
    
    if len(words) >= 2:
        markup.add(
            types.InlineKeyboardButton("1️⃣ Single Filter", callback_data="sel_1"),
            types.InlineKeyboardButton("2️⃣ VIP Double Filter", callback_data="sel_2")
        )
        msg = f"✅ **Name Received:** `{user_name}`\n\nAapne double name likha hai, niche se koi bhi filter chunein:"
    else:
        markup.add(types.InlineKeyboardButton("1️⃣ Apply Filters", callback_data="sel_1"))
        msg = f"✅ **Name Received:** `{user_name}`\n\nNiche button par click karke fonts chunein:"

    bot.reply_to(message, msg, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("sel_"))
def select_filter(call):
    mode = call.data.split("_")[1]
    u_id = call.from_user.id
    if u_id not in user_sessions: return
    user_sessions[u_id]["mode"] = mode
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Adding ALL 19 buttons
    markup.add(
        types.InlineKeyboardButton("🅰️ Block", callback_data="f_block"),
        types.InlineKeyboardButton("🟢 Circle", callback_data="f_circle"),
        types.InlineKeyboardButton("🅂🅀🅄🄰🅁🄴", callback_data="f_square"),
        types.InlineKeyboardButton("ꜱᴍᴀʟʟᴄᴀᴘ", callback_data="f_small"),
        types.InlineKeyboardButton("ค๒ Wild", callback_data="f_wild"),
        types.InlineKeyboardButton("𝓢𝓬𝓻𝓲𝓹𝓽", callback_data="f_bold_script"),
        types.InlineKeyboardButton("𝙲𝚘𝚘𝚕 Mono", callback_data="f_monospace"),
        types.InlineKeyboardButton("𝕆𝕦𝕥𝕝𝕚𝕟𝕖", callback_data="f_double_struck"),
        types.InlineKeyboardButton("𝘐𝘵𝘢𝘭𝘪𝘤", callback_data="f_italic_bold"),
        types.InlineKeyboardButton("🫧 Bubble", callback_data="f_bubble"),
        types.InlineKeyboardButton("🇬🇷 Greek", callback_data="f_greek"),
        types.InlineKeyboardButton("💲 Money", callback_data="f_currency"),
        types.InlineKeyboardButton("⒜ Paren", callback_data="f_paren"),
        types.InlineKeyboardButton("𝐁𝐨𝐥𝐝", callback_data="f_bold_sans"),
        types.InlineKeyboardButton("𝕋𝕙𝕚𝕟", callback_data="f_thin"),
        types.InlineKeyboardButton("𝐒𝐞𝐫𝐢𝐞𝐟", callback_data="f_serif"),
        types.InlineKeyboardButton("𝓒𝓞𝓜𝓘𝓒", callback_data="f_comic"),
        types.InlineKeyboardButton("𝘚𝘭𝘢𝘯𝘵", callback_data="f_slant"),
        types.InlineKeyboardButton("𝕭𝖔𝖑𝖉_𝖌𝖔𝖙𝖍𝖎𝖈", callback_data="f_gothic")
    )
    bot.edit_message_text("🎨 **Select Font Style**", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("f_"))
def handle_font(call):
    font = call.data.split("_")[1]
    u_id = call.from_user.id
    if u_id not in user_sessions: return
    user_sessions[u_id]["font"] = font
    user_sessions[u_id]["page"] = 0
    bot.answer_callback_query(call.id, text=f"Applying {font}...")
    show_designs(call.message, u_id)

def show_designs(message, u_id):
    data = user_sessions.get(u_id)
    text, font, page, mode = data["text"], data["font"], data["page"], data["mode"]
    words = text.split()
    
    if mode == "1": styled = [apply_font(text, font)]
    else:
        if len(words) < 2: return bot.send_message(message.chat.id, "⚠️ Need 2 words.")
        styled = [apply_font(words[0], font), apply_font(" ".join(words[1:]), font)]

    target_list = designs.get(mode, [])
    start, end = page * 10, (page + 1) * 10
    current = target_list[start:end]

    for d in current:
        try: bot.send_message(message.chat.id, f"`{d.format(*styled)}`", parse_mode="Markdown")
        except: continue

    if len(target_list) > end:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Next 10 Designs ➡️", callback_data="next_p"))
        bot.send_message(message.chat.id, "Check more:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "next_p")
def next_page(call):
    u_id = call.from_user.id
    if u_id in user_sessions:
        user_sessions[u_id]["page"] += 1
        show_designs(call.message, u_id)

# ===============================
# MAIN EXECUTION
# ===============================
def start_bot():
    print("🤖 Bot Online!")
    bot.infinity_polling(skip_pending=True)

Thread(target=start_bot).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
