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
# FONT ENGINE WITH EVERY ALPHABET
# ===============================
def apply_font(text, font_type):
    m = {
        "block": {
            'a': '🅰️', 'b': '🅱️', 'c': '🅲', 'd': '🅳', 'e': '🅴', 'f': '🅵', 'g': '🅶', 'h': '🅷', 'i': '🅸', 'j': '🅹', 'k': '🅺', 'l': '🅻', 'm': '🅼', 'n': '🅽', 'o': '🅾️', 'p': '🅿️', 'q': '🆀', 'r': '🆁', 's': '🆂', 't': '🆃', 'u': '🆄', 'v': '🆅', 'w': '🆆', 'x': '🆇', 'y': '🆈', 'z': '🆉',
            'A': '🅰️', 'B': '🅱️', 'C': '🅲', 'D': '🅳', 'E': '🅴', 'F': '🅵', 'G': '🅶', 'H': '🅷', 'I': '🅸', 'J': '🅹', 'K': '🅺', 'L': '🅻', 'M': '🅼', 'N': '🅽', 'O': '🅾️', 'P': '🅿️', 'Q': '🆀', 'R': '🆁', 'S': '🆂', 'T': '🆃', 'U': '🆄', 'V': '🆅', 'W': '🆆', 'X': '🆇', 'Y': '🆈', 'Z': '🆉'
        },
        "circle": {
            'a': '🅐', 'b': '🅑', 'c': '🅒', 'd': '🅓', 'e': '🅔', 'f': '🅕', 'g': '🅖', 'h': '🅗', 'i': '🅘', 'j': '🅙', 'k': '🅚', 'l': '🅛', 'm': '🅜', 'n': '🅝', 'o': '🅞', 'p': '🅟', 'q': '🅠', 'r': '🅡', 's': '🅢', 't': '🅣', 'u': '🅤', 'v': '🅥', 'w': '🅦', 'x': '🅧', 'y': '🅨', 'z': '🅩',
            'A': '🅐', 'B': '🅑', 'C': '🅒', 'D': '🅓', 'E': '🅔', 'F': '🅕', 'G': '🅖', 'H': '🅗', 'I': '🅘', 'J': '🅙', 'K': '🅚', 'L': '🅛', 'M': '🅜', 'N': '🅝', 'O': '🅞', 'P': '🅟', 'Q': '🅠', 'R': '🅡', 'S': '🅢', 'T': '🅣', 'U': '🅤', 'V': '🅥', 'W': '🅦', 'X': '🅧', 'Y': '🅨', 'Z': '🅩'
        },
        "square": {
            'a': '🄰', 'b': '🄱', 'c': '🄲', 'd': '🄳', 'e': '🄴', 'f': '🄵', 'g': '🄶', 'h': '🄷', 'i': '🄸', 'j': '🄹', 'k': '🄺', 'l': '🄻', 'm': '🄼', 'n': '🄽', 'o': '🄾', 'p': '🄿', 'q': '🅀', 'r': '🅁', 's': '🅂', 't': '🅃', 'u': '🆄', 'v': '🆅', 'w': '🆆', 'x': '🆇', 'y': '🅈', 'z': '🅉',
            'A': '🄰', 'B': '🄱', 'C': '🄲', 'D': '🄳', 'E': '🄴', 'F': '🄵', 'G': '🄶', 'H': '🄷', 'I': '🄸', 'J': '🄹', 'K': '🄺', 'L': '🄻', 'M': '🄼', 'N': '🄽', 'O': '🄾', 'P': '🄿', 'Q': '🅀', 'R': '🅁', 'S': '🅂', 'T': '🅃', 'U': '🆄', 'V': '🆅', 'W': '🆆', 'X': '🆇', 'Y': '🅈', 'Z': '🅉'
        },
        "small": {
            'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
            'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ꜰ', 'G': 'ɢ', 'H': 'ʜ', 'I': 'ɪ', 'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ', 'O': 'ᴏ', 'P': 'ᴘ', 'Q': 'ǫ', 'R': 'ʀ', 'S': 's', 'T': 'ᴛ', 'U': 'ᴜ', 'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x', 'Y': 'ʏ', 'Z': 'ᴢ'
        },
        "wild": {
            'a': 'ค', 'b': '๒', 'c': 'ς', 'd': '๔', 'e': 'є', 'f': 'Ŧ', 'g': 'ﻮ', 'h': 'ђ', 'i': 'เ', 'j': 'ן', 'k': 'к', 'l': 'ɭ', 'm': '๓', 'n': 'ภ', 'o': '๏', 'p': 'ק', 'q': 'ợ', 'r': 'г', 's': 'ร', 't': 'Շ', 'u': 'ย', 'v': 'ง', 'w': 'ฬ', 'x': 'א', 'y': 'ץ', 'z': 'չ',
            'A': 'ค', 'B': '๒', 'C': 'ς', 'D': '๔', 'E': 'є', 'F': 'Ŧ', 'G': 'ﻮ', 'H': 'ђ', 'I': 'เ', 'J': 'ן', 'K': 'к', 'L': 'ɭ', 'M': '๓', 'N': 'ภ', 'O': '๏', 'P': 'ק', 'Q': 'ợ', 'R': 'г', 'S': 'ร', 'T': 'Շ', 'U': 'ย', 'V': 'ง', 'W': 'ฬ', 'X': 'א', 'Y': 'ץ', 'Z': 'չ'
        },
        "bold_script": {
            'a': '𝓪', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮', 'f': '𝓯', 'g': '𝓰', 'h': '𝓱', 'i': '𝓲', 'j': '𝓳', 'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷', 'o': '𝓸', 'p': '𝓹', 'q': '𝓺', 'r': '𝓻', 's': '𝓼', 't': '𝓽', 'u': '𝓾', 'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃',
            'A': '𝓐', 'B': '𝓑', 'C': '𝓒', 'D': '𝓓', 'E': '𝓔', 'F': '𝓕', 'G': '𝓖', 'H': '𝓗', 'I': '𝓘', 'J': '𝓙', 'K': '𝓚', 'L': '𝓛', 'M': '𝓜', 'N': '𝓝', 'O': '𝓞', 'P': '𝓟', 'Q': '𝓠', 'R': '𝓡', 'S': '𝓢', 'T': '𝓣', 'U': '𝓤', 'V': '𝓥', 'W': '𝓦', 'X': '𝓧', 'Y': '𝓨', 'Z': '𝓩'
        },
        "monospace": {
            'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎', 'f': '𝚏', 'g': '𝚐', 'h': '𝚑', 'i': '𝚒', 'j': '𝚓', 'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗', 'o': '𝚘', 'p': '𝚙', 'q': '𝚚', 'r': '𝚛', 's': '𝚜', 't': '𝚝', 'u': '𝚞', 'v': '𝚟', 'w': '𝚠', 'x': '𝚡', 'y': '𝚢', 'z': '𝚣',
            'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶', 'H': '𝙷', 'I': '𝙸', 'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽', 'O': '𝙾', 'P': '𝙿', 'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃', 'U': '𝚄', 'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈', 'Z': '𝚉'
        },
        "double_struck": {
            'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖', 'f': '𝕗', 'g': '𝕘', 'h': '𝕙', 'i': '𝕚', 'j': '𝕛', 'k': '𝕜', 'l': '𝕝', 'm': '𝕞', 'n': '𝕟', 'o': '𝕠', 'p': '𝕡', 'q': '𝕢', 'r': '𝕣', 's': '𝕤', 't': '𝕥', 'u': '𝕦', 'v': '𝕧', 'w': '𝕨', 'x': '𝕩', 'y': '𝕪', 'z': '𝕫',
            'A': '𝔸', 'B': '𝔹', 'C': 'ℂ', 'D': '𝔻', 'E': '𝔼', 'F': '𝔽', 'G': '𝔾', 'H': 'ℍ', 'I': '𝕀', 'J': '𝕁', 'K': '𝕂', 'L': '𝕃', 'M': '𝕄', 'N': 'ℕ', 'O': '𝕆', 'P': 'ℙ', 'Q': 'ℚ', 'R': 'ℝ', 'S': '𝕊', 'T': '𝕋', 'U': '𝕌', 'V': '𝕍', 'W': '𝕎', 'X': '𝕏', 'Y': '𝕐', 'Z': 'ℤ'
        },
        "italic_bold": {
            'a': '𝙖', 'b': '𝙗', 'c': '𝙘', 'd': '🇩', 'e': '𝙚', 'f': '𝙛', 'g': '𝙜', 'h': '𝙝', 'i': '𝙞', 'j': '𝙟', 'k': '𝙠', 'l': '𝙡', 'm': '𝙢', 'n': '𝙣', 'o': '𝙤', 'p': '𝙥', 'q': '𝙦', 'r': '𝙧', 's': '𝙨', 't': '𝙩', 'u': '𝙪', 'v': '𝙫', 'w': '𝙬', 'x': '𝙭', 'y': '𝙮', 'z': '𝙯',
            'A': '𝘼', 'B': '𝘽', 'C': '𝘾', 'D': '𝘿', 'E': '𝙀', 'F': '𝙁', 'G': '𝙂', 'H': '𝙃', 'I': '𝙄', 'J': '𝙅', 'K': '𝙆', 'L': '𝙇', 'M': '𝙈', 'N': '𝙉', 'O': '𝙊', 'P': '𝙋', 'Q': '𝙌', 'R': '𝙍', 'S': '𝙎', 'T': '𝙏', 'U': '𝙐', 'V': '𝙑', 'W': '𝙒', 'X': '𝙓', 'Y': '𝙔', 'Z': '𝙕'
        },
        "bubble": {
            'a': 'ⓐ', 'b': 'ⓑ', 'c': 'ⓒ', 'd': 'ⓓ', 'e': 'ⓔ', 'f': 'ⓕ', 'g': 'ⓖ', 'h': 'ⓗ', 'i': 'ⓘ', 'j': 'ⓙ', 'k': 'ⓚ', 'l': 'ⓛ', 'm': 'ⓜ', 'n': 'ⓝ', 'o': 'ⓞ', 'p': 'ⓟ', 'q': 'ⓠ', 'r': 'ⓡ', 's': 'ⓢ', 't': 'ⓣ', 'u': 'ⓤ', 'v': 'ⓥ', 'w': 'ⓦ', 'x': 'ⓧ', 'y': 'ⓨ', 'z': 'ⓩ',
            'A': 'Ⓐ', 'B': 'Ⓑ', 'C': 'Ⓒ', 'D': 'Ⓓ', 'E': 'Ⓔ', 'F': 'Ⓕ', 'G': 'Ⓖ', 'H': 'Ⓗ', 'I': 'Ⓘ', 'J': 'Ⓙ', 'K': 'Ⓚ', 'L': 'Ⓛ', 'M': 'Ⓜ', 'N': 'Ⓝ', 'O': 'Ⓞ', 'P': 'Ⓟ', 'Q': 'Ⓠ', 'R': 'Ⓡ', 'S': 'Ⓢ', 'T': 'Ⓣ', 'U': 'Ⓤ', 'V': 'Ⓥ', 'W': 'Ⓦ', 'X': 'Ⓧ', 'Y': 'Ⓨ', 'Z': 'Ⓩ'
        },
        "greek": {
            'a': 'α', 'b': 'β', 'c': 'ψ', 'd': 'δ', 'e': 'ε', 'f': 'φ', 'g': 'γ', 'h': 'η', 'i': 'ι', 'j': 'ξ', 'k': 'κ', 'l': 'λ', 'm': 'μ', 'n': 'ν', 'o': 'ο', 'p': 'π', 'q': 'χ', 'r': 'ρ', 's': 'σ', 't': 'τ', 'u': 'υ', 'v': 'ω', 'w': 'ω', 'x': 'χ', 'y': 'υ', 'z': 'ζ',
            'A': 'Α', 'B': 'Β', 'C': 'Ψ', 'D': 'Δ', 'E': 'Ε', 'F': 'Φ', 'G': 'Γ', 'H': 'Η', 'I': 'Ι', 'J': 'Ξ', 'K': 'Κ', 'L': 'Λ', 'M': 'Μ', 'N': 'Ν', 'O': 'Ο', 'P': 'Π', 'Q': 'Χ', 'R': 'Ρ', 'S': 'Σ', 'T': 'Τ', 'U': 'Υ', 'V': 'Ω', 'W': 'Ω', 'X': 'Χ', 'Y': 'Υ', 'Z': 'Ζ'
        },
        "currency": {
            'a': '₳', 'b': '฿', 'c': '₵', 'd': 'Đ', 'e': 'Ɇ', 'f': '₣', 'g': '₲', 'h': 'Ⱨ', 'i': 'ł', 'j': 'J', 'k': '₭', 'l': 'Ⱡ', 'm': '₥', 'n': '₦', 'o': 'Ø', 'p': '₱', 'q': 'Q', 'r': 'Ɽ', 's': '₴', 't': '₮', 'u': 'Ʉ', 'v': 'V', 'w': '₩', 'x': 'Ӿ', 'y': 'Ɏ', 'z': 'Ƶ',
            'A': '₳', 'B': '฿', 'C': '₵', 'D': 'Đ', 'E': 'Ɇ', 'F': '₣', 'G': '₲', 'H': 'Ⱨ', 'I': 'ł', 'J': 'J', 'K': '₭', 'L': 'Ⱡ', 'M': '₥', 'N': '₦', 'O': 'Ø', 'P': '₱', 'Q': 'Q', 'R': 'Ɽ', 'S': '₴', 'T': '₮', 'U': 'Ʉ', 'V': 'V', 'W': '₩', 'X': 'Ӿ', 'Y': 'Ɏ', 'Z': 'Ƶ'
        },
        "bold_sans": {
            'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻', 'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
            'A': '𝗮', 'B': '𝗯', 'C': '𝗰', 'D': '𝗱', 'E': '𝗲', 'F': '𝗳', 'G': '𝗴', 'H': '𝗵', 'I': '𝗶', 'J': '𝗷', 'K': '𝗸', 'L': '𝗹', 'M': '𝗺', 'N': '𝗻', 'O': '𝗼', 'P': '𝗽', 'Q': '𝗾', 'R': '𝗿', 'S': '𝘀', 'T': '𝘁', 'U': '𝘂', 'V': '𝘃', 'W': '𝘄', 'X': '𝘅', 'Y': '𝘆', 'Z': '𝘇'
        },
        "thin": {
            'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖', 'f': '𝕗', 'g': '𝕘', 'h': '𝕙', 'i': '𝕚', 'j': '𝕛', 'k': '𝕜', 'l': '𝕝', 'm': '𝕞', 'n': '𝕟', 'o': '𝕠', 'p': '𝕡', 'q': '𝕢', 'r': '𝕣', 's': '𝕤', 't': '𝕥', 'u': '𝕦', 'v': '𝕧', 'w': '𝕨', 'x': '𝕩', 'y': '𝕪', 'z': '𝕫',
            'A': '𝕒', 'B': '𝕓', 'C': '𝕔', 'D': '𝕕', 'E': '𝕖', 'F': '𝕗', 'G': '𝕘', 'H': '𝕙', 'I': '𝕚', 'J': '𝕛', 'K': '𝕜', 'L': '𝕝', 'M': '𝕞', 'N': '𝕟', 'O': '𝕠', 'P': '𝕡', 'Q': '𝕢', 'R': '𝕣', 'S': '𝕤', 'T': '𝕥', 'u': '𝕦', 'v': '𝕧', 'w': '𝕨', 'x': '𝕩', 'y': '𝕪', 'z': '𝕫'
        },
        "serif": {
            'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠', 'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧', 'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',
            'A': '𝐚', 'B': '𝐛', 'C': '𝐜', 'D': '𝐝', 'E': '𝐞', 'F': '𝐟', 'G': '𝐠', 'H': '𝐡', 'I': '𝐢', 'J': '𝐣', 'K': '𝐤', 'L': '𝐥', 'M': '𝐦', 'N': '𝐧', 'O': '𝐨', 'P': '𝐩', 'Q': '𝐪', 'R': '𝐫', 'S': '𝐬', 'T': '𝐭', 'U': '𝐮', 'V': '𝐯', 'W': '𝐰', 'X': '𝐱', 'Y': '𝐲', 'Z': '𝐳'
        },
        "gothic": {
            'a': '𝖆', 'b': '𝖇', 'c': '𝖈', 'd': '𝖉', 'e': '𝖊', 'f': '𝖋', 'g': '𝖌', 'h': '𝖍', 'i': '𝖎', 'j': '𝖏', 'k': '𝖐', 'l': '𝖑', 'm': '𝖒', 'n': '𝖓', 'o': '𝖔', 'p': '𝖕', 'q': '𝖖', 'r': '𝖗', 's': '𝖘', 't': '𝖙', 'u': '𝖚', 'v': '𝖛', 'w': '𝖜', 'x': '𝖝', 'y': '𝖞', 'z': '𝖟',
            'A': '𝕬', 'B': '𝕭', 'C': '𝕮', 'D': '𝕯', 'E': '𝕰', 'F': '𝕱', 'G': '𝕲', 'H': '𝕳', 'I': '𝕴', 'J': '𝕵', 'K': '𝕶', 'L': '𝕷', 'M': '𝕸', 'N': '𝕹', 'O': '𝕺', 'P': '𝕻', 'Q': '𝕼', 'R': '𝕽', 'S': '𝕾', 'T': '𝕿', 'U': '𝖀', 'V': '𝖁', 'W': '𝖂', 'X': '𝖃', 'Y': '𝖄', 'Z': '𝖅'
        },
        "slant": {
            'a': '𝘢', 'b': '𝘣', 'c': '𝘤', 'd': '𝘥', 'e': '𝘦', 'f': '𝘧', 'g': '𝘨', 'h': '𝘩', 'i': '𝘪', 'j': '𝘫', 'k': '𝘬', 'l': '𝘭', 'm': '𝘮', 'n': '𝘯', 'o': '𝘰', 'p': '𝘱', 'q': '𝘲', 'r': '𝘳', 's': '𝘴', 't': '𝘵', 'u': '𝕦', 'v': '𝘷', 'w': '𝘸', 'x': '𝘹', 'y': '𝘺', 'z': '𝘻',
            'A': '𝘈', 'B': '𝘉', 'C': '𝘊', 'D': '𝘋', 'E': '𝘌', 'F': '𝘍', 'G': '𝘎', 'H': '𝘏', 'I': '𝘐', 'J': '𝘑', 'K': '𝘒', 'L': '𝘓', 'M': '𝘔', 'N': '𝘕', 'O': '𝘖', 'P': '𝘗', 'Q': '𝘘', 'R': '𝘙', 'S': '𝘚', 'T': '𝘛', 'U': '𝘜', 'V': '𝘝', 'W': '𝘞', 'X': '𝘟', 'Y': '𝘠', 'Z': '𝘡'
        },
        "comic": {
            'a': '𝓬', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮', 'f': '𝓯', 'g': '𝓰', 'h': '𝓱', 'i': '𝓲', 'j': '𝓳', 'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷', 'o': '𝓸', 'p': '𝓹', 'q': '𝓺', 'r': '𝓻', 's': '𝓼', 't': '𝓽', 'u': '𝓾', 'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃',
            'A': '𝓒', 'B': '𝓑', 'C': '𝓒', 'D': '𝓓', 'E': '𝓔', 'F': '𝓕', 'G': '𝓖', 'H': '𝓗', 'I': '𝓘', 'J': '𝓙', 'K': '𝓚', 'L': '𝓛', 'M': '𝓜', 'N': '𝓝', 'O': '𝓞', 'P': '𝓟', 'Q': '𝓠', 'R': '𝓡', 'S': '𝓢', 'T': '𝓣', 'U': '𝓤', 'V': '𝓥', 'W': '𝓦', 'X': '𝓧', 'Y': '𝓨', 'Z': '𝓩'
        },
        "flash": {
            'a': 'λ', 'b': 'ß', 'c': 'ç', 'd': 'Ð', 'e': 'È', 'f': '₣', 'g': '₲', 'h': 'Ħ', 'i': 'Ì', 'j': 'Ĵ', 'k': '₭', 'l': 'Ł', 'm': '₥', 'n': 'Ñ', 'o': 'Ö', 'p': '₱', 'q': 'Ø', 'r': 'ℜ', 's': '§', 't': '₮', 'u': 'Ü', 'v': 'V', 'w': '₩', 'x': 'Ӿ', 'y': '¥', 'z': 'Ƶ',
            'A': 'λ', 'B': 'ß', 'C': 'ç', 'D': 'Ð', 'E': 'È', 'F': '₣', 'G': '₲', 'H': 'Ħ', 'I': 'Ì', 'J': 'Ĵ', 'K': '₭', 'L': 'Ł', 'M': '₥', 'N': 'Ñ', 'O': 'Ö', 'P': '₱', 'Q': 'Ø', 'R': 'ℜ', 'S': '§', 'T': '₮', 'U': 'Ü', 'V': 'V', 'W': '₩', 'X': 'Ӿ', 'Y': '¥', 'Z': 'Ƶ'
        },
        "mirror": {
            'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ', 'f': 'ɟ', 'g': 'ƃ', 'h': 'ɥ', 'i': 'ᴉ', 'j': 'ɾ', 'k': 'ʞ', 'l': 'l', 'm': 'ɯ', 'n': 'u', 'o': 'o', 'p': 'd', 'q': 'b', 'r': 'ɹ', 's': 's', 't': 'ʇ', 'u': 'n', 'v': 'ʌ', 'w': 'ʍ', 'x': 'x', 'y': 'ʎ', 'z': 'z',
            'A': '∀', 'B': '𐐒', 'C': 'Ɔ', 'D': '◖', 'E': 'Ǝ', 'F': 'Ⅎ', 'G': '⅁', 'H': 'H', 'I': 'I', 'J': 'Ր', 'K': 'ʞ', 'L': '˥', 'M': 'W', 'N': 'N', 'O': 'O', 'P': 'Ԁ', 'Q': 'Ό', 'R': 'ᴚ', 'S': 'S', 'T': '⊥', 'U': '∩', 'V': 'Λ', 'W': 'M', 'X': 'X', 'Y': '⅄', 'Z': 'Z'
        },
        "web": {
            'a': 'ą', 'b': 'ҍ', 'c': 'ç', 'd': 'ժ', 'e': 'ҽ', 'f': 'ƒ', 'g': 'ց', 'h': 'հ', 'i': 'ì', 'j': 'ʝ', 'k': 'ҟ', 'l': 'Ӏ', 'm': 'ʍ', 'n': 'ղ', 'o': 'օ', 'p': 'ք', 'q': 'զ', 'r': 'ɾ', 's': 'ʂ', 't': 'է', 'u': 'մ', 'v': 'ѵ', 'w': 'ա', 'x': '×', 'y': 'վ', 'z': 'Հ',
            'A': 'Ą', 'B': 'Ҍ', 'C': 'Ç', 'D': 'Ժ', 'E': 'Ҽ', 'F': 'Ƒ', 'G': 'Ց', 'H': 'Հ', 'I': 'Ì', 'J': 'ʝ', 'K': 'Ҟ', 'L': 'Ӏ', 'M': 'ʍ', 'N': 'Ղ', 'O': 'Օ', 'P': 'Ք', 'Q': 'Զ', 'R': 'Ր', 'S': 'ʂ', 'T': 'Է', 'U': 'Մ', 'V': 'Վ', 'W': 'Ա', 'X': '×', 'Y': 'Վ', 'Z': 'Հ'
        },
        "ancient": {
            'a': 'ǟ', 'b': 'ɮ', 'c': 'ƈ', 'd': 'ɖ', 'e': 'ɛ', 'f': 'ʄ', 'g': 'ɢ', 'h': 'ɦ', 'i': 'ɨ', 'j': 'ʝ', 'k': 'ӄ', 'l': 'ʟ', 'm': 'ʍ', 'n': 'ռ', 'o': 'օ', 'p': 'ք', 'q': 'զ', 'r': 'ʀ', 's': 'ֆ', 't': 'ȶ', 'u': 'ʊ', 'v': 'ʋ', 'w': 'ա', 'x': 'Ӽ', 'y': 'ʏ', 'z': 'ʐ',
            'A': 'Ǟ', 'B': 'ɮ', 'C': 'ƈ', 'D': 'ɖ', 'E': 'ɛ', 'F': 'ʄ', 'G': 'ɢ', 'H': 'ɦ', 'I': 'ɨ', 'J': 'ʝ', 'K': 'ӄ', 'L': 'ʟ', 'M': 'ʍ', 'N': 'ռ', 'O': 'օ', 'P': 'ք', 'Q': 'զ', 'R': 'ʀ', 'S': 'ֆ', 'T': 'ȶ', 'U': 'ʊ', 'V': 'ʋ', 'W': 'ա', 'X': 'Ӽ', 'Y': 'ʏ', 'Z': 'ʐ'
        },
        "knight": {
            'a': 'Δ', 'b': 'β', 'c': 'Ć', 'd': 'Đ', 'e': '€', 'f': '₣', 'g': 'Ǥ', 'h': 'Ħ', 'i': 'Ɨ', 'j': 'Ĵ', 'k': 'Ҝ', 'l': 'Ł', 'm': 'Μ', 'n': 'Ň', 'o': 'Ø', 'p': 'Ƥ', 'q': 'Ω', 'r': 'Ř', 's': 'Ş', 't': 'Ŧ', 'u': 'Ữ', 'v': 'V', 'w': 'Ŵ', 'x': 'Ж', 'y': '¥', 'z': 'Ž',
            'A': 'Δ', 'B': 'β', 'C': 'Ć', 'D': 'Đ', 'E': '€', 'F': '₣', 'G': 'Ǥ', 'H': 'Ħ', 'I': 'Ɨ', 'J': 'Ĵ', 'K': 'Ҝ', 'L': 'Ł', 'M': 'Μ', 'N': 'Ň', 'O': 'Ø', 'P': 'Ƥ', 'Q': 'Ω', 'R': 'Ř', 'S': 'Ş', 'T': 'Ŧ', 'U': 'Ữ', 'V': 'V', 'W': 'Ŵ', 'X': 'Ж', 'Y': '¥', 'Z': 'Ž'
        },
        "storm": {
            'a': 'ᗩ', 'b': 'ᗷ', 'c': 'ᑕ', 'd': 'ᗪ', 'e': 'E', 'f': 'ᖴ', 'g': 'G', 'h': 'ᕼ', 'i': 'I', 'j': 'ᒍ', 'k': 'K', 'l': 'ᒪ', 'm': 'ᗰ', 'n': 'ᑎ', 'o': 'O', 'p': 'ᑭ', 'q': 'ᑫ', 'r': 'ᖇ', 's': 'ᔕ', 't': 'T', 'u': 'ᑌ', 'v': 'ᐯ', 'w': 'ᗯ', 'x': '᙭', 'y': 'Y', 'z': 'ᘔ',
            'A': 'ᗩ', 'B': 'ᗷ', 'C': 'ᑕ', 'D': 'ᗪ', 'E': 'E', 'F': 'ᖴ', 'G': 'G', 'H': 'ᕼ', 'I': 'I', 'J': 'ᒍ', 'K': 'K', 'L': 'ᒪ', 'M': 'ᗰ', 'N': 'ᑎ', 'O': 'O', 'P': 'ᑭ', 'Q': 'ᑫ', 'R': 'ᖇ', 'S': 'ᔕ', 'T': 'T', 'U': 'ᑌ', 'V': 'ᐯ', 'W': 'ᗯ', 'X': '᙭', 'Y': 'Y', 'Z': 'ᘔ'
        },
        "drama": {
            'a': 'α', 'b': 'в', 'c': '¢', 'd': '∂', 'e': 'є', 'f': 'ƒ', 'g': 'g', 'h': 'н', 'i': 'ι', 'j': 'נ', 'k': 'к', 'l': 'ℓ', 'm': 'м', 'n': 'η', 'o': 'σ', 'p': 'ρ', 'q': 'ף', 'r': 'я', 's': 'ѕ', 't': 'т', 'u': 'υ', 'v': 'ν', 'w': 'ω', 'x': 'χ', 'y': 'у', 'z': 'z',
            'A': 'α', 'B': 'в', 'C': '¢', 'D': '∂', 'E': 'є', 'F': 'ƒ', 'G': 'g', 'H': 'н', 'I': 'ι', 'J': 'נ', 'K': 'к', 'L': 'ℓ', 'M': 'м', 'N': 'η', 'O': 'σ', 'P': 'ρ', 'Q': 'ף', 'R': 'я', 'S': 'ѕ', 'T': 'т', 'U': 'υ', 'V': 'ν', 'W': 'ω', 'X': 'χ', 'Y': 'у', 'Z': 'z'
        },
        "diamond": {
            'a': '闩', 'b': '乃', 'c': '匚', 'd': '刀', 'e': '乇', 'f': '下', 'g': '厶', 'h': '卄', 'i': '工', 'j': '丁', 'k': '长', 'l': '乚', 'm': '从', 'n': '𠘨', 'o': '口', 'p': '尸', 'q': '㔿', 'r': '尺', 's': '丂', 't': '丅', 'u': '凵', 'v': 'リ', 'w': '山', 'x': '乂', 'y': '丫', 'z': '乙',
            'A': '闩', 'B': '乃', 'C': '匚', 'D': '刀', 'E': '乇', 'F': '下', 'G': '厶', 'H': '卄', 'I': '工', 'J': '丁', 'K': '长', 'L': '乚', 'M': '从', 'N': '𠘨', 'O': '口', 'P': '尸', 'Q': '㔿', 'R': '尺', 'S': '丂', 'T': '丅', 'U': '凵', 'v': 'リ', 'w': '山', 'x': '乂', 'y': '丫', 'z': '乙'
        },
        "cloud": {
            'a': 'α', 'b': 'Ъ', 'c': 'с', 'd': 'ď', 'e': 'є', 'f': 'ƒ', 'g': 'ģ', 'h': 'н', 'i': 'ї', 'j': 'ĵ', 'k': 'к', 'l': 'ℓ', 'm': 'м', 'n': 'и', 'o': 'о', 'p': 'р', 'q': 'φ', 'r': 'я', 's': 'ร', 't': 'т', 'u': 'ц', 'v': 'v', 'w': 'ω', 'x': 'х', 'y': 'у', 'z': 'ž',
            'A': 'α', 'B': 'Ъ', 'C': 'с', 'D': 'ď', 'E': 'є', 'F': 'ƒ', 'G': 'ģ', 'H': 'н', 'I': 'ї', 'J': 'ĵ', 'K': 'к', 'L': 'ℓ', 'M': 'м', 'N': 'и', 'O': 'о', 'P': 'р', 'Q': 'φ', 'R': 'я', 'S': 'ร', 'T': 'т', 'U': 'ц', 'V': 'v', 'W': 'ω', 'X': 'х', 'Y': 'у', 'Z': 'ž'
        },
        "flag_font": {
            'a': '🇦','b': '🇧','c': '🇨','d': '🇩','e': '🇪','f': '🇫','g': '🇬','h': '🇭','i': '🇮','j': '🇯','k': '🇰','l': '🇱','m': '🇲','n': '🇳','o': '🇴','p': '🇵','q': '🇶','r': '🇷','s': '🇸','t': '🇹','u': '🇺','v': '🇻','w': '🇼','x': '🇽','y': '🇾','z': '🇿',
            'A': '🇦','B': '🇧','C': '🇨','D': '🇩','E': '🇪','F': '🇫','G': '🇬','H': '🇭','I': '🇮','J': '🇯','K': '🇰','L': '🇱','M': '🇲','N': '🇳','O': '🇴','P': '🇵','Q': '🇶','R': '🇷','S': '🇸','T': '🇹','U': '🇺','V': '🇻','W': '🇼','X': '🇽','Y': '🇾','Z': '🇿'
        }
    }
    target = m.get(font_type, {})
    if font_type == "flag_font":
    return "".join(target.get(ch, ch) for ch in text)
else:
    return " ".join(target.get(ch, ch) for ch in text)

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
        return bot.send_message(message.chat.id, "❌ No More Designs Found!")

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
        bot.send_message(message.chat.id, "Click For More Design 👇", reply_markup=markup)

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
╭────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼ ─────★
┆● ʜᴇʏ  : {full_name}, 👋 
┆● ɪ ᴀᴍ : ᴇᴀsʏ ɴᴀᴍᴇ ᴅᴇsɪɢɴᴇʀ
┆● ᴡɪᴛʜ ᴘᴏᴡᴇʀғᴜʟ ғᴇᴀᴛᴜʀᴇs
┊● sᴛʏʟɪsʜ ɴᴀᴍᴇ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ
╰─────────────────────★
───────────────────────
❖ ˹ ɪ ᴀᴍ ᴀ sᴛʏʟɪsʜ ɴᴀᴍᴇ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ ᴡɪᴛʜ ᴍᴀɴʏ ᴛʏᴘᴇ sᴛʏʟɪsʜ ғᴏɴᴛ ˼ ❖
───────────────────────
    📖 ʜᴏᴡ ᴛᴏ ᴜsᴇ (sᴛᴇᴘ ʙʏ sᴛᴇᴘ)
───────────────────────
❖ sᴛᴇᴘ 1: /name ᴄᴏᴍᴍᴀɴᴅ ʟɪᴋʜᴏ.
❖ sᴛᴇᴘ 2: ᴜsᴋᴇ ᴀᴀɢᴇ ᴀᴘɴᴀ sɪɴɢʟᴇ ʏᴀ 
                  ᴅᴏᴜʙʟᴇ ɴᴀᴀᴍ ʟɪᴋʜᴏ.

   ❖(ᴇx: 1. /name ʜᴇʟʟᴏ 
   ❖(ᴇx: 2. /name ʜᴇʟʟᴏ ᴡᴏʀʟᴅ

❖ sᴛᴇᴘ 3: ᴀɢᴀʀ 2 ᴡᴏʀᴅs ʜᴀɪɴ, ᴛᴏʜ ʙᴏᴛ :
   1️⃣ sɪɴɢʟᴇ ғɪʟᴛᴇʀ: ᴘᴏᴏʀᴇ ɴᴀᴀᴍ ᴘᴀʀ 
         ᴇᴋ ᴊᴀɪsᴀ ғᴏɴᴛ.
   2️⃣ ᴠɪᴘ ᴅᴏᴜʙʟᴇ: ᴅᴏɴᴏ ᴡᴏʀᴅs ᴘᴀʀ 
         ᴀʟᴀɢ-ᴀʟᴀɢ ᴅᴇsɪɢɴ.
❖ sᴛᴇᴘ 4: ᴀᴘɴᴇ ᴘᴀsᴀɴᴅ ᴋᴀ ʙᴜᴛᴛᴏɴ ᴅᴀʙᴀʏᴇɪɴ ᴀᴜʀ ʀᴇsᴜʟᴛ ᴄᴏᴘʏ ᴋᴀʀᴇɪɴ!
───────────────────────
"""
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['name', 'Name', 'NAME'])
def start_name(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: 
        return bot.reply_to(message, "⚠️ Usage: /name Your Name")
    
    u_id = message.from_user.id
    user_sessions[u_id] = {"text": args[1], "font": "small", "mode": "1"}
    
    markup = types.InlineKeyboardMarkup()
    if len(args[1].split()) >= 2:
        markup.add(types.InlineKeyboardButton("1️⃣ Single(One Word)", callback_data="sel_1"))
        markup.add(types.InlineKeyboardButton("2️⃣ Double (Two Word)", callback_data="sel_2"))
    else:
        markup.add(types.InlineKeyboardButton("✨ Choose Font's", callback_data="sel_1"))
    
    bot.reply_to(message, f"Name: `{args[1]}`", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("sel_"))
def select_filter(call):
    mode = call.data.split("_")[1]
    u_id = call.from_user.id
    if u_id in user_sessions: 
        user_sessions[u_id]["mode"] = mode
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ꜱᴍᴀʟʟ", callback_data="f_small"),
               types.InlineKeyboardButton("𝐁𝐨𝐥𝐝", callback_data="f_bold_sans"),
               types.InlineKeyboardButton("𝘐𝘵𝘢𝘭𝘪𝘤", callback_data="f_italic_bold"),
               types.InlineKeyboardButton("𝓢𝓬𝓻𝓲𝓹𝓽", callback_data="f_bold_script"),
               types.InlineKeyboardButton("𝕆𝕦𝕥𝕝𝕚𝕟𝕖", callback_data="f_double_struck"),
               types.InlineKeyboardButton("𝐒𝐞𝐫𝐢𝐞𝐟", callback_data="f_serif"),
               types.InlineKeyboardButton("𝔅𝔬𝔩𝔡_𝔠", callback_data="f_wild"),
               types.InlineKeyboardButton("𝙲𝚘𝚘𝚕", callback_data="f_monospace"),
               types.InlineKeyboardButton("𝓒𝓞𝓜𝓘𝓒", callback_data="f_comic"),
               types.InlineKeyboardButton("𝘚𝘭𝘢𝘯𝘵", callback_data="f_slant"),
               types.InlineKeyboardButton("𝕭𝖔𝖑𝖉_𝖌", callback_data="f_gothic"),
               types.InlineKeyboardButton("🅂🅀🅄🄰🅁🄴", callback_data="f_square"),
               types.InlineKeyboardButton("🅱🅻🅾🅲🅺", callback_data="f_block"),
               types.InlineKeyboardButton("🅒🅘🅡🅒🅛🅔", callback_data="f_circle"),
               types.InlineKeyboardButton("ⓑⓤⓑⓑⓛⓔ", callback_data="f_bubble"),
               types.InlineKeyboardButton("Γρεεκ", callback_data="f_greek"),
               types.InlineKeyboardButton("₥Ø₦ɆɎ", callback_data="f_currency"),
               types.InlineKeyboardButton("𝕋𝕙𝕚𝕟", callback_data="f_thin"),
               types.InlineKeyboardButton("ƒℓαѕн", callback_data="f_flash"),
               types.InlineKeyboardButton("ɯıɹɹoɹ", callback_data="f_mirror"),
               types.InlineKeyboardButton("աɛɮ", callback_data="f_web"),
               types.InlineKeyboardButton("ǟռƈɨɛռȶ", callback_data="f_ancient"),
               types.InlineKeyboardButton("ƙռɨɢɦȶ", callback_data="f_knight"),
               types.InlineKeyboardButton("ѕтσям", callback_data="f_storm"),
               types.InlineKeyboardButton("∂яαмα", callback_data="f_drama"),
               types.InlineKeyboardButton("ᗪᎥᗩᗰᝪᑎᗪ", callback_data="f_diamond"),
               types.InlineKeyboardButton("ƈℓσυ∂", callback_data="f_cloud"),
               types.InlineKeyboardButton("🇫 🇱 🇦 🇬", callback_data="f_flag_font"))

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
    
    bot.delete_webhook() 
    
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
