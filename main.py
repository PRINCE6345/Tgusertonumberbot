import os
import json
import requests
from datetime import date
from flask import Flask, request

# ╔═════════════════════════════════════════════════╗
# ║   💀 TG LOOKUP BOT — ELITE OSINT SYSTEM 💀    ║
# ║       Made by PRINCE | @Ownerofworld45          ║
# ╚═════════════════════════════════════════════════╝

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

# ═══════════════════════════════════════════════════
#   DATABASE
# ═══════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════
#   TELEGRAM API
# ═══════════════════════════════════════════════════
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
    r = tg('getChatMember', {'chat_id': CHANNEL, 'user_id': uid})
    status = r.get('result', {}).get('status', '')
    return status in ['member', 'administrator', 'creator']

# ═══════════════════════════════════════════════════
#   KEYBOARDS
# ═══════════════════════════════════════════════════
def main_kb():
    return [
        [
            {'text': '🎯 𝗧𝗔𝗥𝗚𝗘𝗧', 'switch_inline_query_chosen_chat': {
                'allow_user_chats': True,
                'allow_bot_chats': False,
                'allow_group_chats': False,
                'allow_channel_chats': False
            }},
        ],
        [
            {'text': '🔎 𝗛𝗼𝘄 𝘁𝗼 𝗦𝗲𝗮𝗿𝗰𝗵', 'callback_data': 'how_search'},
            {'text': '👤 𝗣𝗿𝗼𝗳𝗶𝗹𝗲',         'callback_data': 'profile'},
        ],
        [
            {'text': '🎁 𝗗𝗮𝗶𝗹𝘆 𝗕𝗼𝗻𝘂𝘀',    'callback_data': 'daily'},
            {'text': '🔗 𝗥𝗲𝗳𝗲𝗿 & 𝗘𝗮𝗿𝗻',   'callback_data': 'refer'},
        ],
        [
            {'text': '🎟️ 𝗣𝗿𝗼𝗺𝗼 𝗖𝗼𝗱𝗲',     'callback_data': 'redeem'},
            {'text': '📊 𝗦𝘁𝗮𝘁𝘀',            'callback_data': 'botstats'},
        ],
        [
            {'text': '💬 𝗦𝘂𝗽𝗽𝗼𝗿𝘁',          'url': 'https://t.me/Ownerofworld45'},
            {'text': '📢 𝗖𝗵𝗮𝗻𝗻𝗲𝗹',          'url': CHANNEL_URL},
        ],
    ]

def menu_kb():
    return [[{'text': '🏠 « 𝗠𝗮𝗶𝗻 𝗠𝗲𝗻𝘂', 'callback_data': 'menu'}]]

def search_kb():
    return [[
        {'text': '🎯 𝗡𝗲𝘄 𝗧𝗮𝗿𝗴𝗲𝘁', 'switch_inline_query_chosen_chat': {
            'allow_user_chats': True,
            'allow_bot_chats': False,
            'allow_group_chats': False,
            'allow_channel_chats': False
        }},
        {'text': '🏠 𝗠𝗲𝗻𝘂', 'callback_data': 'menu'}
    ]]

# ═══════════════════════════════════════════════════
#   MESSAGES
# ═══════════════════════════════════════════════════
def not_joined_msg():
    return (
        "🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴\n"
        "   ⛔️ <b>𝗔𝗖𝗖𝗘𝗦𝗦 𝗗𝗘𝗡𝗜𝗘𝗗</b> ⛔️\n"
        "🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴\n\n"
        "🔐 <b>Join our channel to unlock\n"
        "this Elite OSINT Bot!</b>\n\n"
        "✨ <b>𝗪𝗵𝗮𝘁 𝘆𝗼𝘂'𝗹𝗹 𝗴𝗲𝘁:</b>\n"
        "┣ 🎯 Target & Lookup Anyone\n"
        "┣ 💎 5 Free Starting Points\n"
        "┣ 🎁 Daily Bonus Rewards\n"
        "┣ 🔗 Referral Earning System\n"
        "┗ 🎟️ Exclusive Promo Codes\n\n"
        "<i>Tap ✅ after joining!</i>"
    )

def welcome_msg(name, points):
    return (
        "⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡\n"
        "  💀 <b>𝗧𝗚 𝗟𝗢𝗢𝗞𝗨𝗣 𝗕𝗢𝗧</b> 💀\n"
        "⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡\n\n"
        f"👋 <b>Hey, {name}!</b>\n\n"
        "🔎 <b>𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗜𝗗 → 𝗣𝗵𝗼𝗻𝗲 𝗡𝘂𝗺𝗯𝗲𝗿</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>Balance:</b>  💎 <b>{points} pts</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📌 <b>𝗛𝗼𝘄 𝗶𝘁 𝘄𝗼𝗿𝗸𝘀:</b>\n"
        "┣ 🎯 Tap Target → Select User → Get Number\n"
        "┣ 🔴 1 Search = 1 Point\n"
        "┣ 🟢 Daily Bonus = +2 Points\n"
        "┗ 🔵 Each Referral = +5 Points\n\n"
        "👇 <b>Tap 🎯 𝗧𝗔𝗥𝗚𝗘𝗧 to begin!</b>"
    )

def result_msg(number, country_code, country, search_id, pts_left):
    full_number = f"{country_code}{number}" if country_code else number
    return (
        "🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢\n"
        "  ✅ <b>𝗗𝗔𝗧𝗔 𝗥𝗘𝗧𝗥𝗜𝗘𝗩𝗘𝗗!</b> ✅\n"
        "🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢\n\n"
        f"🎯 <b>𝗧𝗮𝗿𝗴𝗲𝘁 𝗜𝗗:</b>\n"
        f"┗ <code>{search_id}</code>\n\n"
        f"📱 <b>𝗣𝗵𝗼𝗻𝗲 𝗡𝘂𝗺𝗯𝗲𝗿:</b>\n"
        f"┗ <code>{full_number}</code>\n\n"
        f"🌍 <b>Country:</b>  {country}\n"
        f"🔢 <b>Code:</b>     {country_code}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"💎 <b>Points Left:</b> {pts_left}\n"
        f"📢 {CHANNEL_URL}\n"
        "🤖 <b>𝗠𝗮𝗱𝗲 𝗯𝘆 𝗣𝗥𝗜𝗡𝗖𝗘</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━"
    )

def not_found_msg(search_id, pts_left):
    return (
        "🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴\n"
        "  ❌ <b>𝗡𝗢 𝗗𝗔𝗧𝗔 𝗙𝗢𝗨𝗡𝗗!</b> ❌\n"
        "🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴\n\n"
        f"🎯 <b>Target ID:</b>\n"
        f"┗ <code>{search_id}</code>\n\n"
        "⚠️ No phone number linked\n"
        "to this Telegram account.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"💎 <b>Points Left:</b> {pts_left}\n"
        "━━━━━━━━━━━━━━━━━━━━━"
    )

# ═══════════════════════════════════════════════════
#   SEARCH FUNCTION
# ═══════════════════════════════════════════════════
def do_search(cid, uid, text, db):
    if db[uid]['points'] < 1:
        send(cid,
            "💎💎💎💎💎💎💎💎💎💎\n"
            "   😔 <b>𝗢𝗨𝗧 𝗢𝗙 𝗣𝗢𝗜𝗡𝗧𝗦!</b>\n"
            "💎💎💎💎💎💎💎💎💎💎\n\n"
            "You need at least <b>1 point</b>!\n\n"
            "📌 <b>𝗘𝗮𝗿𝗻 𝗠𝗼𝗿𝗲:</b>\n"
            "┣ 🎁 Daily Bonus  → +2 pts\n"
            "┣ 🔗 Refer Friend → +5 pts\n"
            "┗ 🎟️ Promo Code   → Variable",
            [[
                {'text': '🎁 𝗗𝗮𝗶𝗹𝘆 𝗕𝗼𝗻𝘂𝘀',  'callback_data': 'daily'},
                {'text': '🔗 𝗥𝗲𝗳𝗲𝗿 & 𝗘𝗮𝗿𝗻', 'callback_data': 'refer'}
            ]]
        )
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
    save_db(db)

    if (
        status == 200
        and res
        and res.get('code') == 200
        and res.get('data', {}).get('found') is True
    ):
        data         = res['data']
        number       = data.get('number', 'N/A')
        country_code = data.get('country_code', '')
        country      = data.get('country', '—')
        send(cid, result_msg(number, country_code, country, text, pts_left), search_kb())
    else:
        send(cid, not_found_msg(text, pts_left), search_kb())

# ═══════════════════════════════════════════════════
#   INLINE QUERY HANDLER
# ═══════════════════════════════════════════════════
def handle_inline(inline_query):
    iq_id = inline_query['id']
    uid   = str(inline_query['from']['id'])
    name  = inline_query['from'].get('first_name', 'User')

    results = [{
        'type': 'article',
        'id': '1',
        'title': f'🎯 Lookup: {name}',
        'description': '📱 Tap to retrieve phone number',
        'input_message_content': {
            'message_text': uid
        },
        'reply_markup': {'inline_keyboard': [[
            {'text': '🔎 Searching...', 'callback_data': 'searching'}
        ]]}
    }]

    tg('answerInlineQuery', {
        'inline_query_id': iq_id,
        'results': results,
        'cache_time': 0
    })

# ═══════════════════════════════════════════════════
#   CALLBACK HANDLER
# ═══════════════════════════════════════════════════
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
            send(cid,
                "✅✅✅✅✅✅✅✅✅✅\n"
                f"  🎊 <b>𝗪𝗘𝗟𝗖𝗢𝗠𝗘, {name}!</b> 🎊\n"
                "✅✅✅✅✅✅✅✅✅✅\n\n"
                "🔓 <b>Access Granted!</b>\n"
                "💎 <b>5 Free Points</b> added!\n\n"
                "🎯 Tap <b>TARGET</b> to find anyone!",
                main_kb()
            )
        else:
            send(cid,
                "❌ <b>Not joined yet!</b>\n\n"
                "Please join the channel first,\n"
                "then tap ✅ Check again.",
                [[
                    {'text': '📢 𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹',  'url': CHANNEL_URL},
                    {'text': '✅ 𝗖𝗵𝗲𝗰𝗸 𝗔𝗴𝗮𝗶𝗻',   'callback_data': 'check_join'}
                ]]
            )

    elif cb_data == 'daily':
        today = str(date.today())
        if db[uid]['last_daily'] == today:
            send(cid,
                "⏳⏳⏳⏳⏳⏳⏳⏳⏳⏳\n"
                "    🎁 <b>𝗗𝗔𝗜𝗟𝗬 𝗕𝗢𝗡𝗨𝗦</b>\n"
                "⏳⏳⏳⏳⏳⏳⏳⏳⏳⏳\n\n"
                "✅ <b>Already claimed today!</b>\n\n"
                f"💎 Balance: <b>{db[uid]['points']} pts</b>\n\n"
                "🕐 Come back tomorrow!",
                menu_kb()
            )
        else:
            db[uid]['points']     += 2
            db[uid]['last_daily']  = today
            save_db(db)
            send(cid,
                "🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁\n"
                "  ✨ <b>𝗕𝗢𝗡𝗨𝗦 𝗖𝗟𝗔𝗜𝗠𝗘𝗗!</b> ✨\n"
                "🎁🎁🎁🎁🎁🎁🎁🎁🎁🎁\n\n"
                "🟢 <b>+2 Points</b> added!\n"
                f"💎 New Balance: <b>{db[uid]['points']} pts</b>\n\n"
                "🔥 Come back tomorrow for more!",
                menu_kb()
            )

    elif cb_data == 'profile':
        u    = db[uid]
        refs = len(u.get('referrals', []))
        pts  = u['points']
        rank = '💀 𝗟𝗘𝗚𝗘𝗡𝗗' if pts >= 500 else (
               '👑 𝗩𝗜𝗣'     if pts >= 100 else (
               '🥇 𝗚𝗼𝗹𝗱'    if pts >= 50  else (
               '🥈 𝗦𝗶𝗹𝘃𝗲𝗿'  if pts >= 20  else '🥉 𝗕𝗿𝗼𝗻𝘇𝗲')))
        send(cid,
            "🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵\n"
            "     👤 <b>𝗠𝗬 𝗣𝗥𝗢𝗙𝗜𝗟𝗘</b>\n"
            "🔵🔵🔵🔵🔵🔵🔵🔵🔵🔵\n\n"
            f"🆔 <b>User ID:</b>\n"
            f"┗ <code>{uid}</code>\n\n"
            f"👋 <b>Name:</b>      {u['name']}\n"
            f"🏅 <b>Rank:</b>      {rank}\n"
            f"💎 <b>Balance:</b>   {pts} pts\n"
            f"🔎 <b>Searches:</b>  {u['searches']}\n"
            f"👥 <b>Referrals:</b> {refs}\n\n"
            "🤖 <b>𝗠𝗮𝗱𝗲 𝗯𝘆 𝗣𝗥𝗜𝗡𝗖𝗘</b>",
            menu_kb()
        )

    elif cb_data == 'refer':
        r   = tg('getMe', {})
        bun = r.get('result', {}).get('username', 'HitmanXprinceInfobot')
        link = f"https://t.me/{bun}?start=ref_{uid}"
        send(cid,
            "🔗🔗🔗🔗🔗🔗🔗🔗🔗🔗\n"
            "   💰 <b>𝗥𝗘𝗙𝗘𝗥 & 𝗘𝗔𝗥𝗡</b>\n"
            "🔗🔗🔗🔗🔗🔗🔗🔗🔗🔗\n\n"
            "🎁 Each referral = <b>+5 Points</b>\n\n"
            "📲 <b>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸:</b>\n"
            f"<code>{link}</code>\n\n"
            "👆 Share with friends!\n"
            f"💎 Balance: <b>{db[uid]['points']} pts</b>",
            menu_kb()
        )

    elif cb_data == 'redeem':
        db[uid]['awaiting'] = 'promo'
        save_db(db)
        send(cid,
            "🎟️🎟️🎟️🎟️🎟️🎟️🎟️🎟️🎟️🎟️\n"
            "  💳 <b>𝗥𝗘𝗗𝗘𝗘𝗠 𝗣𝗥𝗢𝗠𝗢 𝗖𝗢𝗗𝗘</b>\n"
            "🎟️🎟️🎟️🎟️🎟️🎟️🎟️🎟️🎟️🎟️\n\n"
            "✍️ Send your promo code:\n"
            "<i>Example: PRINCE50</i>",
            [[{'text': '❌ 𝗖𝗮𝗻𝗰𝗲𝗹', 'callback_data': 'menu'}]]
        )

    elif cb_data == 'how_search':
        send(cid,
            "🔎🔎🔎🔎🔎🔎🔎🔎🔎🔎\n"
            "   📖 <b>𝗛𝗢𝗪 𝗧𝗢 𝗦𝗘𝗔𝗥𝗖𝗛</b>\n"
            "🔎🔎🔎🔎🔎🔎🔎🔎🔎🔎\n\n"
            "📌 <b>𝗠𝗲𝘁𝗵𝗼𝗱 𝟭 — 𝗧𝗮𝗿𝗴𝗲𝘁 𝗕𝘂𝘁𝘁𝗼𝗻:</b>\n"
            "┣ Tap 🎯 Target button\n"
            "┣ Select any user from your list\n"
            "┗ Number appears instantly!\n\n"
            "📌 <b>𝗠𝗲𝘁𝗵𝗼𝗱 𝟮 — 𝗠𝗮𝗻𝘂𝗮𝗹 𝗜𝗗:</b>\n"
            "┣ Get Telegram User ID\n"
            "┣ Send that numeric ID here\n"
            "┗ Get phone number instantly!\n\n"
            "💡 Use @userinfobot to find IDs\n\n"
            f"⚡ Cost: <b>1 Point per search</b>\n"
            f"💎 Balance: <b>{db[uid]['points']} pts</b>",
            menu_kb()
        )

    elif cb_data == 'botstats':
        db2     = load_db()
        total   = len(db2)
        tsearch = sum(u.get('searches', 0) for u in db2.values())
        send(cid,
            "📊📊📊📊📊📊📊📊📊📊\n"
            "   🤖 <b>𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦</b>\n"
            "📊📊📊📊📊📊📊📊📊📊\n\n"
            f"👥 <b>Total Users:</b>    {total}\n"
            f"🔎 <b>Total Searches:</b> {tsearch}\n\n"
            "🤖 <b>𝗠𝗮𝗱𝗲 𝗯𝘆 𝗣𝗥𝗜𝗡𝗖𝗘</b>",
            menu_kb()
        )

    elif cb_data == 'menu':
        db[uid]['awaiting'] = None
        save_db(db)
        send(cid, welcome_msg(name, db[uid]['points']), main_kb())

    save_db(db)

# ═══════════════════════════════════════════════════
#   MESSAGE HANDLER
# ═══════════════════════════════════════════════════
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
                        'text': (
                            "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉\n"
                            "  🔗 <b>𝗡𝗘𝗪 𝗥𝗘𝗙𝗘𝗥𝗥𝗔𝗟!</b>\n"
                            "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉\n\n"
                            f"👤 <b>{name}</b> just joined!\n"
                            f"🟢 <b>+5 Points</b> added!\n"
                            f"💎 Balance: <b>{db[ref_by]['points']} pts</b>"
                        ),
                        'parse_mode': 'HTML'
                    })
        save_db(db)

        if not is_member(uid):
            send(cid, not_joined_msg(), [[
                {'text': '📢 𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹',   'url': CHANNEL_URL},
                {'text': '✅ 𝗝𝗼𝗶𝗻𝗲𝗱! 𝗖𝗵𝗲𝗰𝗸', 'callback_data': 'check_join'}
            ]])
            return

        send(cid, welcome_msg(name, db[uid]['points']), main_kb())
        save_db(db)
        return

    # Channel gate
    if not is_member(uid):
        send(cid, not_joined_msg(), [[
            {'text': '📢 𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹',   'url': CHANNEL_URL},
            {'text': '✅ 𝗝𝗼𝗶𝗻𝗲𝗱! 𝗖𝗵𝗲𝗰𝗸', 'callback_data': 'check_join'}
        ]])
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
                send(cid,
                    "❌❌❌❌❌❌❌❌❌❌\n"
                    "  ⚠️ <b>𝗔𝗟𝗥𝗘𝗔𝗗𝗬 𝗨𝗦𝗘𝗗!</b>\n"
                    "❌❌❌❌❌❌❌❌❌❌\n\n"
                    "You already used this code!\nTry a different one.",
                    menu_kb()
                )
            else:
                pts = int(codes[code]['points'])
                db[uid]['points'] += pts
                codes[code]['used'].append(uid)
                save_codes(codes)
                send(cid,
                    "✅✅✅✅✅✅✅✅✅✅\n"
                    "  🎊 <b>𝗖𝗢𝗗𝗘 𝗥𝗘𝗗𝗘𝗘𝗠𝗘𝗗!</b> 🎊\n"
                    "✅✅✅✅✅✅✅✅✅✅\n\n"
                    f"🎟️ Code: <code>{code}</code>\n"
                    f"🟢 <b>+{pts} Points</b> added!\n"
                    f"💎 Balance: <b>{db[uid]['points']} pts</b>",
                    menu_kb()
                )
        else:
            send(cid,
                "❌❌❌❌❌❌❌❌❌❌\n"
                "  🚫 <b>𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗖𝗢𝗗𝗘!</b>\n"
                "❌❌❌❌❌❌❌❌❌❌\n\n"
                "This code does not exist!\nPlease check and try again.",
                menu_kb()
            )

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
                send(cid, f"✅ <b>Code Created!</b>\n🎟️ <code>{code}</code> → 💎 <b>{pts} pts</b>")
            else:
                send(cid, "Usage: <code>/addcode CODE POINTS</code>")
            save_db(db); return

        if text.startswith('/delcode '):
            parts = text.split()
            code  = parts[1].upper() if len(parts) > 1 else ''
            codes = load_codes()
            if code in codes:
                del codes[code]; save_codes(codes)
                send(cid, f"🗑️ Code <code>{code}</code> deleted!")
            else:
                send(cid, "❌ Code not found!")
            save_db(db); return

        if text.startswith('/addpoints '):
            parts = text.split()
            if len(parts) == 3:
                tid = parts[1]; pts = int(parts[2])
                get_user(db, tid)
                db[tid]['points'] += pts
                save_db(db)
                send(cid, f"✅ Added 💎 <b>{pts} pts</b> to <code>{tid}</code>!")
            return

        if text == '/stats':
            total   = len(db)
            tpoints = sum(u.get('points', 0) for u in db.values())
            tsearch = sum(u.get('searches', 0) for u in db.values())
            send(cid,
                "📊 <b>𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗦</b>\n\n"
                f"👥 Users:    <b>{total}</b>\n"
                f"💎 Points:   <b>{tpoints}</b>\n"
                f"🔎 Searches: <b>{tsearch}</b>"
            )
            save_db(db); return

        if text.startswith('/broadcast '):
            bmsg = text[11:]
            sent = 0
            for bid in db.keys():
                try:
                    r = tg('sendMessage', {
                        'chat_id': bid,
                        'text': (
                            "📢📢📢📢📢📢📢📢📢📢\n"
                            "  📣 <b>𝗔𝗡𝗡𝗢𝗨𝗡𝗖𝗘𝗠𝗘𝗡𝗧</b>\n"
                            "📢📢📢📢📢📢📢📢📢📢\n\n"
                            f"{bmsg}\n\n"
                            "🤖 <b>𝗠𝗮𝗱𝗲 𝗯𝘆 𝗣𝗥𝗜𝗡𝗖𝗘</b>"
                        ),
                        'parse_mode': 'HTML'
                    })
                    if r.get('ok'): sent += 1
                except:
                    pass
            send(cid, f"📢 Sent to <b>{sent}</b> users!")
            save_db(db); return

        if text == '/listcodes':
            codes = load_codes()
            if not codes:
                send(cid, "❌ No active promo codes.")
            else:
                lines = "🎟️ <b>𝗔𝗰𝘁𝗶𝘃𝗲 𝗖𝗼𝗱𝗲𝘀:</b>\n\n"
                for c, info in codes.items():
                    lines += f"┣ <code>{c}</code> — 💎 {info['points']} pts | Used: {len(info.get('used',[]))}x\n"
                send(cid, lines)
            save_db(db); return

    # Search by manual ID
    if text and not text.startswith('/'):
        if not text.isdigit():
            send(cid,
                "⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️\n"
                "  ❗ <b>𝗪𝗥𝗢𝗡𝗚 𝗙𝗢𝗥𝗠𝗔𝗧!</b>\n"
                "⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️\n\n"
                "📲 Send a <b>Telegram User ID</b> only!\n"
                "<i>Example: <code>123456789</code></i>\n\n"
                "💡 Use @userinfobot to find IDs!",
                [[
                    {'text': '🔎 𝗦𝗲𝗮𝗿𝗰𝗵 𝗚𝘂𝗶𝗱𝗲', 'callback_data': 'how_search'},
                    {'text': '🏠 𝗠𝗮𝗶𝗻 𝗠𝗲𝗻𝘂',    'callback_data': 'menu'}
                ]]
            )
            save_db(db); return

        do_search(cid, uid, text, db)

    save_db(db)

# ═══════════════════════════════════════════════════
#   WEBHOOK ROUTE
# ═══════════════════════════════════════════════════
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return 'ok'

    if 'inline_query' in data:
        handle_inline(data['inline_query'])
    elif 'callback_query' in data:
        handle_callback(data['callback_query'])
    elif 'message' in data:
        handle_message(data['message'])

    return 'ok'

@app.route('/')
def index():
    return '💀 TG LOOKUP BOT is Running! Made by PRINCE'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
