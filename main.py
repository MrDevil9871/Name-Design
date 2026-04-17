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
    return "Bot Is Running By Dear!"

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
DESIGNS_FILE = "my_designs.json"
user_sessions = {}

# ===============================
# JSON LOADING
# ===============================
def load_designs_from_file():
    if os.path.exists(DESIGNS_FILE):
        try:
            with open(DESIGNS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"JSON Error: {e}")
            return {"1": [], "2": []}
    return {"1": [], "2": []}

# ===============================
# FONT ENGINE
# ===============================
def apply_font(text, font_type):
    m = {
        # (⚠️ tumhara pura font dict yaha SAME rahega — kuch bhi change nahi)
    }
    target = m.get(font_type, {})
    return "".join(target.get(c, c) for c in text)

# ===============================
# SHOW DESIGNS (Pagination Logic)
# ===============================
def show_designs(message, u_id, start_index=0):
    data = user_sessions.get(u_id)
    if not data: return
    
    text, font, mode = data["text"], data["font"], data["mode"]
    words = text.split()
    
    current_designs = load_designs_from_file()
    target_list = current_designs.get(mode, [])
    
    if not target_list:
        return bot.send_message(message.chat.id, "❌ No designs found!")

    end_index = start_index + 10
    page_designs = target_list[start_index:end_index]
    
    if mode == "1":
        styled = [apply_font(text, font)]
    else:
        if len(words) < 2: return
        styled = [apply_font(words[0], font), apply_font(" ".join(words[1:]), font)]

    bot.send_message(message.chat.id, f"🚀 Sending Designs {start_index + 1} to {min(end_index, len(target_list))}...")

    for d in page_designs:
        try:
            placeholders = d.count("{}")
            formatted = d.format(*styled[:placeholders]) if placeholders > 0 else d
            bot.send_message(message.chat.id, f"`{formatted}`", parse_mode="Markdown")
            time.sleep(1)
        except Exception as e:
            print(f"Error in loop: {e}")
            continue

    markup = types.InlineKeyboardMarkup()
    if end_index < len(target_list):
        markup.add(types.InlineKeyboardButton("➡️ Next 10 Designs", callback_data=f"next_{end_index}"))
        bot.send_message(message.chat.id, "Agle designs ke liye click karein:", reply_markup=markup)

# ===============================
# HANDLERS
# ===============================
@bot.callback_query_handler(func=lambda call: call.data.startswith("next_"))
def handle_next_page(call):
    next_index = int(call.data.split("_")[1])
    u_id = call.from_user.id
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    show_designs(call.message, u_id, start_index=next_index)

@bot.message_handler(commands=['start'])
def welcome(message):
    full_name = message.from_user.first_name 
    
    welcome_text = f"""
Hey {full_name} 👋
I am Stylish Name Generator Bot
Use /name yourname
"""
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['name', 'Name', 'NAME'])
def start_name(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: 
        return bot.reply_to(message, "⚠️ Usage: /name hello")
    
    u_id = message.from_user.id
    user_sessions[u_id] = {"text": args[1], "font": "small", "mode": "1"}
    
    markup = types.InlineKeyboardMarkup()
    if len(args[1].split()) >= 2:
        markup.add(types.InlineKeyboardButton("1️⃣ Single", callback_data="sel_1"),
                   types.InlineKeyboardButton("2️⃣ Double", callback_data="sel_2"))
    else:
        markup.add(types.InlineKeyboardButton("✨ Apply", callback_data="sel_1"))
    
    bot.reply_to(message, f"Name: `{args[1]}`", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("sel_"))
def select_filter(call):
    mode = call.data.split("_")[1]
    u_id = call.from_user.id
    if u_id in user_sessions: 
        user_sessions[u_id]["mode"] = mode
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Small", callback_data="f_small"),
               types.InlineKeyboardButton("Bold", callback_data="f_bold_sans"))
    
    bot.edit_message_text("Select Font", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("f_"))
def handle_font(call):
    font = call.data.split("_")[1]
    u_id = call.from_user.id
    if u_id in user_sessions: 
        user_sessions[u_id]["font"] = font
    
    bot.answer_callback_query(call.id, "Generating...")
    show_designs(call.message, u_id)

# ===============================
# RUNNER
# ===============================
def start_bot():
    print("Bot is polling...")
    while True:
        try:
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print(f"Polling Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    t = Thread(target=start_bot)
    t.daemon = True
    t.start()

    # 🔥 IMPORTANT FIX FOR RENDER
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, use_reloader=False)
