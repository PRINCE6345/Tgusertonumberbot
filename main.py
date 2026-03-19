import os
import json
import requests
from datetime import date
from flask import Flask, request

# ╔══════════════════════════════════════════════╗
# ║     🔥 PRINCE X BOT - OSINT SYSTEM 🔥       ║
# ║         Made by PRINCE | @Ownerofworld45     ║
# ╚══════════════════════════════════════════════╝

BOT_TOKEN   = '8622715627:AAEOQnOF07_c7T3oW5ZOvbDs4CVUu_UbIrE'
CHANNEL     = '@princexhitmanmods'
CHANNEL_URL = 'https://t.me/princexhitmanmods'
SEARCH_API  = 'https://api-test-vip-835d081a6316.herokuapp.com/api/search'
API_KEY     = '98577049'
ADMIN_ID    = '6021592483'
TG_API      = f'https://api.telegram.org/bot{BOT_TOKEN}'

DB_FILE     = 'users_db.json'
CODES_FILE  = 'promo_codes.json'

app = Flask(__name__)

# ─── Database ─────────────────────────────────────────────
def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=2)

def get_user(db, uid, name=''):
    uid = str(uid)
    if uid not in db:
        db[uid] = {
            'name': name,
            'points': 5,
            'last_daily': '',
            'referred_by': None,
            'referrals': [],
            'searches': 0,
            'awaiting': None
        }
    return db[uid]

def load_codes():
    if not os.path.exists(CODES_FILE):
        return {}
    with open(CODES_FILE, 'r') as f:
        return json.load(f)

def save_codes(codes):
    with open(CODES_FILE, 'w') as f:
        json.dump(codes, f, indent=2)

# ─── Telegram API ─────────────────────────────────────────
def tg(method, data):
    try:
        r = requests.post(f'{TG_API}/{method}', json=data, timeout=20)
        return r.json()
    except:
        return {}

def send(cid, text, kb=None):
    d = {
        'chat_id': cid,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    if kb:
        d['reply_markup'] = {'inline_keyboard': kb}
    return tg('sendMessage', d)

def typing(cid):
    tg('sendChatAction', {'chat_id': cid, 'action': 'typing'})

def is_member(uid):
    return True
# ─── Keyboards ────────────────────────────────────────────
def main_kb():
    return [
        [
            {'text': '🔍 How to Search', 'callback_data': 'how_search'},
            {'text': '👤 My Profile',    'callback_data': 'profile'}
        ],
        [
            {'text': '🎁 Daily Bonus',   'callback_data': 'daily'},
            {'text': '🔗 Refer & Earn',  'callback_data': 'refer'}
        ],
        [
            {'text': '🎟️ Promo Code',    'callback_data': 'redeem'},
            {'text': '📢 Our Channel',   'url': CHANNEL_URL}
        ]
    ]

def menu_kb():
    return [[{'text': '🏠 Main Menu', 'callback_data': 'menu'}]]

# ─── Messages ─────────────────────────────────────────────
def not_joined_msg():
    return """
🚫━━━━━━━━━━━━━━━━━━━━🚫
      ⛔ <b>ACCESS DENIED</b> ⛔
🚫━━━━━━━━━━━━━━━━━━━━🚫

🔐 To use this bot, you must
📢 join our <b>Official Channel</b> first!

🎁 After joining you will get:
🔓 Full OSINT Access
💎 <b>5 Free Starting Points</b>
🎯 Daily Bonus System
🔗 Referral Earning System

<i>After joining, tap the ✅ button below</i>
"""

def welcome_msg(name, points):
    return f"""
🌟━━━━━━━━━━━━━━━━━━━━🌟
      ⚡ <b>PRINCE X BOT</b> ⚡
🌟━━━━━━━━━━━━━━━━━━━━🌟

👋 <b>Welcome, {name}!</b>

🔍 <b>Telegram ID → Phone Number</b>
💎 <b>Your Points:</b> {points}

━━━━━━━━━━━━━━━━━━━━━━━
📲 <b>Send any Telegram User ID</b>
    and get their phone number!
━━━━━━━━━━━━━━━━━━━━━━━

🔴 1 Search  =  1 Point
🟢 Daily Bonus  =  +2 Points
🔵 Refer Friend  =  +5 Points
"""

def result_msg(data, search_id, pts_left):
    if not isinstance(data, dict):
        raw = str(data)
        return f"""
🔴━━━━━━━━━━━━━━━━━━━━🔴
      🔍 <b>SEARCH RESULT</b>
🔴━━━━━━━━━━━━━━━━━━━━🔴

🆔 <b>Searched ID:</b>
   <code>{search_id}</code>

📋 <b>Data Found:</b>
<code>{raw}</code>

🟡━━━━━━━━━━━━━━━━━━━━🟡
💎 <b>Points Left: {pts_left}</b>
📢 <b>Join Channel:</b> {CHANNEL_URL}
🤖 <b>Made by PRINCE</b>
🟡━━━━━━━━━━━━━━━━━━━━🟡
"""

    number   = data.get('phone') or data.get('number') or data.get('mobile') or '❓ N/A'
    uname    = data.get('username', '')
    fname    = data.get('first_name') or data.get('name') or '❓'
    lname    = data.get('last_name', '')
    fullname = f"{fname} {lname}".strip() or '❓'
    bio      = data.get('bio') or data.get('about') or '—'
    premium  = '⭐ Yes' if data.get('premium') else '❌ No'
    country  = data.get('country') or data.get('region') or '—'
    uname_str = f"@{uname}" if uname else '❓'

    return f"""
🔴━━━━━━━━━━━━━━━━━━━━🔴
      🔍 <b>SEARCH RESULT</b>
🔴━━━━━━━━━━━━━━━━━━━━🔴

🆔 <b>Telegram ID:</b>
   <code>{search_id}</code>

📱 <b>Phone Number:</b>
   <code>{number}</code>

👤 <b>Full Name:</b>    {fullname}
🔖 <b>Username:</b>     {uname_str}
🌍 <b>Country:</b>      {country}
📝 <b>Bio:</b>          {bio}
⭐ <b>Premium:</b>      {premium}

🟡━━━━━━━━━━━━━━━━━━━━🟡
💎 <b>Points Left: {pts_left}</b>
📢 <b>Join Channel:</b> {CHANNEL_URL}
🤖 <b>Made by PRINCE</b>
🟡━━━━━━━━━━━━━━━━━━━━🟡
"""

# ─── Handlers ─────────────────────────────────────────────
def handle_callback(cb):
    cid     = cb['message']['chat']['id']
    uid     = str(cb['from']['id'])
    name    = cb['from'].get('first_name', 'User')
    cb_data = cb['data']

    tg('answerCallbackQuery', {'callback_query_id': cb['id']})

    db   = load_db()
    user = get_user(db, uid, name)
    db[uid]['name'] = name

    if cb_data == 'check_join':
        if is_member(uid):
            save_db(db)
            send(cid, f"""
✅━━━━━━━━━━━━━━━━━━━━✅
    🎉 <b>WELCOME {name}!</b> 🎉
✅━━━━━━━━━━━━━━━━━━━━✅

🔓 <b>Bot Unlocked Successfully!</b>
💎 <b>5 Free Points</b> added to your wallet!

Send any Telegram ID to get started! 🔍
""", main_kb())
        else:
            send(cid, "❌ <b>You haven't joined yet!</b>\n\nPlease join the channel first, then tap Check again 👇", [
                [
                    {'text': '📢 Join Channel',  'url': CHANNEL_URL},
                    {'text': '✅ Joined! Check', 'callback_data': 'check_join'}
                ]
            ])

    elif cb_data == 'daily':
        today = str(date.today())
        if db[uid]['last_daily'] == today:
            send(cid, f"""
⏳━━━━━━━━━━━━━━━━━━━━⏳
      <b>DAILY BONUS</b>
⏳━━━━━━━━━━━━━━━━━━━━⏳

✅ <b>Already claimed today!</b>
💎 Current Points: <b>{db[uid]['points']}</b>

Come back tomorrow! ⏰
""", menu_kb())
        else:
            db[uid]['points']     += 2
            db[uid]['last_daily']  = today
            save_db(db)
            send(cid, f"""
🎁━━━━━━━━━━━━━━━━━━━━🎁
   <b>DAILY BONUS CLAIMED!</b> 🎉
🎁━━━━━━━━━━━━━━━━━━━━🎁

🟢 <b>+2 Points Added!</b>
💎 Total Balance: <b>{db[uid]['points']} Points</b>

Come back tomorrow for more! 🔥
""", menu_kb())

    elif cb_data == 'profile':
        u    = db[uid]
        refs = len(u.get('referrals', []))
        pts  = u['points']
        rank = '💎 VIP' if pts >= 100 else ('🥇 Gold' if pts >= 50 else ('🥈 Silver' if pts >= 20 else '🥉 Bronze'))
        send(cid, f"""
🔵━━━━━━━━━━━━━━━━━━━━🔵
      👤 <b>MY PROFILE</b>
🔵━━━━━━━━━━━━━━━━━━━━🔵

🆔 <b>User ID:</b>
   <code>{uid}</code>

👋 <b>Name:</b>       {u['name']}
🏅 <b>Rank:</b>       {rank}
💎 <b>Points:</b>     {pts}
🔍 <b>Searches:</b>   {u['searches']}
👥 <b>Referrals:</b>  {refs}

━━━━━━━━━━━━━━━━━━━━━━━
📢 {CHANNEL_URL}
🤖 <b>Made by PRINCE</b>
""", menu_kb())

    elif cb_data == 'refer':
        r   = tg('getMe', {})
        bun = r.get('result', {}).get('username', 'PrinceXBot')
        link = f"https://t.me/{bun}?start=ref_{uid}"
        send(cid, f"""
🔗━━━━━━━━━━━━━━━━━━━━🔗
      <b>REFER &amp; EARN</b>
🔗━━━━━━━━━━━━━━━━━━━━🔗

🎁 Each Referral = <b>+5 Points</b>

📲 <b>Your Referral Link:</b>
<code>{link}</code>

👆 Copy and share with friends!
More referrals = More earnings! 💰

💎 Current Points: <b>{db[uid]['points']}</b>
""", menu_kb())

    elif cb_data == 'redeem':
        db[uid]['awaiting'] = 'promo'
        save_db(db)
        send(cid, """
🎟️━━━━━━━━━━━━━━━━━━━━🎟️
    <b>REDEEM PROMO CODE</b>
🎟️━━━━━━━━━━━━━━━━━━━━🎟️

✍️ <b>Send your promo code below:</b>
<i>Example: PRINCE50</i>
""", [[{'text': '❌ Cancel', 'callback_data': 'menu'}]])

    elif cb_data == 'how_search':
        send(cid, f"""
🔍━━━━━━━━━━━━━━━━━━━━🔍
      <b>HOW TO SEARCH</b>
🔍━━━━━━━━━━━━━━━━━━━━🔍

📲 <b>Steps:</b>

1️⃣ Get the Telegram User ID
2️⃣ Send that numeric ID here
3️⃣ Get their phone number instantly!

💡 <b>How to find Telegram ID?</b>
   Use @userinfobot or @getidsbot

⚡ <b>Cost: 1 Point per Search</b>
💎 Your Points: <b>{db[uid]['points']}</b>

<b>Send an ID now! 👇</b>
""", menu_kb())

    elif cb_data == 'menu':
        db[uid]['awaiting'] = None
        save_db(db)
        send(cid, welcome_msg(name, db[uid]['points']), main_kb())

    save_db(db)


def handle_message(msg):
    cid  = msg['chat']['id']
    uid  = str(msg['from']['id'])
    name = msg['from'].get('first_name', 'User')
    text = msg.get('text', '').strip()

    db   = load_db()
    user = get_user(db, uid, name)
    db[uid]['name'] = name

    # /start
    if text.startswith('/start'):
        parts = text.split()
        if len(parts) > 1 and parts[1].startswith('ref_'):
            ref_by = parts[1].replace('ref_', '')
            if ref_by != uid and not user.get('referred_by'):
                db[uid]['referred_by'] = ref_by
                get_user(db, ref_by)
                if uid not in db[ref_by].get('referrals', []):
                    db[ref_by]['referrals'].append(uid)
                    db[ref_by]['points'] += 5
                    tg('sendMessage', {
                        'chat_id': ref_by,
                        'text': f"🎉━━━━━━━━━━━━━━━━━━━━🎉\n    <b>NEW REFERRAL!</b>\n🎉━━━━━━━━━━━━━━━━━━━━🎉\n\n👤 <b>{name}</b> just joined!\n🔵 Came through your link!\n🟢 <b>+5 Points</b> added!\n💎 Total: <b>{db[ref_by]['points']}</b>",
                        'parse_mode': 'HTML'
                    })
        save_db(db)

        if not is_member(uid):
            send(cid, not_joined_msg(), [
                [
                    {'text': '📢 Join Channel',  'url': CHANNEL_URL},
                    {'text': '✅ Joined! Check', 'callback_data': 'check_join'}
                ]
            ])
            return

        send(cid, welcome_msg(name, db[uid]['points']), main_kb())
        save_db(db)
        return

    # Channel gate
    if not is_member(uid):
        send(cid, not_joined_msg(), [
            [
                {'text': '📢 Join Channel',  'url': CHANNEL_URL},
                {'text': '✅ Joined! Check', 'callback_data': 'check_join'}
            ]
        ])
        save_db(db)
        return

    # Promo code input
    if db[uid].get('awaiting') == 'promo':
        db[uid]['awaiting'] = None
        codes = load_codes()
        code  = text.upper().strip()

        if code in codes:
            used = codes[code].get('used', [])
            if uid in used:
                send(cid, """
❌━━━━━━━━━━━━━━━━━━━━❌
    <b>ALREADY USED!</b>
❌━━━━━━━━━━━━━━━━━━━━❌

⚠️ You have already used this code!
Try a different promo code.
""", menu_kb())
            else:
                pts = int(codes[code]['points'])
                db[uid]['points'] += pts
                codes[code]['used'].append(uid)
                save_codes(codes)
                send(cid, f"""
✅━━━━━━━━━━━━━━━━━━━━✅
    <b>CODE REDEEMED!</b> 🎉
✅━━━━━━━━━━━━━━━━━━━━✅

🎟️ Code: <code>{code}</code>
🟢 <b>+{pts} Points</b> Added!
💎 Total Balance: <b>{db[uid]['points']} Points</b>
""", menu_kb())
        else:
            send(cid, """
❌━━━━━━━━━━━━━━━━━━━━❌
    <b>INVALID CODE!</b>
❌━━━━━━━━━━━━━━━━━━━━❌

🚫 This promo code does not exist!
Please check and try again.
""", menu_kb())

        save_db(db)
        return

    # Admin commands
    if uid == ADMIN_ID:

        if text.startswith('/addcode '):
            parts = text.split()
            if len(parts) == 3:
                code = parts[1].upper()
                pts  = int(parts[2])
                codes = load_codes()
                codes[code] = {'points': pts, 'used': []}
                save_codes(codes)
                send(cid, f"✅ <b>Code Created!</b>\n🎟️ Code: <code>{code}</code>\n💎 Points: <b>{pts}</b>")
            else:
                send(cid, "Usage: <code>/addcode CODE POINTS</code>\nEx: <code>/addcode PRINCE50 50</code>")
            save_db(db)
            return

        if text.startswith('/delcode '):
            parts = text.split()
            code  = parts[1].upper() if len(parts) > 1 else ''
            codes = load_codes()
            if code in codes:
                del codes[code]
                save_codes(codes)
                send(cid, f"🗑️ Code <code>{code}</code> deleted successfully!")
            else:
                send(cid, "❌ Code not found!")
            save_db(db)
            return

        if text.startswith('/addpoints '):
            parts = text.split()
            if len(parts) == 3:
                tid = parts[1]
                pts = int(parts[2])
                get_user(db, tid)
                db[tid]['points'] += pts
                save_db(db)
                send(cid, f"✅ Added 💎 <b>{pts} Points</b> to user <code>{tid}</code>!")
            return

        if text == '/stats':
            total   = len(db)
            tpoints = sum(u.get('points', 0) for u in db.values())
            tsearch = sum(u.get('searches', 0) for u in db.values())
            send(cid, f"""
📊━━━━━━━━━━━━━━━━━━━━📊
      <b>BOT STATISTICS</b>
📊━━━━━━━━━━━━━━━━━━━━📊

👥 Total Users:     <b>{total}</b>
💎 Total Points:    <b>{tpoints}</b>
🔍 Total Searches:  <b>{tsearch}</b>
""")
            save_db(db)
            return

        if text.startswith('/broadcast '):
            bmsg = text[11:]
            sent = 0
            for bid in db.keys():
                try:
                    r = tg('sendMessage', {
                        'chat_id': bid,
                        'text': f"📢━━━━━━━━━━━━━━━━━━━━📢\n      <b>ANNOUNCEMENT</b>\n📢━━━━━━━━━━━━━━━━━━━━📢\n\n{bmsg}\n\n🤖 <b>Made by PRINCE</b>",
                        'parse_mode': 'HTML'
                    })
                    if r.get('ok'):
                        sent += 1
                except:
                    pass
            send(cid, f"📢 Broadcast complete! Sent to <b>{sent}</b> users.")
            save_db(db)
            return

        if text == '/listcodes':
            codes = load_codes()
            if not codes:
                send(cid, "❌ No active promo codes.")
            else:
                lines = "🎟️ <b>Active Promo Codes:</b>\n\n"
                for c, info in codes.items():
                    used_count = len(info.get('used', []))
                    lines += f"• <code>{c}</code> — 💎 {info['points']} pts | Used: {used_count}x\n"
                send(cid, lines)
            save_db(db)
            return

    # Search
    if text and not text.startswith('/'):
        if not text.isdigit():
            send(cid, """
⚠️━━━━━━━━━━━━━━━━━━━━⚠️
      <b>WRONG FORMAT!</b>
⚠️━━━━━━━━━━━━━━━━━━━━⚠️

📲 Please send a <b>Telegram User ID</b> only!
<i>Example: <code>123456789</code></i>

💡 <b>Don't know the ID?</b>
   Use @userinfobot to find it!
""", [
                [
                    {'text': '🔍 Search Guide', 'callback_data': 'how_search'},
                    {'text': '🏠 Main Menu',    'callback_data': 'menu'}
                ]
            ])
            save_db(db)
            return

        if db[uid]['points'] < 1:
            send(cid, """
💎━━━━━━━━━━━━━━━━━━━━💎
      <b>OUT OF POINTS!</b>
💎━━━━━━━━━━━━━━━━━━━━💎

😔 You need at least 1 point to search!

<b>Earn more points:</b>
🎁 Daily Bonus   →  +2 Points
🔗 Refer Friend  →  +5 Points
🎟️ Promo Code    →  Variable
""", [
                [
                    {'text': '🎁 Daily Bonus',  'callback_data': 'daily'},
                    {'text': '🔗 Refer & Earn', 'callback_data': 'refer'}
                ]
            ])
            save_db(db)
            return

        typing(cid)

        try:
            r      = requests.get(f"{SEARCH_API}?key={API_KEY}&userid={text}", timeout=15)
            status = r.status_code
            res    = r.json() if status == 200 else None
        except:
            status = 0
            res    = None

        db[uid]['points']   -= 1
        db[uid]['searches'] += 1
        pts_left = db[uid]['points']

        if status == 200 and res is not None:
            send(cid, result_msg(res, text, pts_left), [
                [
                    {'text': '🔍 New Search', 'callback_data': 'how_search'},
                    {'text': '🏠 Main Menu',  'callback_data': 'menu'}
                ]
            ])
        else:
            send(cid, f"""
❌━━━━━━━━━━━━━━━━━━━━❌
    <b>NO RESULT FOUND!</b>
❌━━━━━━━━━━━━━━━━━━━━❌

🚫 This ID does not exist or
   the API is temporarily down.

💡 Please try again later!
<i>HTTP Status: {status}</i>
""", [[{'text': '🔍 Try Again', 'callback_data': 'how_search'}]])

        save_db(db)

# ─── Webhook Route ─────────────────────────────────────────
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return 'ok'

    if 'callback_query' in data:
        handle_callback(data['callback_query'])
    elif 'message' in data:
        handle_message(data['message'])

    return 'ok'

@app.route('/')
def index():
    return '🤖 PRINCE X BOT is Running! Made by PRINCE'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
