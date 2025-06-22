import os
import telebot
import threading
from telebot import types
from datetime import datetime, timedelta
import json
import math
import numpy as np
import re
import hashlib
from collections import defaultdict
import time
import random
import string
import requests
from telebot.types import ReactionTypeEmoji
import logging

# ==============================================
# CẤU HÌNH HỆ THỐNG
# ==============================================
# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN") or "8048266129:AAHKcRXoXRNW7OJMrcIpBpNkWK-j8-xsUJI"
ADMIN_ID = 7780640154  # Thay bằng ID admin của bạn
SUPPORT_CONTACT = "@huydev"
REQUIRED_GROUPS = ["@techtitansteam", "@techtitansteamchat"]  # Các nhóm yêu cầu
PREMIUM_CODE = "PREMIUM7DAY"
BOT_USERNAME = "botmd5v2pro_bot"
BANK_ACCOUNT = {
    "name": "NGUYEN BAO THIEN NHAN",
    "number": "6996056789",
    "bank": "MB BANK"
}
ADMIN_SECRET_KEY = "huydevtool"  # Key bí mật cho xác thực admin

bot = telebot.TeleBot(TOKEN)

# Icon hệ thống
ICONS = {
    "success": "✅", "error": "❌", "info": "ℹ️", "warning": "⚠️", "vip": "💎",
    "lock": "🔒", "unlock": "🔓", "clock": "⏰", "stats": "📊", "history": "📜",
    "user": "👤", "admin": "🛡️", "broadcast": "📢", "referral": "📨", "group": "👥",
    "tai": "🎰", "xiu": "🎲", "engine": "⚙️", "risk": "🚸", "time": "⏰",
    "correct": "✔️", "wrong": "❌", "analyze": "🔍", "invite": "📩", "help": "🆘",
    "money": "💰", "key": "🔑", "deposit": "📥", "friends": "👥", "gift": "🎁",
    "loading": "🔄", "sun": "☀️", "dice": "🎲", "bank": "🏦", "chart": "📈",
    "list": "📋", "add": "➕", "remove": "➖", "settings": "⚙️", "star": "⭐",
    "crown": "👑", "medal": "🏅", "trophy": "🏆", "fire": "🔥", "rocket": "🚀",
    "back": "🔙", "refresh": "🔄", "next": "➡️", "prev": "⬅️", "ban": "🚫",
    "unban": "🔓", "backup": "💾", "security": "🔐", "search": "🔎", "download": "📥",
    "upload": "📤", "shield": "🛡️", "robot": "🤖", "phone": "📱", "email": "📧",
    "link": "🔗", "pin": "📌", "megaphone": "📢", "bell": "🔔", "gear": "⚙️",
    "tools": "🛠️", "keyboard": "⌨️", "trash": "🗑️", "checklist": "📝", "qrcode": "📱",
    "barcode": "📊", "label": "🏷️", "bookmark": "🔖", "wifi": "📶", "battery": "🔋",
    "bluetooth": "📶", "signal": "📶", "voice": "🎙️", "video": "🎥", "camera": "📷",
    "image": "🖼️", "microphone": "🎤", "headphones": "🎧", "tv": "📺", "radio": "📻",
    "game": "🎮", "joystick": "🕹️", "dart": "🎯", "bowling": "🎳", "slot": "🎰",
    "casino": "🎲", "card": "🎴", "chess": "♟️", "puzzle": "🧩", "block": "🧱",
    "construction": "🏗️", "hammer": "🔨", "pick": "⛏️", "nutbolt": "🔩", "bricks": "🧱",
    "magnet": "🧲", "chains": "⛓️", "hook": "🪝", "knife": "🔪", "gun": "🔫",
    "bomb": "💣", "sword": "⚔️", "shield2": "🛡️", "armor": "🥋", "helmet": "⛑️",
    "medal2": "🎖️", "trophy2": "🏆", "coin": "🪙", "moneybag": "💰", "yen": "💴",
    "dollar": "💵", "euro": "💶", "pound": "💷", "receipt": "🧾", "creditcard": "💳",
    "bank2": "🏛️", "atm": "🏧", "shopping": "🛒", "cart": "🛒", "basket": "🧺",
    "box": "📦", "package": "📦", "mail": "✉️", "email2": "📧", "inbox": "📥",
    "outbox": "📤", "envelope": "✉️", "paperclip": "📎", "scissors": "✂️", "ruler": "📏",
    "pen": "🖊️", "pencil": "✏️", "paintbrush": "🖌️", "crayon": "🖍️", "notebook": "📓",
    "book": "📖", "newspaper": "📰", "notepad": "📋", "calendar": "📅", "date": "📅",
    "clock2": "🕰️", "hourglass": "⏳", "stopwatch": "⏱️", "timer": "⏲️", "alarm": "⏰",
    "thermometer": "🌡️", "umbrella": "☂️", "rain": "🌧️", "snow": "❄️", "fire2": "🔥",
    "volcano": "🌋", "tornado": "🌪️", "wind": "🌬️", "thunder": "🌩️", "fog": "🌫️",
    "sun2": "🌞", "moon": "🌙", "star2": "⭐", "planet": "🪐", "comet": "☄️",
    "telescope": "🔭", "microscope": "🔬", "satellite": "🛰️", "rocket2": "🚀", "ufo": "🛸",
    "alien": "👽", "robot2": "🤖", "android": "🤖", "avatar": "👤", "ghost": "👻",
    "skull": "💀", "bone": "🦴", "footprints": "👣", "eye": "👁️", "ear": "👂",
    "nose": "👃", "mouth": "👄", "tongue": "👅", "lips": "👄", "tooth": "🦷",
    "hand": "✋", "fist": "✊", "wave": "👋", "clap": "👏", "thumbsup": "👍",
    "thumbsdown": "👎", "point": "👆", "victory": "✌️", "ok": "👌", "pinch": "🤏",
    "crossed": "🤞", "love": "🤟", "callme": "🤙", "muscle": "💪", "mechanical": "🦾",
    "leg": "🦵", "foot": "🦶", "brain": "🧠", "heart": "❤️", "lungs": "🫁",
    "tooth2": "🦷", "bone2": "🦴", "eyes": "👀", "ear2": "👂", "nose2": "👃",
    "baby": "👶", "child": "🧒", "boy": "👦", "girl": "👧", "adult": "🧑",
    "man": "👨", "woman": "👩", "elder": "🧓", "blonde": "👱", "beard": "🧔",
    "redhair": "👨‍🦰", "curlyhair": "👨‍🦱", "whitehair": "👨‍🦳", "bald": "👨‍🦲", "blonde_woman": "👱‍♀️",
    "redhair_woman": "👩‍🦰", "curlyhair_woman": "👩‍🦱", "whitehair_woman": "👩‍🦳", "bald_woman": "👩‍🦲", "healthworker": "🧑‍⚕️",
    "doctor": "👨‍⚕️", "nurse": "👩‍⚕️", "student": "🧑‍🎓", "teacher": "🧑‍🏫", "judge": "🧑‍⚖️",
    "farmer": "🧑‍🌾", "cook": "🧑‍🍳", "mechanic": "🧑‍🔧", "factory": "🧑‍🏭", "office": "🧑‍💼",
    "scientist": "🧑‍🔬", "technologist": "🧑‍💻", "singer": "🧑‍🎤", "artist": "🧑‍🎨", "pilot": "🧑‍✈️",
    "astronaut": "🧑‍🚀", "firefighter": "🧑‍🚒", "police": "👮", "detective": "🕵️", "guard": "💂",
    "ninja": "🥷", "construction_worker": "👷", "prince": "🤴", "princess": "👸", "superhero": "🦸",
    "supervillain": "🦹", "mage": "🧙", "fairy": "🧚", "vampire": "🧛", "merperson": "🧜",
    "elf": "🧝", "genie": "🧞", "zombie": "🧟", "santa": "🎅", "mrs_claus": "🤶",
    "superhero_man": "🦸‍♂️", "superhero_woman": "🦸‍♀️", "supervillain_man": "🦹‍♂️", "supervillain_woman": "🦹‍♀️", "mage_man": "🧙‍♂️",
    "mage_woman": "🧙‍♀️", "fairy_man": "🧚‍♂️", "fairy_woman": "🧚‍♀️", "vampire_man": "🧛‍♂️", "vampire_woman": "🧛‍♀️",
    "merperson_man": "🧜‍♂️", "merperson_woman": "🧜‍♀️", "elf_man": "🧝‍♂️", "elf_woman": "🧝‍♀️", "genie_man": "🧞‍♂️",
    "genie_woman": "🧞‍♀️", "zombie_man": "🧟‍♂️", "zombie_woman": "🧟‍♀️", "massage": "💆", "haircut": "💇",
    "walking": "🚶", "standing": "🧍", "kneeling": "🧎", "runner": "🏃", "dancer": "💃",
    "man_dancing": "🕺", "levitate": "🕴️", "cartwheel": "🤸", "juggling": "🤹", "bath": "🛀",
    "bed": "🛌", "couple": "👫", "friends": "👭", "handshake": "🤝", "selfie": "🤳",
    "flex": "💪", "speech": "🗣️", "silhouette": "👤", "bust": "👥", "footprints2": "👣", "file": "🧾", "check": "🔍"
}

# Danh sách emoji cho reaction
REACTION_EMOJIS = [
    "❤️", "😂", "👍", "👎", "🔥", "🎉", "👏", "🤔", "😢", "😡", "😮",
    "💯", "🥰", "😎", "💔", "🙄", "😅", "😆", "😁", "😐", "😴"
]

# ==============================================
# CƠ SỞ DỮ LIỆU NÂNG CẤP
# ==============================================
class EnhancedDatabase:
    @staticmethod
    def load(filename):
        try:
            with open(f'data/{filename}.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            defaults = {
                'users': {},
                'history': {},
                'activity': {},
                'codes': {},
                'referral': {},
                'config': {'reverse_mode': False, 'maintenance': False},
                'keys': {},
                'deposits': {},
                'withdrawals': {},
                'staff': {},
                'sunwin_sessions': {},
                'broadcast_messages': {},
                'banned_users': [],
                'admin_logs': [],
                'user_logs': [],
                'transactions': [],
                'security': {'admin_auth': {}, 'failed_attempts': {}},
                'settings': {
                    'min_deposit': 10000,
                    'min_withdraw': 50000,
                    'max_withdraw': 10000000,
                    'fees': {'deposit': 0, 'withdraw': 0.05},
                    'limits': {'daily_analyze': 50, 'vip_daily_analyze': 200}
                }
            }
            return defaults.get(filename, {})

    @staticmethod
    def save(data, filename):
        os.makedirs('data', exist_ok=True)
        with open(f'data/{filename}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def backup():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs('backups', exist_ok=True)
        for filename in ['users', 'history', 'activity', 'codes', 'referral', 'config', 
                        'keys', 'deposits', 'withdrawals', 'staff', 'sunwin_sessions', 
                        'broadcast_messages', 'banned_users', 'admin_logs', 'user_logs']:
            try:
                with open(f'data/{filename}.json', 'r', encoding='utf-8') as f_in:
                    with open(f'backups/{filename}_{timestamp}.json', 'w', encoding='utf-8') as f_out:
                        json.dump(json.load(f_in), f_out, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"Backup failed for {filename}: {str(e)}")

# Khởi tạo cơ sở dữ liệu
users = EnhancedDatabase.load('users')
history = EnhancedDatabase.load('history')
activity = EnhancedDatabase.load('activity')
codes_db = EnhancedDatabase.load('codes')
referral_db = EnhancedDatabase.load('referral')
config_db = EnhancedDatabase.load('config')
keys_db = EnhancedDatabase.load('keys')
deposits_db = EnhancedDatabase.load('deposits')
withdrawals_db = EnhancedDatabase.load('withdrawals')
staff_db = EnhancedDatabase.load('staff')
sunwin_sessions = EnhancedDatabase.load('sunwin_sessions')
broadcast_messages = EnhancedDatabase.load('broadcast_messages')
banned_users = EnhancedDatabase.load('banned_users')
admin_logs = EnhancedDatabase.load('admin_logs')
user_logs = EnhancedDatabase.load('user_logs')
security_db = EnhancedDatabase.load('security')
settings_db = EnhancedDatabase.load('settings')

reverse_mode = config_db.get('reverse_mode', False)
maintenance_mode = config_db.get('maintenance', False)

# ==============================================
# TIỆN ÍCH HỆ THỐNG NÂNG CẤP
# ==============================================
def log_admin_action(user_id, action, details=None):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": str(user_id),
        "action": action,
        "details": details or {}
    }
    admin_logs.append(log_entry)
    EnhancedDatabase.save(admin_logs, 'admin_logs')

def log_user_action(user_id, action, details=None):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": str(user_id),
        "action": action,
        "details": details or {}
    }
    user_logs.append(log_entry)
    EnhancedDatabase.save(user_logs, 'user_logs')

def send_typing(chat_id):
    try:
        bot.send_chat_action(chat_id, 'typing')
    except Exception as e:
        logger.error(f"Error sending typing action: {str(e)}")

def random_reaction(message):
    try:
        emoji = random.choice(REACTION_EMOJIS)
        bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[ReactionTypeEmoji(emoji=emoji)]
        )
    except Exception as e:
        logger.error(f"Reaction error: {e}")

def is_user_in_group(user_id, group_username):
    try:
        chat_member = bot.get_chat_member(group_username, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Check group membership error: {str(e)}")
        return False

def check_group_membership(user_id):
    missing = []
    for group in REQUIRED_GROUPS:
        try:
            chat_member = bot.get_chat_member(group, user_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                missing.append(group)
        except Exception as e:
            logger.error(f"Error checking group {group}: {str(e)}")
            missing.append(group)
    return missing

def is_vip_active(uid):
    uid = str(uid)
    user = users.get(uid, {})
    if not user.get("vip_active", False):
        return False
    exp_str = user.get("vip_expire", "")
    try:
        return datetime.now() <= datetime.strptime(exp_str, "%Y-%m-%d %H:%M:%S")
    except:
        return False

def is_premium_user(uid):
    uid = str(uid)
    return users.get(uid, {}).get("premium", False)

def get_user_balance(uid):
    uid = str(uid)
    return users.get(uid, {}).get("balance", 0)

def activate_vip(uid, days=7, extend=False):
    uid = str(uid)
    users[uid] = users.get(uid, {})
    
    if extend and users[uid].get("vip_expire"):
        try:
            current_expire = datetime.strptime(users[uid]["vip_expire"], "%Y-%m-%d %H:%M:%S")
            exp_date = (max(datetime.now(), current_expire) + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        except:
            exp_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        exp_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    
    users[uid]["vip_active"] = True
    users[uid]["vip_expire"] = exp_date
    users[uid]["last_active"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    EnhancedDatabase.save(users, 'users')
    
    log_user_action(uid, "activate_vip", {"days": days, "exp_date": exp_date})
    return exp_date

def activate_premium(uid):
    uid = str(uid)
    users[uid] = users.get(uid, {})
    users[uid]["premium"] = True
    EnhancedDatabase.save(users, 'users')
    log_user_action(uid, "activate_premium")

def create_premium_code(code_name, days, max_uses=1, creator_id=None):
    codes_db[code_name] = {
        "days": days,
        "max_uses": max_uses,
        "used_count": 0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "used_by": [],
        "creator": str(creator_id) if creator_id else None
    }
    EnhancedDatabase.save(codes_db, 'codes')
    
    if creator_id:
        log_admin_action(creator_id, "create_code", {"code": code_name, "days": days, "max_uses": max_uses})
    return codes_db[code_name]

def create_vip_key(key_name, days, max_uses=1, creator_id=None):
    keys_db[key_name] = {
        "days": days,
        "max_uses": max_uses,
        "used_count": 0,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "used_by": [],
        "price": get_key_price(days),
        "creator": str(creator_id) if creator_id else None
    }
    EnhancedDatabase.save(keys_db, 'keys')
    
    if creator_id:
        log_admin_action(creator_id, "create_key", {"key": key_name, "days": days, "max_uses": max_uses})
    return keys_db[key_name]

def get_key_price(days):
    prices = {
        1: 20000,
        7: 60000,
        30: 120000,
        60: 180000,
        90: 250000,
        180: 450000,
        365: 800000
    }
    return prices.get(days, days * 1000)

def use_premium_code(code_name, user_id):
    if code_name not in codes_db:
        return False, f"{ICONS['error']} Mã không hợp lệ!"
    
    code = codes_db[code_name]
    user_id = str(user_id)
    
    if user_id in code["used_by"]:
        return False, f"{ICONS['warning']} Bạn đã sử dụng mã này!"
    
    if code["used_count"] >= code["max_uses"]:
        return False, f"{ICONS['clock']} Mã đã hết lượt sử dụng!"
    
    extend = user_id in users and users[user_id].get("vip_active")
    exp_date = activate_vip(user_id, code["days"], extend)
    
    code["used_count"] += 1
    code["used_by"].append(user_id)
    EnhancedDatabase.save(codes_db, 'codes')
    
    log_user_action(user_id, "use_premium_code", {"code": code_name, "days": code["days"]})
    
    return True, (
        f"{ICONS['success']} Kích hoạt VIP {code['days']} ngày thành công!\n"
        f"{ICONS['clock']} Hết hạn: {exp_date}"
    )

def use_vip_key(key_name, user_id):
    if key_name not in keys_db:
        return False, f"{ICONS['error']} Key không hợp lệ!"
    
    key = keys_db[key_name]
    user_id = str(user_id)
    
    if user_id in key["used_by"]:
        return False, f"{ICONS['warning']} Bạn đã sử dụng key này!"
    
    if key["used_count"] >= key["max_uses"]:
        return False, f"{ICONS['clock']} Key đã hết lượt sử dụng!"
    
    extend = user_id in users and users[user_id].get("vip_active")
    exp_date = activate_vip(user_id, key["days"], extend)
    
    key["used_count"] += 1
    key["used_by"].append(user_id)
    EnhancedDatabase.save(keys_db, 'keys')
    
    log_user_action(user_id, "use_vip_key", {"key": key_name, "days": key["days"]})
    return True, f"{ICONS['success']} Kích hoạt VIP {key['days']} ngày thành công!\n{ICONS['clock']} Hết hạn: {exp_date}"

def track_activity(user_id, action, details=None):
    user_id = str(user_id)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    activity[user_id] = activity.get(user_id, {
        "first_seen": now,
        "last_seen": now,
        "request_count": 0,
        "actions": []
    })
    
    activity[user_id]["last_seen"] = now
    activity[user_id]["request_count"] += 1
    activity[user_id]["actions"].append({
        "action": action,
        "timestamp": now,
        "details": details or {}
    })
    
    EnhancedDatabase.save(activity, 'activity')

def create_referral_code(user_id):
    code = f"REF1DAY_{user_id}_{int(time.time())}"
    create_premium_code(code, 1, 1)
    return code

def track_referral(referrer_id, referred_id):
    referrer_id = str(referrer_id)
    referred_id = str(referred_id)
    
    if referrer_id not in referral_db:
        referral_db[referrer_id] = []
    
    if referred_id not in referral_db[referrer_id]:
        referral_db[referrer_id].append(referred_id)
        EnhancedDatabase.save(referral_db, 'referral')
        
        reward_code = create_referral_code(referrer_id)
        try:
            bot.send_message(
                referrer_id,
                f"""
{ICONS['success']} Chúc mừng bạn đã mời thành công ID {referred_id}!
🔑 Mã thưởng: <code>{reward_code}</code>
📋 Sử dụng: /code {reward_code}
                """,
                parse_mode="HTML"
            )
            log_user_action(referrer_id, "referral_success", {"referred_id": referred_id})
        except Exception as e:
            logger.error(f"Error sending referral reward: {str(e)}")

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def create_deposit_request(user_id, amount):
    deposit_id = f"DEP{int(time.time())}"
    deposits_db[deposit_id] = {
        "user_id": str(user_id),
        "amount": amount,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "processed_at": None,
        "processed_by": None
    }
    EnhancedDatabase.save(deposits_db, 'deposits')
    
    log_user_action(user_id, "create_deposit", {"deposit_id": deposit_id, "amount": amount})
    return deposit_id

def create_withdrawal_request(user_id, amount, account_info):
    withdrawal_id = f"WDR{int(time.time())}"
    withdrawals_db[withdrawal_id] = {
        "user_id": str(user_id),
        "amount": amount,
        "account_info": account_info,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "processed_at": None,
        "processed_by": None
    }
    EnhancedDatabase.save(withdrawals_db, 'withdrawals')
    
    log_user_action(user_id, "create_withdrawal", {"withdrawal_id": withdrawal_id, "amount": amount})
    return withdrawal_id

def get_user_status(user_id):
    user_id = str(user_id)
    if is_premium_user(user_id):
        return f"{ICONS['crown']} USER VIP"
    elif is_vip_active(user_id):
        return f"{ICONS['vip']} Đã kích hoạt"
    else:
        return f"{ICONS['lock']} Chưa kích hoạt"

def get_user_permissions(user_id):
    user_id = str(user_id)
    return staff_db.get(user_id, {}).get("permissions", [])

def add_staff(user_id, permissions, added_by=None):
    user_id = str(user_id)
    staff_db[user_id] = {
        "permissions": permissions,
        "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "added_by": str(added_by) if added_by else None
    }
    EnhancedDatabase.save(staff_db, 'staff')
    
    if added_by:
        log_admin_action(added_by, "add_staff", {"staff_id": user_id, "permissions": permissions})

def remove_staff(user_id, removed_by=None):
    user_id = str(user_id)
    if user_id in staff_db:
        del staff_db[user_id]
        EnhancedDatabase.save(staff_db, 'staff')
        
        if removed_by:
            log_admin_action(removed_by, "remove_staff", {"staff_id": user_id})
        return True
    return False

def can_user_perform(user_id, permission):
    if int(user_id) == ADMIN_ID:
        return True
    return permission in get_user_permissions(user_id)

def get_all_users():
    return list(users.keys())

def save_broadcast_message(content, sent_by, total_users, success_count):
    message_id = f"BC{int(time.time())}"
    broadcast_messages[message_id] = {
        "content": content,
        "sent_by": sent_by,
        "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_users": total_users,
        "success_count": success_count
    }
    EnhancedDatabase.save(broadcast_messages, 'broadcast_messages')
    
    log_admin_action(sent_by, "broadcast", {
        "message_id": message_id,
        "total_users": total_users,
        "success_count": success_count
    })
    return message_id

def ban_user(user_id, banned_by=None):
    user_id = str(user_id)
    if user_id not in banned_users:
        banned_users.append(user_id)
        EnhancedDatabase.save(banned_users, 'banned_users')
        
        if banned_by:
            log_admin_action(banned_by, "ban_user", {"user_id": user_id})
        return True
    return False

def unban_user(user_id, unbanned_by=None):
    user_id = str(user_id)
    if user_id in banned_users:
        banned_users.remove(user_id)
        EnhancedDatabase.save(banned_users, 'banned_users')
        
        if unbanned_by:
            log_admin_action(unbanned_by, "unban_user", {"user_id": user_id})
        return True
    return False

def is_user_banned(user_id):
    return str(user_id) in banned_users

def check_admin_auth(user_id):
    return security_db.get('admin_auth', {}).get(str(user_id), False)

def require_admin_auth(user_id):
    security_db['admin_auth'] = security_db.get('admin_auth', {})
    security_db['admin_auth'][str(user_id)] = False
    EnhancedDatabase.save(security_db, 'security')

def verify_admin_auth(user_id, secret_key):
    if secret_key == ADMIN_SECRET_KEY:
        security_db['admin_auth'] = security_db.get('admin_auth', {})
        security_db['admin_auth'][str(user_id)] = True
        EnhancedDatabase.save(security_db, 'security')
        return True
    return False

def is_maintenance_mode():
    return maintenance_mode

def set_maintenance_mode(status):
    global maintenance_mode
    maintenance_mode = status
    config_db['maintenance'] = status
    EnhancedDatabase.save(config_db, 'config')

# ========== SUNWIN BOT CORE NÂNG CẤP ==========
class SunWinBot:
    def __init__(self, user_id):
        self.user_id = str(user_id)
        self.running = False
        self.thread = None
        self.last_session = None
        self.history = []
        self.stop_event = threading.Event()
        self.correct_predictions = 0
        self.wrong_predictions = 0
        self.last_update = None
        self.api_url = "https://api.sunwin.com.vn/predictions"  # Thay bằng API thực tế

    def start(self, chat_id):
        if self.running:
            return False
        
        self.running = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run_bot, args=(chat_id,))
        self.thread.daemon = True
        self.thread.start()
        
        sunwin_sessions[self.user_id] = {
            "running": True,
            "chat_id": chat_id,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "bot_instance": self
        }
        EnhancedDatabase.save(sunwin_sessions, 'sunwin_sessions')
        
        log_user_action(self.user_id, "start_sunwin_bot")
        return True

    def stop(self):
        if not self.running:
            return False
        
        self.running = False
        self.stop_event.set()
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
        
        if self.user_id in sunwin_sessions:
            del sunwin_sessions[self.user_id]
            EnhancedDatabase.save(sunwin_sessions, 'sunwin_sessions')
        
        log_user_action(self.user_id, "stop_sunwin_bot")
        return True

    def _run_bot(self, chat_id):
        while self.running and not self.stop_event.is_set():
            try:
                if is_maintenance_mode():
                    bot.send_message(chat_id, f"{ICONS['warning']} Bot đang bảo trì, tạm dừng hoạt động...")
                    time.sleep(60)
                    continue
                
                data = self._get_sunwin_data()
                if data and data.get("Phien") != self.last_session:
                    self.last_session = data.get("Phien")
                    self._send_result(chat_id, data)
                    self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self._update_prediction_stats(data)
                
                time.sleep(5)
            except Exception as e:
                logger.error(f"SunWinBot error: {str(e)}")
                time.sleep(10)

    def _get_sunwin_data(self):
        try:
            # Gọi API thực tế
            response = requests.get(self.api_url)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API Error: Status code {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"API Connection Error: {str(e)}")
            return None

    def _update_prediction_stats(self, data):
        if data.get("prediction") == data.get("Ket_qua"):
            self.correct_predictions += 1
        else:
            self.wrong_predictions += 1

    def _send_result(self, chat_id, data):
        try:
            msg = self._format_message(data)
            sent_msg = bot.send_message(chat_id, msg)
            
            self.history.insert(0, {
                "message": msg,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": data
            })
            
            if len(self.history) > 100:
                self.history = self.history[:100]
        except Exception as e:
            logger.error(f"Send message error: {str(e)}")

    def _format_message(self, data):
        current_time = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        return f"""
{ICONS['sun']} SUNWIN BOT - DỰ ĐOÁN CHUẨN {data.get('tincay', '80%')} {ICONS['sun']}
══════════════════════════
{ICONS['info']} Mã Phiên: {data.get("Phien", "N/A")}
{ICONS['dice']} Xúc Xắc: {data.get('Xuc_xac_1', 0)} - {data.get('Xuc_xac_2', 0)} - {data.get('Xuc_xac_3', 0)} | Tổng: {data.get('Tong', 0)}
{ICONS['stats']} Kết Quả: {data.get('Ket_qua', 'N/A')}
──────────────────────────
{ICONS['engine']} Dự đoán phiên {data.get('Next_phien', 'N/A')}: {data.get('prediction', 'N/A')}
{ICONS['file']} Lý do: {data.get('reason', 'Không rõ')}
{ICONS['chart']} Tin Cậy: {data.get('tincay', '0%')}
{ICONS['check']} Đúng: {data.get('Dudoan_dung', 0)} | Sai: {data.get('Dudoan_sai', 0)}
{ICONS['time']} Giờ VN: {current_time}
══════════════════════════
{ICONS['vip']} SUNWIN VIP BOT {ICONS['vip']}
"""

    def get_status(self):
        return {
            "running": self.running,
            "last_session": self.last_session,
            "last_update": self.last_update,
            "correct_predictions": self.correct_predictions,
            "wrong_predictions": self.wrong_predictions,
            "history_count": len(self.history)
        }
# ==============================================
# HỆ THỐNG PHÂN TÍCH MD5 NÂNG CẤP
# ==============================================
class MD5Analyzer:
    @staticmethod
    def hyper_ai_engine(md5_hash):
        md5_hash = md5_hash.lower().strip()
        if len(md5_hash) != 32 or not re.match(r'^[a-f0-9]{32}$', md5_hash):
            raise ValueError("MD5 không hợp lệ")
        
        hex_bytes = [int(md5_hash[i:i+2], 16) for i in range(0, len(md5_hash), 2)]
        byte_array = np.array(hex_bytes)
        total_sum = sum(hex_bytes)

        # Thuật toán 1: Hyper-AI 7 Engines
        quantum_sum = sum(byte_array[i] * math.cos(i * math.pi/16) for i in range(16))
        neural_score = sum(byte_array[i] * (1.618 ** (i % 5)) for i in range(16))
        fractal_dim = sum(byte_array[i] * (1 + math.sqrt(5)) / 2 for i in range(16))
        score1 = (quantum_sum + neural_score + fractal_dim) % 20
        result1 = "TÀI" if score1 < 10 else "XỈU"
        prob1 = 95 - abs(score1 - 10) * 4.5 if score1 < 10 else 50 + (score1 - 10) * 4.5

        # Thuật toán 2: Diamond AI 7
        nums = [int(c, 16) for c in md5_hash]
        avg = sum(nums) / 32
        even_count = sum(1 for n in nums if n % 2 == 0)
        over8_count = sum(1 for n in nums if n > 8)
        score2 = (1 if avg > 7.5 else 0) + (1 if even_count > 16 else 0) + (1 if over8_count >= 10 else 0)
        result2 = "TÀI" if score2 >= 2 else "XỈU"
        prob2 = 90 if score2 == 3 else 75 if score2 == 2 else 60
        prob2 = prob2 if result2 == "TÀI" else 100 - prob2

        # Thuật toán 3: AI-Tech Titans
        x = int(md5_hash, 16)
        result3 = "TÀI" if x % 2 == 0 else "XỈU"
        prob3 = 75.0

        # Kết quả cuối cùng
        weights = [0.5, 0.3, 0.2]
        final_score = (score1 * weights[0] + score2 * 5 * weights[1] + (0 if result3 == "XỈU" else 10) * weights[2])
        final_result = "TÀI" if final_score < 10 else "XỈU"
        final_prob = (prob1 * weights[0] + prob2 * weights[1] + prob3 * weights[2])
        
        if reverse_mode:
            final_result = "XỈU" if final_result == "TÀI" else "TÀI"
            final_prob = 100 - final_prob

        risk_level = "THẤP" if final_prob > 80 else "TRUNG BÌNH" if final_prob > 60 else "CAO"
        
        return {
            "total_sum": total_sum,
            "algo1": {"result": result1, "prob": f"{prob1:.1f}%", "score": score1},
            "algo2": {"result": result2, "prob": f"{prob2:.1f}%", "score": score2},
            "algo3": {"result": result3, "prob": f"{prob3:.1f}%", "score": x % 2},
            "final": {"result": final_result, "prob": f"{final_prob:.1f}%"},
            "risk": risk_level,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reversed": reverse_mode
        }

# ==============================================
# GIAO DIỆN NGƯỜI DÙNG NÂNG CẤP
# ==============================================
class EnhancedUserInterface:
    @staticmethod
    def create_main_menu():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            types.KeyboardButton(f"{ICONS['analyze']} Phân Tích MD5"),
            types.KeyboardButton(f"{ICONS['vip']} Nâng Cấp VIP")
        )
        markup.add(
            types.KeyboardButton(f"{ICONS['stats']} Thống Kê"),
            types.KeyboardButton(f"{ICONS['history']} Lịch Sử")
        )
        markup.add(
            types.KeyboardButton(f"{ICONS['invite']} Mời Bạn"),
            types.KeyboardButton(f"{ICONS['help']} Trợ Giúp")
        )
        return markup

    @staticmethod
    def create_vip_menu():
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['vip']} 1 NGÀY - 20K", callback_data="buy_1"),
            types.InlineKeyboardButton(f"{ICONS['vip']} 7 NGÀY - 60K", callback_data="buy_7")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['vip']} 30 NGÀY - 120K", callback_data="buy_30"),
            types.InlineKeyboardButton(f"{ICONS['vip']} 60 NGÀY - 180K", callback_data="buy_60")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['crown']} 90 NGÀY - 250K", callback_data="buy_90"),
            types.InlineKeyboardButton(f"{ICONS['crown']} 180 NGÀY - 450K", callback_data="buy_180")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['crown']} 365 NGÀY - 800K", callback_data="buy_365")
        )
        return markup

    @staticmethod
    def create_deposit_confirm():
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['success']} Xác nhận chuyển khoản", callback_data="confirm_deposit"),
            types.InlineKeyboardButton(f"{ICONS['error']} Hủy bỏ", callback_data="cancel_deposit")
        )
        return markup

    @staticmethod
    def create_withdrawal_confirm():
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['success']} Xác nhận rút tiền", callback_data="confirm_withdrawal"),
            types.InlineKeyboardButton(f"{ICONS['error']} Hủy bỏ", callback_data="cancel_withdrawal")
        )
        return markup

    @staticmethod
    def create_admin_actions(deposit_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['success']} Duyệt", callback_data=f"approve_{deposit_id}"),
            types.InlineKeyboardButton(f"{ICONS['error']} Từ chối", callback_data=f"reject_{deposit_id}")
        )
        return markup

    @staticmethod
    def create_admin_withdrawal_actions(withdrawal_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['success']} Duyệt", callback_data=f"approve_wdr_{withdrawal_id}"),
            types.InlineKeyboardButton(f"{ICONS['error']} Từ chối", callback_data=f"reject_wdr_{withdrawal_id}")
        )
        return markup

    @staticmethod
    def create_result_message(md5_input, analysis):
        mode = "ĐẢO" if analysis["reversed"] else "BÌNH THƯỜNG"
        return f"""
{ICONS['engine']} HYPER-AI 7 ENGINES PRO MAX {ICONS['engine']}
──────────────────────────────
{ICONS['info']} Phiên bản: HYPER-AI 7 ENGINES
{ICONS['lock']} MD5: <code>{md5_input[:8]}...{md5_input[-8:]}</code>
{ICONS['stats']} Tổng HEX: <code>{analysis['total_sum']}</code>
{ICONS['engine']} Chế độ: <code>{mode}</code>
──────────────────────────────
🌌 THUẬT TOÁN HYPER-AI
{ICONS['tai' if analysis['algo1']['result'] == 'TÀI' else 'xiu']} Dự đoán: <b>{analysis['algo1']['result']}</b>
{ICONS['stats']} Xác suất: <code>{analysis['algo1']['prob']}</code>

🧬 THUẬT TOÁN DIAMOND AI
{ICONS['tai' if analysis['algo2']['result'] == 'TÀI' else 'xiu']} Dự đoán: <b>{analysis['algo2']['result']}</b>
{ICONS['stats']} Xác suất: <code>{analysis['algo2']['prob']}</code>

🦠 THUẬT TOÁN AI-TECH TITANS
{ICONS['tai' if analysis['algo3']['result'] == 'TÀI' else 'xiu']} Dự đoán: <b>{analysis['algo3']['result']}</b>
{ICONS['stats']} Xác suất: <code>{analysis['algo3']['prob']}</code>
──────────────────────────────
📊 THỐNG KÊ THUẬT TOÁN
{ICONS['stats']} Hyper-AI: <code>{analysis['algo1']['score']:.2f}</code>
{ICONS['stats']} Diamond AI: <code>{analysis['algo2']['score']:.2f}</code>
{ICONS['stats']} AI-Tech: <code>{analysis['algo3']['score']:.2f}</code>
──────────────────────────────
🎯 KẾT LUẬN CUỐI CÙNG
{ICONS['tai' if analysis['final']['result'] == 'TÀI' else 'xiu']} Dự đoán: <b>{analysis['final']['result']}</b>
{ICONS['stats']} Xác suất: <code>{analysis['final']['prob']}</code>
{ICONS['risk']} Rủi ro: <b>{analysis['risk']}</b>
{ICONS['time']} Thời gian: {analysis['timestamp']}
──────────────────────────────
"""

    @staticmethod
    def create_admin_menu():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            types.KeyboardButton(f"{ICONS['user']} Quản lý User"),
            types.KeyboardButton(f"{ICONS['vip']} Quản lý VIP")
        )
        markup.add(
            types.KeyboardButton(f"{ICONS['money']} Quản lý Tiền"),
            types.KeyboardButton(f"{ICONS['settings']} Cài đặt")
        )
        markup.add(
            types.KeyboardButton(f"{ICONS['broadcast']} Gửi thông báo"),
            types.KeyboardButton(f"{ICONS['stats']} Thống kê")
        )
        markup.add(
            types.KeyboardButton(f"{ICONS['help']} Trở về menu chính")
        )
        return markup

    @staticmethod
    def create_user_management_menu():
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['add']} Thêm CTV", callback_data="admin_add_staff"),
            types.InlineKeyboardButton(f"{ICONS['remove']} Xóa CTV", callback_data="admin_remove_staff")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['ban']} Ban User", callback_data="admin_ban_user"),
            types.InlineKeyboardButton(f"{ICONS['unlock']} Gỡ Ban", callback_data="admin_unban_user")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['list']} Danh sách CTV", callback_data="admin_list_staff"),
            types.InlineKeyboardButton(f"{ICONS['list']} Danh sách Ban", callback_data="admin_list_banned")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['back']} Quay lại", callback_data="admin_back")
        )
        return markup

    @staticmethod
    def create_vip_management_menu():
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['add']} Tạo Code VIP", callback_data="admin_create_code"),
            types.InlineKeyboardButton(f"{ICONS['add']} Tạo Key VIP", callback_data="admin_create_key")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['list']} Danh sách Code", callback_data="admin_list_codes"),
            types.InlineKeyboardButton(f"{ICONS['list']} Danh sách Key", callback_data="admin_list_keys")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['remove']} Xóa Code", callback_data="admin_delete_code"),
            types.InlineKeyboardButton(f"{ICONS['remove']} Xóa Key", callback_data="admin_delete_key")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['back']} Quay lại", callback_data="admin_back")
        )
        return markup

    @staticmethod
    def create_money_management_menu():
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['money']} Nạp tiền User", callback_data="admin_add_balance"),
            types.InlineKeyboardButton(f"{ICONS['money']} Trừ tiền User", callback_data="admin_subtract_balance")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['list']} Đơn nạp tiền", callback_data="admin_list_deposits"),
            types.InlineKeyboardButton(f"{ICONS['list']} Đơn rút tiền", callback_data="admin_list_withdrawals")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['stats']} Thống kê giao dịch", callback_data="admin_deposit_stats"),
            types.InlineKeyboardButton(f"{ICONS['settings']} Cài đặt phí", callback_data="admin_fee_settings")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['back']} Quay lại", callback_data="admin_back")
        )
        return markup

    @staticmethod
    def create_settings_menu():
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['settings']} Bật chế độ đảo", callback_data="admin_set_reverse_on"),
            types.InlineKeyboardButton(f"{ICONS['settings']} Tắt chế độ đảo", callback_data="admin_set_reverse_off")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['backup']} Sao lưu dữ liệu", callback_data="admin_backup_data"),
            types.InlineKeyboardButton(f"{ICONS['stats']} Thống kê hệ thống", callback_data="admin_system_stats")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['settings']} Cài đặt nhóm", callback_data="admin_group_settings"),
            types.InlineKeyboardButton(f"{ICONS['settings']} Cài đặt phí", callback_data="admin_fee_settings")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['security']} Bảo mật", callback_data="admin_security"),
            types.InlineKeyboardButton(f"{ICONS['tools']} Bảo trì", callback_data="admin_maintenance")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['back']} Quay lại", callback_data="admin_back")
        )
        return markup

    @staticmethod
    def create_stats_menu():
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['stats']} Thống kê user", callback_data="admin_user_stats"),
            types.InlineKeyboardButton(f"{ICONS['stats']} Thống kê dự đoán", callback_data="admin_prediction_stats")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['stats']} Thống kê giao dịch", callback_data="admin_transaction_stats"),
            types.InlineKeyboardButton(f"{ICONS['stats']} Thống kê VIP", callback_data="admin_vip_stats")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['stats']} Thống kê hoạt động", callback_data="admin_activity_stats"),
            types.InlineKeyboardButton(f"{ICONS['stats']} Thống kê lợi nhuận", callback_data="admin_profit_stats")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['back']} Quay lại", callback_data="admin_back")
        )
        return markup

    @staticmethod
    def create_security_menu():
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['security']} Xác thực Admin", callback_data="admin_auth"),
            types.InlineKeyboardButton(f"{ICONS['shield']} Đổi mật khẩu", callback_data="admin_change_password")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['search']} Xem log đăng nhập", callback_data="admin_view_auth_logs"),
            types.InlineKeyboardButton(f"{ICONS['list']} IP bị chặn", callback_data="admin_blocked_ips")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['back']} Quay lại", callback_data="admin_back")
        )
        return markup

    @staticmethod
    def create_maintenance_menu():
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['tools']} Bật bảo trì", callback_data="admin_maintenance_on"),
            types.InlineKeyboardButton(f"{ICONS['tools']} Tắt bảo trì", callback_data="admin_maintenance_off")
        )
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['back']} Quay lại", callback_data="admin_back")
        )
        return markup

    @staticmethod
    def create_back_button():
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"{ICONS['back']} Quay lại", callback_data="admin_back"))
        return markup

    @staticmethod
    def create_feedback_buttons(md5_hash):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"{ICONS['correct']} Đúng", callback_data=f"correct_{md5_hash}"),
            types.InlineKeyboardButton(f"{ICONS['wrong']} Sai", callback_data=f"wrong_{md5_hash}")
        )
        return markup

# ==============================================
# QUẢN LÝ DỮ LIỆU NÂNG CẤP
# ==============================================
def save_prediction(user_id, md5, analysis, is_correct=None):
    user_id = str(user_id)
    history[user_id] = history.get(user_id, [])
    history[user_id].append({
        "md5": md5,
        "prediction": analysis,
        "timestamp": analysis["timestamp"],
        "is_correct": is_correct,
        "awaiting_feedback": True if is_correct is None else False
    })
    if len(history[user_id]) > 100:
        history[user_id] = history[user_id][-100:]
    EnhancedDatabase.save(history, 'history')
    
    log_user_action(user_id, "save_prediction", {
        "md5": md5[:8] + "..." + md5[-8:],
        "prediction": analysis["final"]["result"],
        "probability": analysis["final"]["prob"]
    })

def check_feedback_status(user_id):
    user_id = str(user_id)
    if user_id in history:
        for entry in history[user_id]:
            if entry.get("awaiting_feedback", False):
                return True, entry["md5"]
    return False, None

def get_user_stats(user_id):
    user_id = str(user_id)
    if user_id not in history or not history[user_id]:
        return None
    
    user_history = history[user_id]
    total = len(user_history)
    correct = sum(1 for entry in user_history if entry.get("is_correct") is True)
    wrong = sum(1 for entry in user_history if entry.get("is_correct") is False)
    accuracy = correct / total * 100 if total > 0 else 0
    
    return {
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "accuracy": accuracy
    }

def get_global_stats():
    total = 0
    correct = 0
    wrong = 0
    
    for user_history in history.values():
        for entry in user_history:
            total += 1
            if entry.get("is_correct") is True:
                correct += 1
            elif entry.get("is_correct") is False:
                wrong += 1
    
    accuracy = correct / total * 100 if total > 0 else 0
    
    return {
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "accuracy": accuracy
    }

def get_deposit_stats():
    total = len(deposits_db)
    pending = sum(1 for d in deposits_db.values() if d["status"] == "pending")
    approved = sum(1 for d in deposits_db.values() if d["status"] == "approved")
    rejected = sum(1 for d in deposits_db.values() if d["status"] == "rejected")
    total_amount = sum(d["amount"] for d in deposits_db.values() if d["status"] == "approved")
    
    return {
        "total": total,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
        "total_amount": total_amount
    }

def get_withdrawal_stats():
    total = len(withdrawals_db)
    pending = sum(1 for w in withdrawals_db.values() if w["status"] == "pending")
    approved = sum(1 for w in withdrawals_db.values() if w["status"] == "approved")
    rejected = sum(1 for w in withdrawals_db.values() if w["status"] == "rejected")
    total_amount = sum(w["amount"] for w in withdrawals_db.values() if w["status"] == "approved")
    
    return {
        "total": total,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
        "total_amount": total_amount
    }

def get_system_stats():
    return {
        "total_users": len(users),
        "vip_users": sum(1 for u in users.values() if u.get("vip_active")),
        "premium_users": sum(1 for u in users.values() if u.get("premium")),
        "active_users": sum(1 for a in activity.values() if (datetime.now() - datetime.strptime(a["last_seen"], "%Y-%m-%d %H:%M:%S")).days < 7),
        "total_deposits": len(deposits_db),
        "total_withdrawals": len(withdrawals_db),
        "total_codes": len(codes_db),
        "total_keys": len(keys_db),
        "running_sunwin_bots": sum(1 for s in sunwin_sessions.values() if s.get("running"))
    }

def get_vip_stats():
    vip_counts = defaultdict(int)
    for user in users.values():
        if user.get("vip_active"):
            exp_date = user.get("vip_expire", "")
            try:
                expire_date = datetime.strptime(exp_date, "%Y-%m-%d %H:%M:%S")
                days_left = (expire_date - datetime.now()).days
                if days_left >= 365:
                    vip_counts["1_year"] += 1
                elif days_left >= 180:
                    vip_counts["6_months"] += 1
                elif days_left >= 90:
                    vip_counts["3_months"] += 1
                elif days_left >= 30:
                    vip_counts["1_month"] += 1
                elif days_left >= 7:
                    vip_counts["1_week"] += 1
                else:
                    vip_counts["1_day"] += 1
            except:
                pass
    
    return vip_counts

def get_profit_stats():
    total_deposits = sum(d["amount"] for d in deposits_db.values() if d["status"] == "approved")
    total_withdrawals = sum(w["amount"] for w in withdrawals_db.values() if w["status"] == "approved")
    profit = total_deposits - total_withdrawals
    
    return {
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
        "profit": profit,
        "profit_percentage": (profit / total_deposits * 100) if total_deposits > 0 else 0
    }

def get_activity_stats(days=7):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    active_users = 0
    predictions = 0
    deposits = 0
    withdrawals = 0
    vip_activations = 0
    
    for user_id, user_activity in activity.items():
        last_seen = datetime.strptime(user_activity["last_seen"], "%Y-%m-%d %H:%M:%S")
        if start_date <= last_seen <= end_date:
            active_users += 1
    
    for user_history in history.values():
        for entry in user_history:
            entry_date = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            if start_date <= entry_date <= end_date:
                predictions += 1
    
    for deposit in deposits_db.values():
        deposit_date = datetime.strptime(deposit["created_at"], "%Y-%m-%d %H:%M:%S")
        if start_date <= deposit_date <= end_date:
            deposits += 1
    
    for withdrawal in withdrawals_db.values():
        withdrawal_date = datetime.strptime(withdrawal["created_at"], "%Y-%m-%d %H:%M:%S")
        if start_date <= withdrawal_date <= end_date:
            withdrawals += 1
    
    for user in users.values():
        if user.get("vip_active"):
            try:
                activate_date = datetime.strptime(user.get("vip_expire", ""), "%Y-%m-%d %H:%M:%S") - timedelta(days=user.get("vip_days", 0))
                if start_date <= activate_date <= end_date:
                    vip_activations += 1
            except:
                pass
    
    return {
        "active_users": active_users,
        "predictions": predictions,
        "deposits": deposits,
        "withdrawals": withdrawals,
        "vip_activations": vip_activations
    }

# ==============================================
# XỬ LÝ LỆNH NÂNG CẤP
# ==============================================
@bot.message_handler(commands=['start'])
def handle_start(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    
    user_id = str(message.from_user.id)
    name = message.from_user.first_name or "Người Dùng"
    
    if is_user_banned(user_id):
        bot.send_message(message.chat.id, f"{ICONS['error']} Tài khoản của bạn đã bị khóa!")
        return
    
    # Check admin authentication
    if message.from_user.id == ADMIN_ID and not check_admin_auth(user_id):
        msg = bot.send_message(message.chat.id, f"{ICONS['security']} Vui lòng nhập mã xác thực admin:")
        bot.register_next_step_handler(msg, process_admin_auth)
        return
    
    if user_id in users:
        response_text = f"""
{ICONS['user']} CHÀO MỪNG ĐẾN VỚI BOT MD5 V3 {ICONS['user']}

👋 Chào mừng {name} quay lại bot

🧠 AI TECHTITANS & 10 AI KHÁC
🔋 Trạng thái: {get_user_status(user_id)}

📝 Sử dụng lệnh /help để xem lệnh
⚙ Cre : Huy Dev
"""
        bot.send_message(message.chat.id, response_text, reply_markup=EnhancedUserInterface.create_main_menu())
        return
    
    # New user flow
    if len(message.text.split()) > 1:
        referrer_id = message.text.split()[1]
        if referrer_id != user_id:
            track_referral(referrer_id, message.from_user.id)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"{ICONS['success']} Xác Nhận Nhóm", callback_data="verify_groups"))
    
    response_text = f"""
{ICONS['info']} YÊU CẦU ĐỂ SỬ DỤNG BOT {ICONS['info']}

👋 Chào mừng {name}, thực hiện yêu cầu bên dưới để sử dụng bot.

❕Tham gia nhóm Telegram của chúng tôi để nhận ngay tấm vé
🎟 PREMIUM7DAY

1⃣ : @techtitansteam
2⃣ : @techtitansteamchat

🎉 Sau khi tham gia đủ các nhóm trên, nhấn vào nút \"✅ Xác Nhận\" để nhận ngay vé PREMIUM7DAY
"""
    
    bot.send_message(message.chat.id, response_text, reply_markup=markup)
    track_activity(message.from_user.id, "start")

def process_admin_auth(message):
    user_id = str(message.from_user.id)
    if verify_admin_auth(user_id, message.text):
        bot.send_message(message.chat.id, f"{ICONS['success']} Xác thực thành công!", reply_markup=EnhancedUserInterface.create_admin_menu())
    else:
        security_db['failed_attempts'] = security_db.get('failed_attempts', {})
        security_db['failed_attempts'][user_id] = security_db['failed_attempts'].get(user_id, 0) + 1
        EnhancedDatabase.save(security_db, 'security')
        
        if security_db['failed_attempts'].get(user_id, 0) >= 3:
            bot.send_message(message.chat.id, f"{ICONS['error']} Quá nhiều lần thử sai. Hệ thống sẽ khóa trong 5 phút.")
            time.sleep(300)
            security_db['failed_attempts'][user_id] = 0
            EnhancedDatabase.save(security_db, 'security')
        else:
            msg = bot.send_message(message.chat.id, f"{ICONS['error']} Mã xác thực không đúng. Vui lòng thử lại:")
            bot.register_next_step_handler(msg, process_admin_auth)

@bot.message_handler(commands=['help'])
def handle_help(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    
    response_text = f"""
{ICONS['help']} DANH SÁCH LỆNH {ICONS['help']}

🪪 LỆNH CÁ NHÂN
👤 /info - Xem thông tin tài khoản
🚸 /invite - Mời bạn bè
📊 /stats - Xem thống kê
🗝 /code [mã] - Kích hoạt 
🔑 /key [key_vip] - Kích hoạt vip
🎯 /autusun - Chạy bot Sun Win

🛍 LỆNH MUA HÀNG 
📥 /nap - Để nạp tiền mua key vip
📤 /rut - Rút tiền từ tài khoản
📋 /vip - Giá key vip

🛡 LỆNH ADMIN 
🗂 /admin - Xem lệnh admin
🤝 /setctv [id] [stt]

⚙ Cre : Huy Dev
"""
    bot.send_message(message.chat.id, response_text, reply_markup=EnhancedUserInterface.create_main_menu())

@bot.message_handler(commands=['info'])
def handle_info(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    
    user_id = str(message.from_user.id)
    name = message.from_user.first_name or "Không có tên"
    username = f"@{message.from_user.username}" if message.from_user.username else "Không có"
    balance = get_user_balance(user_id)
    status = get_user_status(user_id)
    join_date = users.get(user_id, {}).get("first_seen", "Không có dữ liệu")
    ref_count = len(referral_db.get(user_id, []))
    
    permissions = get_user_permissions(user_id)
    role = "ADMIN" if message.from_user.id == ADMIN_ID else "CTV" if permissions else "USER"
    
    response_text = f"""
{ICONS['user']} THÔNG TIN CÁ NHÂN {ICONS['user']}

👷‍♂ Tên : {name}
📌 Username : {username}
🆔 ID : {user_id}
🚸 Bạn bè : {ref_count}
🔋 Trạng thái : {status}
💰 Số dư : {balance:,} VNĐ
❗️ Quyền hiện tại : {role}

🗓 Tham gia : {join_date}
"""
    bot.send_message(message.chat.id, response_text)

@bot.message_handler(commands=['stats'])
def handle_stats(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    
    stats = get_user_stats(message.from_user.id)
    if not stats:
        response_text = f"""
{ICONS['stats']} THỐNG KÊ TÀI KHOẢN {ICONS['stats']}

✅ Số trận đúng: 0
❌ Số trận sai : 0
🗞 Tổng dự đoán: 0
🎉 Tỉ lệ win : 0%

🎲 Chúc ae đánh đâu thắng đó 🎲
"""
    else:
        response_text = f"""
{ICONS['stats']} THỐNG KÊ TÀI KHOẢN {ICONS['stats']}

✅ Số trận đúng: {stats['correct']}
❌ Số trận sai : {stats['wrong']}
🗞 Tổng dự đoán: {stats['total']}
🎉 Tỉ lệ win : {stats['accuracy']:.1f}%

🎲 Chúc ae đánh đâu thắng đó 🎲
"""
    bot.send_message(message.chat.id, response_text)

@bot.message_handler(commands=['nap'])
def handle_nap(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    user_id = str(message.from_user.id)
    
    # Check for pending deposits
    for dep_id, dep_data in deposits_db.items():
        if dep_data["user_id"] == user_id and dep_data["status"] == "pending":
            bot.send_message(
                message.chat.id,
                f"⛔ Bạn đã có đơn nạp tiền đang chờ duyệt!\n"
                f"💰 Số tiền: {dep_data['amount']:,} VNĐ\n"
                f"⏱ Thời gian: {dep_data['created_at']}\n\n"
                f"📌 Vui lòng chờ admin duyệt hoặc liên hệ {SUPPORT_CONTACT}"
            )
            return
    
    msg = bot.send_message(message.chat.id, "📥 Vui lòng nhập số tiền bạn muốn nạp (tối thiểu 10,000 VNĐ):")
    bot.register_next_step_handler(msg, process_nap_amount)

def process_nap_amount(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    try:
        amount = int(message.text)
        if amount < settings_db.get('min_deposit', 10000):
            bot.send_message(message.chat.id, f"{ICONS['error']} Số tiền nạp tối thiểu là {settings_db.get('min_deposit', 10000):,} VNĐ")
            return
            
        # Create deposit request
        deposit_id = create_deposit_request(message.from_user.id, amount)
        
        response_text = f"""
{ICONS['deposit']} THÔNG TIN NẠP TIỀN {ICONS['deposit']}

💳 Thông tin tài khoản:
🧸Tên : {BANK_ACCOUNT['name']}
🔢STK : {BANK_ACCOUNT['number']}
🏦 Ngân hàng : {BANK_ACCOUNT['bank']}
📝 Nội dung : NAP{message.from_user.id}
💰 Số tiền nạp: {amount:,} VNĐ

📌 Mã đơn nạp: {deposit_id}

📩 Sau khi nạp xong vui lòng nhấn:
\" ✅ Xác nhận chuyển khoản \" bên dưới
"""
        
        bot.send_message(
            message.chat.id, 
            response_text,
            reply_markup=EnhancedUserInterface.create_deposit_confirm()
        )
        
    except ValueError:
        bot.send_message(message.chat.id, f"{ICONS['error']} Số tiền không hợp lệ. Vui lòng nhập số.")

@bot.message_handler(commands=['rut'])
def handle_rut(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    user_id = str(message.from_user.id)
    balance = get_user_balance(user_id)
    
    # Check for pending withdrawals
    for wdr_id, wdr_data in withdrawals_db.items():
        if wdr_data["user_id"] == user_id and wdr_data["status"] == "pending":
            bot.send_message(
                message.chat.id,
                f"⛔ Bạn đã có đơn rút tiền đang chờ duyệt!\n"
                f"💰 Số tiền: {wdr_data['amount']:,} VNĐ\n"
                f"⏱ Thời gian: {wdr_data['created_at']}\n\n"
                f"📌 Vui lòng chờ admin duyệt hoặc liên hệ {SUPPORT_CONTACT}"
            )
            return
    
    min_withdraw = settings_db.get('min_withdraw', 50000)
    if balance < min_withdraw:
        bot.send_message(message.chat.id, f"{ICONS['error']} Số dư tối thiểu để rút là {min_withdraw:,} VNĐ!")
        return
    
    max_withdraw = settings_db.get('max_withdraw', 10000000)
    msg = bot.send_message(message.chat.id, f"📤 Vui lòng nhập số tiền bạn muốn rút (tối thiểu {min_withdraw:,} VNĐ, tối đa {max_withdraw:,} VNĐ):")
    bot.register_next_step_handler(msg, process_rut_amount)

def process_rut_amount(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    try:
        user_id = str(message.from_user.id)
        balance = get_user_balance(user_id)
        amount = int(message.text)
        
        min_withdraw = settings_db.get('min_withdraw', 50000)
        if amount < min_withdraw:
            bot.send_message(message.chat.id, f"{ICONS['error']} Số tiền rút tối thiểu là {min_withdraw:,} VNĐ")
            return
        
        max_withdraw = settings_db.get('max_withdraw', 10000000)
        if amount > max_withdraw:
            bot.send_message(message.chat.id, f"{ICONS['error']} Số tiền rút tối đa là {max_withdraw:,} VNĐ!")
            return
        
        if amount > balance:
            bot.send_message(message.chat.id, f"{ICONS['error']} Số dư không đủ để rút!")
            return
            
        msg = bot.send_message(message.chat.id, "💳 Vui lòng nhập thông tin tài khoản ngân hàng (Tên chủ tài khoản + Số tài khoản + Ngân hàng):")
        bot.register_next_step_handler(msg, lambda m: process_rut_account(m, amount))
        
    except ValueError:
        bot.send_message(message.chat.id, f"{ICONS['error']} Số tiền không hợp lệ. Vui lòng nhập số.")

def process_rut_account(message, amount):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    account_info = message.text.strip()
    user_id = str(message.from_user.id)
    
    # Apply withdrawal fee
    fee_percentage = settings_db.get('fees', {}).get('withdraw', 0.05)
    fee = int(amount * fee_percentage)
    received_amount = amount - fee
    
    # Create withdrawal request
    withdrawal_id = create_withdrawal_request(user_id, amount, account_info)
    
    response_text = f"""
{ICONS['money']} THÔNG TIN RÚT TIỀN {ICONS['money']}

💰 Số tiền rút: {amount:,} VNĐ
💸 Phí rút tiền ({fee_percentage*100}%): {fee:,} VNĐ
💵 Số tiền nhận được: {received_amount:,} VNĐ
💳 Thông tin tài khoản: {account_info}
📌 Mã đơn rút: {withdrawal_id}

📩 Vui lòng nhấn \" ✅ Xác nhận rút tiền \" bên dưới để gửi yêu cầu
"""
    
    bot.send_message(
        message.chat.id, 
        response_text,
        reply_markup=EnhancedUserInterface.create_withdrawal_confirm()
    )

@bot.callback_query_handler(func=lambda call: call.data == "confirm_deposit")
def handle_confirm_deposit(call):
    if is_maintenance_mode() and call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Bot đang bảo trì!")
        return
    
    # Find the latest pending deposit for this user
    user_id = str(call.from_user.id)
    deposit = None
    
    for dep_id, dep_data in deposits_db.items():
        if dep_data["user_id"] == user_id and dep_data["status"] == "pending":
            deposit = dep_data
            deposit["deposit_id"] = dep_id
            break
    
    if not deposit:
        bot.answer_callback_query(call.id, "❌ Không tìm thấy đơn nạp tiền!")
        return
    
    bot.answer_callback_query(call.id, "✅ Đơn nạp tiền đã được gửi đến admin!")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    # Send to admin
    user = call.from_user
    response_text = f"""
{ICONS['money']} ĐƠN NẠP TIỀN MỚI {ICONS['money']}

🧸 Tên: {user.first_name}
📌 Username: @{user.username if user.username else 'N/A'}
🆔 ID: {user.id}
💰 Số tiền: {deposit['amount']:,} VNĐ
⏰ Thời gian: {deposit['created_at']}
🔢 Mã đơn: {deposit['deposit_id']}
"""
    
    bot.send_message(
        ADMIN_ID,
        response_text,
        reply_markup=EnhancedUserInterface.create_admin_actions(deposit['deposit_id'])
    )

@bot.callback_query_handler(func=lambda call: call.data == "confirm_withdrawal")
def handle_confirm_withdrawal(call):
    if is_maintenance_mode() and call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Bot đang bảo trì!")
        return
    
    # Find the latest pending withdrawal for this user
    user_id = str(call.from_user.id)
    withdrawal = None
    
    for wdr_id, wdr_data in withdrawals_db.items():
        if wdr_data["user_id"] == user_id and wdr_data["status"] == "pending":
            withdrawal = wdr_data
            withdrawal["withdrawal_id"] = wdr_id
            break
    
    if not withdrawal:
        bot.answer_callback_query(call.id, "❌ Không tìm thấy đơn rút tiền!")
        return
    
    bot.answer_callback_query(call.id, "✅ Đơn rút tiền đã được gửi đến admin!")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    # Send to admin
    user = call.from_user
    response_text = f"""
{ICONS['money']} ĐƠN RÚT TIỀN MỚI {ICONS['money']}

🧸 Tên: {user.first_name}
📌 Username: @{user.username if user.username else 'N/A'}
🆔 ID: {user.id}
💰 Số tiền: {withdrawal['amount']:,} VNĐ
💳 Thông tin tài khoản: {withdrawal['account_info']}
⏰ Thời gian: {withdrawal['created_at']}
🔢 Mã đơn: {withdrawal['withdrawal_id']}
"""
    
    bot.send_message(
        ADMIN_ID,
        response_text,
        reply_markup=EnhancedUserInterface.create_admin_withdrawal_actions(withdrawal['withdrawal_id'])
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith(('approve_', 'reject_')))
def handle_admin_deposit_action(call):
    if not can_user_perform(call.from_user.id, "approve_deposit"):
        bot.answer_callback_query(call.id, "⛔ Bạn không có quyền!")
        return
    
    action, deposit_id = call.data.split('_', 1)
    
    if deposit_id not in deposits_db:
        bot.answer_callback_query(call.id, "❌ Đơn nạp tiền không tồn tại!")
        return
    
    deposit = deposits_db[deposit_id]
    user_id = deposit["user_id"]
    amount = deposit["amount"]
    
    if action == "approve":
        # Update user balance
        users[user_id] = users.get(user_id, {})
        users[user_id]["balance"] = users[user_id].get("balance", 0) + amount
        EnhancedDatabase.save(users, 'users')
        
        # Update deposit status
        deposit["status"] = "approved"
        deposit["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        deposit["processed_by"] = str(call.from_user.id)
        EnhancedDatabase.save(deposits_db, 'deposits')
        
        # Notify admin
        bot.answer_callback_query(call.id, f"✅ Đã duyệt đơn nạp {amount:,} VNĐ")
        bot.edit_message_text(
            f"✅ ĐÃ DUYỆT ĐƠN NẠP:\n\n"
            f"👤 User ID: {user_id}\n"
            f"💰 Số tiền: {amount:,} VNĐ\n"
            f"⏱ Thời gian: {deposit['processed_at']}\n"
            f"👨‍💼 Xử lý bởi: {call.from_user.first_name}",
            call.message.chat.id,
            call.message.message_id
        )
        
        log_admin_action(call.from_user.id, "approve_deposit", {"deposit_id": deposit_id, "amount": amount})
        
        # Notify user
        try:
            bot.send_message(
                user_id,
                f"✨ Đơn nạp {amount:,} VNĐ đã được duyệt thành công!\n"
                f"💰 Số dư mới: {users[user_id]['balance']:,} VNĐ\n"
                f"📌 Sử dụng lệnh /info để kiểm tra"
            )
        except Exception as e:
            logger.error(f"Error notifying user: {e}")
            
    elif action == "reject":
        # Update deposit status
        deposit["status"] = "rejected"
        deposit["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        deposit["processed_by"] = str(call.from_user.id)
        EnhancedDatabase.save(deposits_db, 'deposits')
        
        # Notify admin
        bot.answer_callback_query(call.id, f"❌ Đã từ chối đơn nạp {amount:,} VNĐ")
        bot.edit_message_text(
            f"❌ ĐÃ TỪ CHỐI ĐƠN NẠP:\n\n"
            f"👤 User ID: {user_id}\n"
            f"💰 Số tiền: {amount:,} VNĐ\n"
            f"⏱ Thời gian: {deposit['processed_at']}\n"
            f"👨‍💼 Xử lý bởi: {call.from_user.first_name}",
            call.message.chat.id,
            call.message.message_id
        )
        
        log_admin_action(call.from_user.id, "reject_deposit", {"deposit_id": deposit_id, "amount": amount})
        
        # Notify user
        try:
            bot.send_message(
                user_id,
                f"❌ Đơn nạp {amount:,} VNĐ đã bị từ chối!\n"
                f"📌 Liên hệ {SUPPORT_CONTACT} để biết thêm chi tiết"
            )
        except Exception as e:
            logger.error(f"Error notifying user: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith(('approve_wdr_', 'reject_wdr_')))
def handle_admin_withdrawal_action(call):
    if not can_user_perform(call.from_user.id, "approve_withdrawal"):
        bot.answer_callback_query(call.id, "⛔ Bạn không có quyền!")
        return
    
    action, withdrawal_id = call.data.split('_', 2)
    
    if withdrawal_id not in withdrawals_db:
        bot.answer_callback_query(call.id, "❌ Đơn rút tiền không tồn tại!")
        return
    
    withdrawal = withdrawals_db[withdrawal_id]
    user_id = withdrawal["user_id"]
    amount = withdrawal["amount"]
    
    if action == "approve":
        # Check user balance
        if users.get(user_id, {}).get("balance", 0) < amount:
            bot.answer_callback_query(call.id, f"❌ User không đủ số dư để rút!")
            return
            
        # Deduct user balance
        users[user_id]["balance"] = users[user_id].get("balance", 0) - amount
        EnhancedDatabase.save(users, 'users')
        
        # Update withdrawal status
        withdrawal["status"] = "approved"
        withdrawal["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        withdrawal["processed_by"] = str(call.from_user.id)
        EnhancedDatabase.save(withdrawals_db, 'withdrawals')
        
        # Notify admin
        bot.answer_callback_query(call.id, f"✅ Đã duyệt đơn rút {amount:,} VNĐ")
        bot.edit_message_text(
            f"✅ ĐÃ DUYỆT ĐƠN RÚT:\n\n"
            f"👤 User ID: {user_id}\n"
            f"💰 Số tiền: {amount:,} VNĐ\n"
            f"💳 Thông tin: {withdrawal['account_info']}\n"
            f"⏱ Thời gian: {withdrawal['processed_at']}\n"
            f"👨‍💼 Xử lý bởi: {call.from_user.first_name}",
            call.message.chat.id,
            call.message.message_id
        )
        
        log_admin_action(call.from_user.id, "approve_withdrawal", {
            "withdrawal_id": withdrawal_id, 
            "amount": amount,
            "account_info": withdrawal['account_info']
        })
        
        # Notify user
        try:
            bot.send_message(
                user_id,
                f"✨ Đơn rút {amount:,} VNĐ đã được duyệt thành công!\n"
                f"💳 Thông tin tài khoản: {withdrawal['account_info']}\n"
                f"📌 Số dư mới: {users[user_id]['balance']:,} VNĐ\n"
                f"⏳ Tiền sẽ được chuyển trong vòng 24h"
            )
        except Exception as e:
            logger.error(f"Error notifying user: {e}")
            
    elif action == "reject":
        # Update withdrawal status
        withdrawal["status"] = "rejected"
        withdrawal["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        withdrawal["processed_by"] = str(call.from_user.id)
        EnhancedDatabase.save(withdrawals_db, 'withdrawals')
        
        # Notify admin
        bot.answer_callback_query(call.id, f"❌ Đã từ chối đơn rút {amount:,} VNĐ")
        bot.edit_message_text(
            f"❌ ĐÃ TỪ CHỐI ĐƠN RÚT:\n\n"
            f"👤 User ID: {user_id}\n"
            f"💰 Số tiền: {amount:,} VNĐ\n"
            f"⏱ Thời gian: {withdrawal['processed_at']}\n"
            f"👨‍💼 Xử lý bởi: {call.from_user.first_name}",
            call.message.chat.id,
            call.message.message_id
        )
        
        log_admin_action(call.from_user.id, "reject_withdrawal", {
            "withdrawal_id": withdrawal_id, 
            "amount": amount
        })
        
        # Notify user
        try:
            bot.send_message(
                user_id,
                f"❌ Đơn rút {amount:,} VNĐ đã bị từ chối!\n"
                f"📌 Liên hệ {SUPPORT_CONTACT} để biết thêm chi tiết"
            )
        except Exception as e:
            logger.error(f"Error notifying user: {e}")

@bot.message_handler(commands=['vip'])
def handle_vip(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    user_id = str(message.from_user.id)
    balance = get_user_balance(user_id)
    
    response_text = f"""
{ICONS['vip']} GIÁ KEY VIP {ICONS['vip']}

💰 Số dư : {balance:,} VNĐ

⚜ KEY 1 NGÀY -- 20,000 VNĐ
⚜ KEY 7 NGÀY -- 60,000 VNĐ
⚜ KEY 1 THÁNG -- 120,000 VNĐ
⚜ KEY 2 THÁNG -- 180,000 VNĐ
⚜ KEY 3 THÁNG -- 250,000 VNĐ
⚜ KEY 6 THÁNG -- 450,000 VNĐ
⚜ KEY 1 NĂM -- 800,000 VNĐ
"""
    
    bot.send_message(
        message.chat.id,
        response_text,
        reply_markup=EnhancedUserInterface.create_vip_menu()
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy_vip(call):
    if is_maintenance_mode() and call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Bot đang bảo trì!")
        return
    
    days = int(call.data.split('_')[1])
    price = get_key_price(days)
    user_id = str(call.from_user.id)
    balance = get_user_balance(user_id)
    
    if balance < price:
        bot.answer_callback_query(call.id, "❌ Số dư không đủ. Vui lòng nạp thêm tiền!")
        return
    
    # Trừ tiền
    users[user_id]["balance"] = balance - price
    EnhancedDatabase.save(users, 'users')
    
    # Tạo và kích hoạt key
    key_name = f"VIP{days}DAY_{generate_random_string()}"
    create_vip_key(key_name, days, 1)
    success, msg = use_vip_key(key_name, user_id)
    
    # Đặt premium=True cho USER VIP
    users[user_id]["premium"] = True
    EnhancedDatabase.save(users, 'users')
    
    response = (
        f"✅ Mua key VIP thành công!\n"
        f"🔑 Key: <code>{key_name}</code>\n"
        f"⏱ Thời hạn: {days} ngày\n"
        f"💰 Số tiền đã trừ: {price:,} VNĐ\n"
        f"💎 Trạng thái: USER VIP\n\n"
        f"{msg}"
    )
    
    bot.send_message(call.message.chat.id, response, parse_mode="HTML")
    bot.answer_callback_query(call.id, "Mua key thành công!")

@bot.message_handler(commands=['taokey'])
def handle_taokey(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if not can_user_perform(message.from_user.id, "taokey"):
        bot.send_message(message.chat.id, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return
    
    parts = message.text.split()
    if len(parts) < 3:
        bot.send_message(message.chat.id, "📌 Sử dụng: /taokey [số_ngày] [số_lần_nhập]")
        return
    
    try:
        days = int(parts[1])
        max_uses = int(parts[2])
        
        key_name = f"VIP{days}DAY_{generate_random_string()}"
        create_vip_key(key_name, days, max_uses, message.from_user.id)
        
        bot.send_message(
            message.chat.id,
            f"✅ Tạo key VIP thành công:\n"
            f"🔑 Key: <code>{key_name}</code>\n"
            f"⏱ Thời hạn: {days} ngày\n"
            f"🔢 Số lần nhập: {max_uses}\n"
            f"💰 Giá trị: {get_key_price(days):,} VNĐ",
            parse_mode="HTML"
        )
    except ValueError:
        bot.send_message(message.chat.id, "❌ Số ngày và số lần nhập phải là số!")

@bot.message_handler(commands=['key'])
def handle_key(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "📌 Sử dụng: /key [mã_key]")
        return
    
    key_name = message.text.split()[1].upper()
    user_id = str(message.from_user.id)
    
    # Check if key exists
    if key_name not in keys_db:
        bot.send_message(message.chat.id, f"❌ Key không tồn tại hoặc đã hết hạn!")
        return
    
    # Check if key is already used by this user
    if user_id in keys_db[key_name]["used_by"]:
        bot.send_message(message.chat.id, f"⚠️ Bạn đã sử dụng key này trước đây!")
        return
    
    # Check if key has remaining uses
    if keys_db[key_name]["used_count"] >= keys_db[key_name]["max_uses"]:
        bot.send_message(message.chat.id, f"⌛ Key đã hết lượt sử dụng!")
        return
    
    # Activate VIP
    success, msg = use_vip_key(key_name, user_id)
    
    # If user is premium (bought VIP), upgrade status
    if success and is_premium_user(user_id):
        activate_premium(user_id)
        msg += "\n\n💎 Trạng thái của bạn đã được nâng cấp lên USER VIP!"
    
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['invite'])
def handle_invite(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    
    user_id = message.from_user.id
    invite_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
    ref_count = len(referral_db.get(str(user_id), []))
    
    response_text = f"""
{ICONS['invite']} MỜI BẠN BÈ {ICONS['invite']}

👥 Mời bạn bè để nhận code kích hoạt 1day
👉 Link mời bạn bè:
{invite_link}

📌 Bạn đã mời được {ref_count} người
"""
    
    bot.send_message(message.chat.id, response_text)

@bot.message_handler(commands=['admin'])
def handle_admin(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if message.from_user.id != ADMIN_ID and not can_user_perform(message.from_user.id, "admin_access"):
        bot.send_message(message.chat.id, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return
    
    admin_commands = f"""
{ICONS['admin']} DANH SÁCH LỆNH ADMIN {ICONS['admin']}

🌀 QUẢN LÝ USER:
/taocode [mã] [ngày] [lần] - Tạo code VIP
/listcode - Xem danh sách code
/delcode [mã] - Xóa code
/ban [id] - Ban user
/unban [id] - Gỡ ban user
/listban - DS user bị ban
/userinfo [id] - Xem thông tin user
/addbalance [id] [số tiền] - Thêm tiền user
/subbalance [id] [số tiền] - Trừ tiền user

💰 QUẢN LÝ TÀI CHÍNH:
/nap - Xem đơn nạp tiền
/rut - Xem đơn rút tiền
/approve [mã đơn] - Duyệt đơn nạp
/reject [mã đơn] - Từ chối đơn nạp
/approve_wdr [mã đơn] - Duyệt đơn rút
/reject_wdr [mã đơn] - Từ chối đơn rút
/thongke - Thống kê giao dịch

🔑 QUẢN LÝ KEY:
/taokey [ngày] [lần] - Tạo key VIP
/listkey - Xem danh sách key
/delkey [key] - Xóa key
/keyinfo [key] - Xem thông tin key

⚙️ HỆ THỐNG:
/model [dao/bth] - Bật/tắt chế độ đảo
/backup - Sao lưu dữ liệu
/maintenance [on/off] - Bật/tắt bảo trì
/broadcast [nội dung] - Gửi thông báo
/setctv [id] [quyền] - Thêm CTV
/delctv [id] - Xóa CTV
/listctv - Danh sách CTV

📊 THỐNG KÊ:
/stats - Thống kê tổng quan
/userstats - Thống kê user
/vipstats - Thống kê VIP
/profitstats - Thống kê lợi nhuận
"""

    bot.send_message(message.chat.id, admin_commands, reply_markup=EnhancedUserInterface.create_admin_menu())

@bot.message_handler(commands=['taocode'])
def handle_taocode(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if not can_user_perform(message.from_user.id, "taocode"):
        bot.send_message(message.chat.id, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return
    
    parts = message.text.split()
    if len(parts) < 4:
        bot.send_message(message.chat.id, "📌 Sử dụng: /taocode [mã] [số_ngày] [số_lần_nhập]")
        return
    
    code_name = parts[1].upper()
    days = int(parts[2])
    max_uses = int(parts[3])
    
    create_premium_code(code_name, days, max_uses, message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"✅ Tạo code thành công:\n"
        f"🔑 Code: <code>{code_name}</code>\n"
        f"⏱ Thời hạn: {days} ngày\n"
        f"🔢 Số lần nhập: {max_uses}",
        parse_mode="HTML"
    )

@bot.message_handler(commands=['listcode'])
def handle_listcode(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if not can_user_perform(message.from_user.id, "listcode"):
        bot.send_message(message.chat.id, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return
    
    if not codes_db:
        bot.send_message(message.chat.id, "📭 Không có code nào!")
        return
    
    response = "📋 DANH SÁCH CODE:\n\n"
    for code, details in codes_db.items():
        response += (
            f"🔑 Code: <code>{code}</code>\n"
            f"⏱ Thời hạn: {details['days']} ngày\n"
            f"🔢 Đã dùng: {details['used_count']}/{details['max_uses']}\n"
            f"📅 Ngày tạo: {details['created_at']}\n"
            f"👤 Người tạo: {details.get('creator', 'System')}\n\n"
        )
    
    bot.send_message(message.chat.id, response, parse_mode="HTML")

@bot.message_handler(commands=['setctv'])
def handle_setctv(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return
    
    parts = message.text.split()
    if len(parts) < 3:
        bot.send_message(message.chat.id, "📌 Sử dụng: /setctv [id] [stt]")
        return
    
    user_id = parts[1]
    permission_number = parts[2]
    
    # Map permission numbers to actual permissions
    permission_map = {
        "1": "taocode",
        "2": "listcode",
        "3": "delcode",
        "10": "taokey",
        "11": "listkey",
        "12": "delkey"
    }
    
    if permission_number not in permission_map:
        bot.send_message(message.chat.id, "❌ Số quyền không hợp lệ!")
        return
    
    permission = permission_map[permission_number]
    add_staff(user_id, [permission], message.from_user.id)
    
    bot.send_message(
        message.chat.id,
        f"✅ Đã thêm CTV {user_id} với quyền: {permission}"
    )

@bot.message_handler(commands=['autusun'])
def handle_autusun(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    
    user_id = str(message.from_user.id)
    if not is_premium_user(user_id):  # Chỉ USER VIP mới dùng được
        bot.send_message(
            message.chat.id,
            f"{ICONS['error']} Chức năng này chỉ dành cho USER VIP!\n"
            f"{ICONS['vip']} Nâng cấp VIP bằng cách mua key để sử dụng tính năng này."
        )
        return
    
    # Create or get existing SunWinBot instance for this user
    if user_id in sunwin_sessions and sunwin_sessions[user_id].get("running"):
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot Sun Win của bạn đang chạy!")
        return
    
    sunwin_bot = SunWinBot(user_id)
    if sunwin_bot.start(message.chat.id):
        bot.send_message(
            message.chat.id,
            f"{ICONS['success']} Bot Sun Win đã khởi động!\n"
            f"{ICONS['loading']} Đang kết nối với API SunWin...\n"
            f"{ICONS['info']} Sử dụng lệnh /stop để dừng bot."
        )
    else:
        bot.send_message(message.chat.id, f"{ICONS['error']} Không thể khởi động bot!")

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    
    user_id = str(message.from_user.id)
    
    if user_id not in sunwin_sessions or not sunwin_sessions[user_id].get("running"):
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot Sun Win của bạn chưa chạy!")
        return
    
    # Lấy instance thực sự đang chạy từ session
    if 'bot_instance' in sunwin_sessions[user_id]:
        sunwin_bot = sunwin_sessions[user_id]['bot_instance']
    else:
        sunwin_bot = SunWinBot(user_id)
    
    if sunwin_bot.stop():
        # Xóa session sau khi dừng thành công
        if user_id in sunwin_sessions:
            del sunwin_sessions[user_id]
            EnhancedDatabase.save(sunwin_sessions, 'sunwin_sessions')
        
        bot.send_message(message.chat.id, f"{ICONS['success']} Bot Sun Win của bạn đã dừng!")
    else:
        bot.send_message(message.chat.id, f"{ICONS['error']} Không thể dừng bot!")

@bot.message_handler(commands=['sunhistory'])
def handle_sunhistory(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    
    user_id = str(message.from_user.id)
    
    if user_id not in sunwin_sessions or not sunwin_sessions[user_id].get("running"):
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot Sun Win của bạn chưa chạy!")
        return
    
    sunwin_bot = SunWinBot(user_id)
    if not sunwin_bot.history:
        bot.send_message(message.chat.id, f"{ICONS['info']} Chưa có lịch sử dự đoán!")
        return
    
    for entry in sunwin_bot.history[:5]:  # Send last 5 results
        try:
            bot.send_message(message.chat.id, entry.get("message", "Không có dữ liệu"))
            time.sleep(1)
        except Exception as e:
            logger.error(f"Error sending history: {str(e)}")

@bot.message_handler(commands=['sunstatus'])
def handle_sunstatus(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    
    user_id = str(message.from_user.id)
    bot_status = "🟢 Đang chạy" if user_id in sunwin_sessions and sunwin_sessions[user_id].get("running") else "🔴 Đã dừng"
    
    bot.send_message(
        message.chat.id,
        f"{ICONS['stats']} TRẠNG THÁI SUNWIN BOT:\n\n"
        f"🤖 Bot của bạn: {bot_status}\n"
        f"📅 Cập nhật: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}\n\n"
        f"{ICONS['info']} Sử dụng /autusun để bắt đầu"
    )

@bot.message_handler(commands=['send'])
def handle_send(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['error']} Bạn không có quyền sử dụng lệnh này!")
        return
    
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, f"{ICONS['info']} Sử dụng: /send [nội dung]")
        return
    
    content = message.text.split(' ', 1)[1]
    all_users = get_all_users()
    total_users = len(all_users)
    success = 0
    failed = 0
    
    bot.send_message(message.chat.id, f"{ICONS['loading']} Đang gửi tin nhắn đến {total_users} người dùng...")
    
    for user_id in all_users:
        try:
            bot.send_message(user_id, f"{ICONS['broadcast']} THÔNG BÁO TỪ ADMIN:\n\n{content}")
            success += 1
            time.sleep(0.1)  # Delay để tránh bị giới hạn
        except Exception as e:
            logger.error(f"Error sending to {user_id}: {str(e)}")
            failed += 1
    
    message_id = save_broadcast_message(content, message.from_user.id, total_users, success)
    
    bot.send_message(
        message.chat.id,
        f"{ICONS['success']} Gửi tin nhắn hoàn tất!\n"
        f"✅ Thành công: {success}\n"
        f"❌ Thất bại: {failed}\n"
        f"📌 ID tin nhắn: {message_id}"
    )

@bot.message_handler(commands=['ban'])
def handle_ban(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if not can_user_perform(message.from_user.id, "ban_user"):
        bot.send_message(message.chat.id, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return
    
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "📌 Sử dụng: /ban [user_id]")
        return
    
    user_id = message.text.split()[1]
    if ban_user(user_id, message.from_user.id):
        bot.send_message(message.chat.id, f"✅ Đã ban user {user_id}")
    else:
        bot.send_message(message.chat.id, f"❌ User {user_id} đã bị ban trước đó")

@bot.message_handler(commands=['unban'])
def handle_unban(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if not can_user_perform(message.from_user.id, "ban_user"):
        bot.send_message(message.chat.id, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return
    
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "📌 Sử dụng: /unban [user_id]")
        return
    
    user_id = message.text.split()[1]
    if unban_user(user_id, message.from_user.id):
        bot.send_message(message.chat.id, f"✅ Đã gỡ ban user {user_id}")
    else:
        bot.send_message(message.chat.id, f"❌ User {user_id} không bị ban")

@bot.message_handler(commands=['listban'])
def handle_listban(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if not can_user_perform(message.from_user.id, "ban_user"):
        bot.send_message(message.chat.id, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return
    
    if not banned_users:
        bot.send_message(message.chat.id, "📭 Không có user nào bị ban!")
        return
    
    response = "📋 DANH SÁCH USER BỊ BAN:\n\n"
    for user_id in banned_users:
        response += f"🆔 {user_id}\n"
    
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['model'])
def handle_model(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return
    
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "📌 Sử dụng: /model [dao/bth]")
        return
    
    mode = message.text.split()[1].lower()
    global reverse_mode
    
    if mode == "dao":
        reverse_mode = True
        config_db['reverse_mode'] = True
        EnhancedDatabase.save(config_db, 'config')
        bot.send_message(message.chat.id, "✅ Đã bật chế độ đảo kết quả!")
        log_admin_action(message.from_user.id, "set_reverse_mode", {"status": "on"})
    elif mode == "bth":
        reverse_mode = False
        config_db['reverse_mode'] = False
        EnhancedDatabase.save(config_db, 'config')
        bot.send_message(message.chat.id, "✅ Đã tắt chế độ đảo kết quả!")
        log_admin_action(message.from_user.id, "set_reverse_mode", {"status": "off"})
    else:
        bot.send_message(message.chat.id, "❌ Chế độ không hợp lệ. Sử dụng 'dao' hoặc 'bth'")

@bot.message_handler(commands=['backup'])
def handle_backup(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return
    
    # Create backup files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_files = []
    
    for filename in ['users', 'history', 'activity', 'codes', 'referral', 'config', 
                    'keys', 'deposits', 'withdrawals', 'staff', 'sunwin_sessions', 
                    'broadcast_messages', 'banned_users', 'admin_logs', 'user_logs']:
        try:
            with open(f'data/{filename}.json', 'rb') as f:
                backup_files.append(types.InputMediaDocument(f, filename=f"{filename}_{timestamp}.json"))
        except Exception as e:
            logger.error(f"Backup error for {filename}: {str(e)}")
    
    if not backup_files:
        bot.send_message(message.chat.id, "❌ Không thể tạo backup!")
        return
    
    # Split into chunks of 10 files each (Telegram limit)
    for i in range(0, len(backup_files), 10):
        chunk = backup_files[i:i+10]
        bot.send_media_group(message.chat.id, chunk)
    
    bot.send_message(message.chat.id, f"✅ Đã tạo backup thành công vào lúc {timestamp}")
    log_admin_action(message.from_user.id, "backup_data")

@bot.message_handler(commands=['maintenance'])
def handle_maintenance(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ Bạn không có quyền sử dụng lệnh này!")
        return
    
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, "📌 Sử dụng: /maintenance [on/off]")
        return
    
    action = message.text.split()[1].lower()
    if action == "on":
        set_maintenance_mode(True)
        bot.send_message(message.chat.id, "✅ Đã bật chế độ bảo trì!")
        log_admin_action(message.from_user.id, "maintenance_mode", {"status": "on"})
    elif action == "off":
        set_maintenance_mode(False)
        bot.send_message(message.chat.id, "✅ Đã tắt chế độ bảo trì!")
        log_admin_action(message.from_user.id, "maintenance_mode", {"status": "off"})
    else:
        bot.send_message(message.chat.id, "❌ Lệnh không hợp lệ. Sử dụng 'on' hoặc 'off'")

@bot.callback_query_handler(func=lambda call: call.data == "verify_groups")
def handle_verify_groups(call):
    if is_maintenance_mode() and call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Bot đang bảo trì!")
        return
    
    missing_groups = check_group_membership(call.from_user.id)
    if missing_groups:
        bot.answer_callback_query(call.id, "❌ Bạn chưa tham gia đủ các nhóm!")
        
        response_text = f"""
{ICONS['warning']} Vui lòng tham gia các nhóm sau:

{'\n'.join(missing_groups)}

Sau đó nhấn nút xác nhận lại!
"""
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"{ICONS['success']} Xác Nhận Lại", callback_data="verify_groups"))
        
        bot.send_message(call.message.chat.id, response_text, reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "✅ Xác nhận thành công!")
        
        response_text = f"""
{ICONS['gift']} Chúc mừng bạn đã nhận được vé
🎟 PREMIUM7DAY
📝 Để sử dụng bấm vào ngay nút \"✅ Sử Dụng\" bên dưới để sử dụng
"""
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"{ICONS['success']} Sử Dụng", callback_data=f"use_{PREMIUM_CODE}"))
        
        bot.send_message(call.message.chat.id, response_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('use_'))
def handle_use_code(call):
    if is_maintenance_mode() and call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Bot đang bảo trì!")
        return
    
    code_name = call.data.split('_')[1]
    user_id = str(call.from_user.id)
    
    # Xử lý code PREMIUM7DAY đặc biệt
    if code_name == PREMIUM_CODE:
        missing_groups = check_group_membership(call.from_user.id)
        if missing_groups:
            bot.answer_callback_query(call.id, "❌ Bạn chưa tham gia đủ các nhóm!")
            return
            
        # Kích hoạt nhưng KHÔNG đặt premium=True
        exp_date = activate_vip(user_id, 7)
        
        response = (
            f"{ICONS['success']} Kích hoạt thành công 7 ngày!\n"
            f"{ICONS['clock']} Hết hạn: {exp_date}\n"
            f"{ICONS['info']} Trạng thái: Đã kích hoạt (Dùng lệnh /info để kiểm tra)"
        )
        bot.answer_callback_query(call.id, response)
        bot.send_message(call.message.chat.id, response)
        return
    
    # Xử lý các code thông thường
    success, msg = use_premium_code(code_name, user_id)
    bot.answer_callback_query(call.id, msg)
    bot.send_message(call.message.chat.id, msg)
    
    # Xử lý các code thông thường
    success, msg = use_premium_code(code_name, user_id)
    bot.answer_callback_query(call.id, msg)
    bot.send_message(call.message.chat.id, msg)

@bot.message_handler(func=lambda m: re.match(r'^[a-f0-9]{32}$', m.text.strip().lower()))
def handle_md5(message):
    if is_maintenance_mode() and message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, f"{ICONS['warning']} Bot đang bảo trì, vui lòng quay lại sau!")
        return
    
    send_typing(message.chat.id)
    random_reaction(message)
    
    user_id = str(message.from_user.id)
    
    if is_user_banned(user_id):
        bot.send_message(message.chat.id, f"{ICONS['error']} Tài khoản của bạn đã bị khóa!")
        return
    
    if not is_vip_active(user_id) and not is_premium_user(user_id):
        bot.send_message(
            message.chat.id,
            f"{ICONS['error']} Chức năng này yêu cầu VIP hoặc Premium!\n"
            f"{ICONS['vip']} Sử dụng /vip để mua key hoặc /start để nhận code miễn phí"
        )
        return
    
    # Check daily limit
    daily_limit = settings_db.get('limits', {}).get('vip_daily_analyze' if is_premium_user(user_id) else 'daily_analyze', 50)
    today = datetime.now().strftime("%Y-%m-%d")
    
    user_activity = activity.get(user_id, {})
    today_analyze = sum(1 for act in user_activity.get("actions", []) 
                        if act.get("action") == "analyze_md5" 
                        and act.get("timestamp", "").startswith(today))
    
    if today_analyze >= daily_limit:
        bot.send_message(
            message.chat.id,
            f"{ICONS['error']} Bạn đã đạt giới hạn {daily_limit} lần phân tích MD5 hôm nay!\n"
            f"{ICONS['vip']} Nâng cấp VIP để tăng giới hạn hàng ngày."
        )
        return
    
    try:
        md5_hash = message.text.strip().lower()
        analysis = MD5Analyzer.hyper_ai_engine(md5_hash)
        result_msg = EnhancedUserInterface.create_result_message(md5_hash, analysis)
        
        bot.send_message(
            message.chat.id,
            result_msg,
            parse_mode="HTML",
            reply_markup=EnhancedUserInterface.create_feedback_buttons(md5_hash)
        )
        
        save_prediction(message.from_user.id, md5_hash, analysis)
        track_activity(message.from_user.id, "analyze_md5")
        
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"{ICONS['error']} Lỗi phân tích MD5: {str(e)}\n"
            f"{ICONS['info']} Vui lòng kiểm tra lại mã MD5 (32 ký tự hex)"
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith(('correct_', 'wrong_')))
def handle_feedback(call):
    if is_maintenance_mode() and call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Bot đang bảo trì!")
        return
    
    action, md5_hash = call.data.split('_', 1)
    is_correct = action == "correct"
    user_id = str(call.from_user.id)
    
    for entry in history.get(user_id, []):
        if entry["md5"] == md5_hash and entry.get("awaiting_feedback"):
            entry["is_correct"] = is_correct
            entry["awaiting_feedback"] = False
            EnhancedDatabase.save(history, 'history')
            break
    
    bot.answer_callback_query(call.id, "✅ Đã ghi nhận phản hồi!")
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=None
    )
    
    log_user_action(user_id, "feedback_prediction", {
        "md5": md5_hash[:8] + "..." + md5_hash[-8:],
        "is_correct": is_correct
    })

# ==============================================
# ADMIN CALLBACK HANDLERS NÂNG CẤP
# ==============================================
@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def handle_admin_callbacks(call):
    if not can_user_perform(call.from_user.id, "admin"):
        bot.answer_callback_query(call.id, "⛔ Bạn không có quyền!")
        return
    
    action = call.data.split('_', 1)[1]
    
    if action == "add_staff":
        msg = bot.send_message(call.message.chat.id, "📌 Nhập ID user và quyền (vd: 123456789 taocode):")
        bot.register_next_step_handler(msg, process_add_staff)
    elif action == "remove_staff":
        msg = bot.send_message(call.message.chat.id, "📌 Nhập ID user cần xóa khỏi CTV:")
        bot.register_next_step_handler(msg, process_remove_staff)
    elif action == "ban_user":
        msg = bot.send_message(call.message.chat.id, "📌 Nhập ID user cần ban:")
        bot.register_next_step_handler(msg, process_ban_user)
    elif action == "unban_user":
        msg = bot.send_message(call.message.chat.id, "📌 Nhập ID user cần gỡ ban:")
        bot.register_next_step_handler(msg, process_unban_user)
    elif action == "list_staff":
        show_staff_list(call.message)
    elif action == "list_banned":
        show_banned_list(call.message)
    elif action == "create_code":
        msg = bot.send_message(call.message.chat.id, "📌 Nhập thông tin code (vd: CODE1DAY 1 10):")
        bot.register_next_step_handler(msg, process_create_code)
    elif action == "create_key":
        msg = bot.send_message(call.message.chat.id, "📌 Nhập thông tin key (vd: 7 10):")
        bot.register_next_step_handler(msg, process_create_key)
    elif action == "list_codes":
        show_code_list(call.message)
    elif action == "list_keys":
        show_key_list(call.message)
    elif action == "delete_code":
        msg = bot.send_message(call.message.chat.id, "📌 Nhập code cần xóa:")
        bot.register_next_step_handler(msg, process_delete_code)
    elif action == "delete_key":
        msg = bot.send_message(call.message.chat.id, "📌 Nhập key cần xóa:")
        bot.register_next_step_handler(msg, process_delete_key)
    elif action == "add_balance":
        msg = bot.send_message(call.message.chat.id, "📌 Nhập ID user và số tiền (vd: 123456789 100000):")
        bot.register_next_step_handler(msg, process_add_balance)
    elif action == "subtract_balance":
        msg = bot.send_message(call.message.chat.id, "📌 Nhập ID user và số tiền (vd: 123456789 100000):")
        bot.register_next_step_handler(msg, process_subtract_balance)
    elif action == "list_deposits":
        show_deposit_list(call.message)
    elif action == "list_withdrawals":
        show_withdrawal_list(call.message)
    elif action == "deposit_stats":
        show_deposit_stats(call.message)
    elif action == "withdrawal_stats":
        show_withdrawal_stats(call.message)
    elif action == "set_reverse_on":
        global reverse_mode
        reverse_mode = True
        config_db['reverse_mode'] = True
        EnhancedDatabase.save(config_db, 'config')
        bot.answer_callback_query(call.id, "✅ Đã bật chế độ đảo!")
        log_admin_action(call.from_user.id, "set_reverse_mode", {"status": "on"})
    elif action == "set_reverse_off":
        reverse_mode = False
        config_db['reverse_mode'] = False
        EnhancedDatabase.save(config_db, 'config')
        bot.answer_callback_query(call.id, "✅ Đã tắt chế độ đảo!")
        log_admin_action(call.from_user.id, "set_reverse_mode", {"status": "off"})
    elif action == "backup_data":
        handle_backup(call.message)
    elif action == "system_stats":
        show_system_stats(call.message)
    elif action == "user_stats":
        show_user_stats(call.message)
    elif action == "prediction_stats":
        show_prediction_stats(call.message)
    elif action == "transaction_stats":
        show_transaction_stats(call.message)
    elif action == "vip_stats":
        show_vip_stats(call.message)
    elif action == "profit_stats":
        show_profit_stats(call.message)
    elif action == "activity_stats":
        show_activity_stats(call.message)
    elif action == "security":
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=EnhancedUserInterface.create_security_menu()
        )
    elif action == "maintenance":
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=EnhancedUserInterface.create_maintenance_menu()
        )
    elif action == "maintenance_on":
        set_maintenance_mode(True)
        bot.answer_callback_query(call.id, "✅ Đã bật chế độ bảo trì!")
        log_admin_action(call.from_user.id, "maintenance_mode", {"status": "on"})
    elif action == "maintenance_off":
        set_maintenance_mode(False)
        bot.answer_callback_query(call.id, "✅ Đã tắt chế độ bảo trì!")
        log_admin_action(call.from_user.id, "maintenance_mode", {"status": "off"})
    elif action == "auth":
        require_admin_auth(call.from_user.id)
        msg = bot.send_message(call.message.chat.id, f"{ICONS['security']} Vui lòng nhập mã xác thực admin:")
        bot.register_next_step_handler(msg, process_admin_auth)
    elif action == "change_password":
        msg = bot.send_message(call.message.chat.id, f"{ICONS['security']} Vui lòng nhập mật khẩu mới:")
        bot.register_next_step_handler(msg, process_change_password)
    elif action == "view_auth_logs":
        show_auth_logs(call.message)
    elif action == "blocked_ips":
        show_blocked_ips(call.message)
    elif action == "back":
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None
        )
        bot.send_message(
            call.message.chat.id,
            "🔙 Đã quay lại menu chính",
            reply_markup=EnhancedUserInterface.create_admin_menu()
        )

def process_add_staff(message):
    try:
        parts = message.text.split()
        user_id = parts[0]
        permission = parts[1]
        
        add_staff(user_id, [permission], message.from_user.id)
        bot.send_message(
            message.chat.id,
            f"✅ Đã thêm CTV {user_id} với quyền: {permission}"
        )
    except:
        bot.send_message(message.chat.id, "❌ Định dạng không hợp lệ!")

def process_remove_staff(message):
    user_id = message.text.strip()
    if remove_staff(user_id, message.from_user.id):
        bot.send_message(message.chat.id, f"✅ Đã xóa CTV {user_id}")
    else:
        bot.send_message(message.chat.id, f"❌ User {user_id} không phải là CTV")

def process_ban_user(message):
    user_id = message.text.strip()
    if ban_user(user_id, message.from_user.id):
        bot.send_message(message.chat.id, f"✅ Đã ban user {user_id}")
    else:
        bot.send_message(message.chat.id, f"❌ User {user_id} đã bị ban trước đó")

def process_unban_user(message):
    user_id = message.text.strip()
    if unban_user(user_id, message.from_user.id):
        bot.send_message(message.chat.id, f"✅ Đã gỡ ban user {user_id}")
    else:
        bot.send_message(message.chat.id, f"❌ User {user_id} không bị ban")

def show_staff_list(message):
    if not staff_db:
        bot.send_message(message.chat.id, "📭 Không có CTV nào!")
        return
    
    response = "📋 DANH SÁCH CTV:\n\n"
    for user_id, data in staff_db.items():
        response += f"🆔 {user_id}\n"
        response += f"🔑 Quyền: {', '.join(data['permissions'])}\n"
        response += f"📅 Ngày thêm: {data['added_at']}\n"
        response += f"👤 Người thêm: {data.get('added_by', 'System')}\n\n"
    
    bot.send_message(message.chat.id, response)

def show_banned_list(message):
    if not banned_users:
        bot.send_message(message.chat.id, "📭 Không có user nào bị ban!")
        return
    
    response = "📋 DANH SÁCH USER BỊ BAN:\n\n"
    for user_id in banned_users:
        response += f"🆔 {user_id}\n"
    
    bot.send_message(message.chat.id, response)

def process_create_code(message):
    try:
        parts = message.text.split()
        code_name = parts[0].upper()
        days = int(parts[1])
        max_uses = int(parts[2])
        
        create_premium_code(code_name, days, max_uses, message.from_user.id)
        bot.send_message(
            message.chat.id,
            f"✅ Tạo code thành công:\n"
            f"🔑 Code: <code>{code_name}</code>\n"
            f"⏱ Thời hạn: {days} ngày\n"
            f"🔢 Số lần nhập: {max_uses}",
            parse_mode="HTML"
        )
    except:
        bot.send_message(message.chat.id, "❌ Định dạng không hợp lệ!")

def process_create_key(message):
    try:
        parts = message.text.split()
        days = int(parts[0])
        max_uses = int(parts[1])
        
        key_name = f"VIP{days}DAY_{generate_random_string()}"
        create_vip_key(key_name, days, max_uses, message.from_user.id)
        
        bot.send_message(
            message.chat.id,
            f"✅ Tạo key VIP thành công:\n"
            f"🔑 Key: <code>{key_name}</code>\n"
            f"⏱ Thời hạn: {days} ngày\n"
            f"🔢 Số lần nhập: {max_uses}\n"
            f"💰 Giá trị: {get_key_price(days):,} VNĐ",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Lỗi khi tạo key: {str(e)}")

def show_code_list(message):
    if not codes_db:
        bot.send_message(message.chat.id, "📭 Không có code nào!")
        return
    
    response = "📋 DANH SÁCH CODE:\n\n"
    for code, details in codes_db.items():
        response += (
            f"🔑 Code: <code>{code}</code>\n"
            f"⏱ Thời hạn: {details['days']} ngày\n"
            f"🔢 Đã dùng: {details['used_count']}/{details['max_uses']}\n"
            f"📅 Ngày tạo: {details['created_at']}\n"
            f"👤 Người tạo: {details.get('creator', 'System')}\n\n"
        )
    
    bot.send_message(message.chat.id, response, parse_mode="HTML")

def show_key_list(message):
    if not keys_db:
        bot.send_message(message.chat.id, "📭 Không có key nào!")
        return
    
    response = "📋 DANH SÁCH KEY VIP:\n\n"
    for key, details in keys_db.items():
        response += (
            f"🔑 Key: <code>{key}</code>\n"
            f"⏱ Thời hạn: {details['days']} ngày\n"
            f"💰 Giá: {details['price']:,} VNĐ\n"
            f"🔢 Đã dùng: {details['used_count']}/{details['max_uses']}\n"
            f"📅 Ngày tạo: {details['created_at']}\n"
            f"👤 Người tạo: {details.get('creator', 'System')}\n\n"
        )
    
    bot.send_message(message.chat.id, response, parse_mode="HTML")

def process_delete_code(message):
    code_name = message.text.strip().upper()
    if code_name in codes_db:
        del codes_db[code_name]
        EnhancedDatabase.save(codes_db, 'codes')
        bot.send_message(message.chat.id, f"✅ Đã xóa code {code_name}")
    else:
        bot.send_message(message.chat.id, f"❌ Không tìm thấy code {code_name}")

def process_delete_key(message):
    key_name = message.text.strip().upper()
    if key_name in keys_db:
        del keys_db[key_name]
        EnhancedDatabase.save(keys_db, 'keys')
        bot.send_message(message.chat.id, f"✅ Đã xóa key {key_name}")
    else:
        bot.send_message(message.chat.id, f"❌ Không tìm thấy key {key_name}")

def process_add_balance(message):
    try:
        parts = message.text.split()
        user_id = parts[0]
        amount = int(parts[1])
        
        users[user_id] = users.get(user_id, {})
        users[user_id]["balance"] = users[user_id].get("balance", 0) + amount
        EnhancedDatabase.save(users, 'users')
        
        bot.send_message(
            message.chat.id,
            f"✅ Đã thêm {amount:,} VNĐ vào tài khoản {user_id}\n"
            f"💰 Số dư mới: {users[user_id]['balance']:,} VNĐ"
        )
        
        try:
            bot.send_message(
                user_id,
                f"✨ Admin đã thêm {amount:,} VNĐ vào tài khoản của bạn\n"
                f"💰 Số dư mới: {users[user_id]['balance']:,} VNĐ"
            )
        except:
            pass
            
        log_admin_action(message.from_user.id, "add_balance", {
            "user_id": user_id,
            "amount": amount
        })
    except:
        bot.send_message(message.chat.id, "❌ Định dạng không hợp lệ!")

def process_subtract_balance(message):
    try:
        parts = message.text.split()
        user_id = parts[0]
        amount = int(parts[1])
        
        if users.get(user_id, {}).get("balance", 0) < amount:
            bot.send_message(message.chat.id, f"❌ Số dư không đủ để trừ!")
            return
            
        users[user_id]["balance"] = users[user_id].get("balance", 0) - amount
        EnhancedDatabase.save(users, 'users')
        
        bot.send_message(
            message.chat.id,
            f"✅ Đã trừ {amount:,} VNĐ từ tài khoản {user_id}\n"
            f"💰 Số dư mới: {users[user_id]['balance']:,} VNĐ"
        )
        
        try:
            bot.send_message(
                user_id,
                f"⚠️ Admin đã trừ {amount:,} VNĐ từ tài khoản của bạn\n"
                f"💰 Số dư mới: {users[user_id]['balance']:,} VNĐ"
            )
        except:
            pass
            
        log_admin_action(message.from_user.id, "subtract_balance", {
            "user_id": user_id,
            "amount": amount
        })
    except:
        bot.send_message(message.chat.id, "❌ Định dạng không hợp lệ!")

def show_deposit_list(message):
    if not deposits_db:
        bot.send_message(message.chat.id, "📭 Không có đơn nạp tiền nào!")
        return
    
    pending = [d for d in deposits_db.values() if d["status"] == "pending"]
    approved = [d for d in deposits_db.values() if d["status"] == "approved"]
    rejected = [d for d in deposits_db.values() if d["status"] == "rejected"]
    
    response = "📋 DANH SÁCH ĐƠN NẠP TIỀN:\n\n"
    response += f"⏳ Chờ duyệt: {len(pending)}\n"
    response += f"✅ Đã duyệt: {len(approved)}\n"
    response += f"❌ Từ chối: {len(rejected)}\n\n"
    
    if pending:
        response += "🔴 ĐƠN CHỜ DUYỆT:\n"
        for dep in pending[:5]:  # Hiển thị tối đa 5 đơn
            response += (
                f"🆔 User: {dep['user_id']}\n"
                f"💰 Số tiền: {dep['amount']:,} VNĐ\n"
                f"📅 Thời gian: {dep['created_at']}\n"
                f"🔢 Mã đơn: {dep['deposit_id']}\n\n"
            )
    
    bot.send_message(message.chat.id, response)

def show_withdrawal_list(message):
    if not withdrawals_db:
        bot.send_message(message.chat.id, "📭 Không có đơn rút tiền nào!")
        return
    
    pending = [w for w in withdrawals_db.values() if w["status"] == "pending"]
    approved = [w for w in withdrawals_db.values() if w["status"] == "approved"]
    rejected = [w for w in withdrawals_db.values() if w["status"] == "rejected"]
    
    response = "📋 DANH SÁCH ĐƠN RÚT TIỀN:\n\n"
    response += f"⏳ Chờ duyệt: {len(pending)}\n"
    response += f"✅ Đã duyệt: {len(approved)}\n"
    response += f"❌ Từ chối: {len(rejected)}\n\n"
    
    if pending:
        response += "🔴 ĐƠN CHỜ DUYỆT:\n"
        for wdr in pending[:5]:  # Hiển thị tối đa 5 đơn
            response += (
                f"🆔 User: {wdr['user_id']}\n"
                f"💰 Số tiền: {wdr['amount']:,} VNĐ\n"
                f"💳 Thông tin: {wdr['account_info']}\n"
                f"📅 Thời gian: {wdr['created_at']}\n"
                f"🔢 Mã đơn: {wdr['withdrawal_id']}\n\n"
            )
    
    bot.send_message(message.chat.id, response)

def show_deposit_stats(message):
    stats = get_deposit_stats()
    response = (
        f"📊 THỐNG KÊ NẠP TIỀN:\n\n"
        f"📌 Tổng đơn: {stats['total']}\n"
        f"⏳ Chờ duyệt: {stats['pending']}\n"
        f"✅ Đã duyệt: {stats['approved']}\n"
        f"❌ Từ chối: {stats['rejected']}\n"
        f"💰 Tổng tiền: {stats['total_amount']:,} VNĐ"
    )
    bot.send_message(message.chat.id, response)

def show_withdrawal_stats(message):
    stats = get_withdrawal_stats()
    response = (
        f"📊 THỐNG KÊ RÚT TIỀN:\n\n"
        f"📌 Tổng đơn: {stats['total']}\n"
        f"⏳ Chờ duyệt: {stats['pending']}\n"
        f"✅ Đã duyệt: {stats['approved']}\n"
        f"❌ Từ chối: {stats['rejected']}\n"
        f"💰 Tổng tiền: {stats['total_amount']:,} VNĐ"
    )
    bot.send_message(message.chat.id, response)

def show_system_stats(message):
    stats = get_system_stats()
    response = (
        f"📊 THỐNG KÊ HỆ THỐNG:\n\n"
        f"👤 Tổng user: {stats['total_users']}\n"
        f"💎 VIP users: {stats['vip_users']}\n"
        f"👑 Premium users: {stats['premium_users']}\n"
        f"🔄 Active users (7 ngày): {stats['active_users']}\n"
        f"📥 Tổng đơn nạp: {stats['total_deposits']}\n"
        f"📤 Tổng đơn rút: {stats['total_withdrawals']}\n"
        f"🔑 Tổng code: {stats['total_codes']}\n"
        f"🔑 Tổng key: {stats['total_keys']}\n"
        f"🤖 Bot SunWin đang chạy: {stats['running_sunwin_bots']}"
    )
    bot.send_message(message.chat.id, response)

def show_user_stats(message):
    stats = get_global_stats()
    response = (
        f"📊 THỐNG KÊ USER:\n\n"
        f"📌 Tổng dự đoán: {stats['total']}\n"
        f"✅ Đúng: {stats['correct']}\n"
        f"❌ Sai: {stats['wrong']}\n"
        f"🎯 Tỉ lệ chính xác: {stats['accuracy']:.1f}%"
    )
    bot.send_message(message.chat.id, response)

def show_prediction_stats(message):
    vip_stats = get_vip_stats()
    response = (
        f"📊 THỐNG KÊ VIP:\n\n"
        f"1 ngày: {vip_stats.get('1_day', 0)}\n"
        f"7 ngày: {vip_stats.get('1_week', 0)}\n"
        f"1 tháng: {vip_stats.get('1_month', 0)}\n"
        f"3 tháng: {vip_stats.get('3_months', 0)}\n"
        f"6 tháng: {vip_stats.get('6_months', 0)}\n"
        f"1 năm: {vip_stats.get('1_year', 0)}"
    )
    bot.send_message(message.chat.id, response)

def show_transaction_stats(message):
    profit_stats = get_profit_stats()
    response = (
        f"📊 THỐNG KÊ GIAO DỊCH:\n\n"
        f"💰 Tổng nạp: {profit_stats['total_deposits']:,} VNĐ\n"
        f"💸 Tổng rút: {profit_stats['total_withdrawals']:,} VNĐ\n"
        f"📈 Lợi nhuận: {profit_stats['profit']:,} VNĐ\n"
        f"📊 Tỉ lệ lợi nhuận: {profit_stats['profit_percentage']:.1f}%"
    )
    bot.send_message(message.chat.id, response)

def show_vip_stats(message):
    vip_stats = get_vip_stats()
    response = (
        f"📊 THỐNG KÊ VIP:\n\n"
        f"1 ngày: {vip_stats.get('1_day', 0)}\n"
        f"7 ngày: {vip_stats.get('1_week', 0)}\n"
        f"1 tháng: {vip_stats.get('1_month', 0)}\n"
        f"3 tháng: {vip_stats.get('3_months', 0)}\n"
        f"6 tháng: {vip_stats.get('6_months', 0)}\n"
        f"1 năm: {vip_stats.get('1_year', 0)}"
    )
    bot.send_message(message.chat.id, response)

def show_profit_stats(message):
    profit_stats = get_profit_stats()
    response = (
        f"📊 THỐNG KÊ LỢI NHUẬN:\n\n"
        f"💰 Tổng nạp: {profit_stats['total_deposits']:,} VNĐ\n"
        f"💸 Tổng rút: {profit_stats['total_withdrawals']:,} VNĐ\n"
        f"📈 Lợi nhuận: {profit_stats['profit']:,} VNĐ\n"
        f"📊 Tỉ lệ lợi nhuận: {profit_stats['profit_percentage']:.1f}%"
    )
    bot.send_message(message.chat.id, response)

def show_activity_stats(message):
    stats = get_activity_stats()
    response = (
        f"📊 THỐNG KÊ HOẠT ĐỘNG (7 NGÀY):\n\n"
        f"👤 User hoạt động: {stats['active_users']}\n"
        f"🎯 Dự đoán: {stats['predictions']}\n"
        f"📥 Nạp tiền: {stats['deposits']}\n"
        f"📤 Rút tiền: {stats['withdrawals']}\n"
        f"💎 Kích hoạt VIP: {stats['vip_activations']}"
    )
    bot.send_message(message.chat.id, response)

def show_auth_logs(message):
    if not admin_logs:
        bot.send_message(message.chat.id, "📭 Không có log đăng nhập nào!")
        return
    
    response = "📋 LỊCH SỬ ĐĂNG NHẬP ADMIN:\n\n"
    for log in admin_logs[-10:]:  # Hiển thị 10 log gần nhất
        response += (
            f"⏰ {log['timestamp']}\n"
            f"🆔 {log['user_id']}\n"
            f"📌 {log['action']}\n"
            f"📝 {log.get('details', '')}\n\n"
        )
    
    bot.send_message(message.chat.id, response)

def show_blocked_ips(message):
    blocked = security_db.get('blocked_ips', {})
    if not blocked:
        bot.send_message(message.chat.id, "📭 Không có IP nào bị chặn!")
        return
    
    response = "📋 DANH SÁCH IP BỊ CHẶN:\n\n"
    for ip, info in blocked.items():
        response += (
            f"🔒 IP: {ip}\n"
            f"⏰ Thời gian: {info.get('timestamp', 'N/A')}\n"
            f"📌 Lý do: {info.get('reason', 'N/A')}\n\n"
        )
    
    bot.send_message(message.chat.id, response)

def process_change_password(message):
    new_password = message.text.strip()
    global ADMIN_SECRET_KEY
    ADMIN_SECRET_KEY = new_password
    bot.send_message(message.chat.id, "✅ Đã đổi mật khẩu admin thành công!")
    log_admin_action(message.from_user.id, "change_password")

# ==============================================
# KHỞI CHẠY BOT
# ==============================================
if __name__ == '__main__':
    logger.info("Starting bot...")
    try:
        # Tạo thư mục data nếu chưa có
        os.makedirs('data', exist_ok=True)
        os.makedirs('backups', exist_ok=True)
        
        # Lên lịch backup hàng ngày
        def daily_backup():
            while True:
                now = datetime.now()
                if now.hour == 0 and now.minute == 0:
                    try:
                        EnhancedDatabase.backup()
                        logger.info("Daily backup completed")
                    except Exception as e:
                        logger.error(f"Backup error: {str(e)}")
                time.sleep(60)
        
        backup_thread = threading.Thread(target=daily_backup)
        backup_thread.daemon = True
        backup_thread.start()
        
        while True:
            try:
                bot.infinity_polling()
            except Exception as e:
                logger.error(f"Bot crashed: {str(e)}")
                logger.info("Restarting bot in 60 seconds...")
                time.sleep(60)
                
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")