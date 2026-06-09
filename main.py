# main.py - النسخة النهائية مع دعم كامل لـ Protobuf

import os
import sys
import asyncio
import signal

# إضافة مسار generated_proto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated_proto'))

from cfonts import render

# استيراد الإعدادات
from config import (
    MAIN_BOT_UID, MAIN_BOT_PASSWORD, BOT_NAME, BOT_VERSION,
    SUPPORTED_REGIONS, normalize_region, get_region_flag,
    BATCH_SIZE, MAX_RETRIES, USE_FUTURE_PROTOCOL
)

# استيراد حسابات الإعجابات
from like_bot_accounts import LIKE_BOT_ACCOUNTS

# استيراد أدوات الإعجابات
from like_utils import send_bulk_likes, search_player, get_like_count

# استيراد أدوات الشبكة
from network_utils import (
    SEndMsG, transmit_network_packet, Emote_k, GenJoinSquadsPacket,
    DecodeWhisperMessage, decode_team_packet
)

# استيراد اختصارات الإيموتات
from emote_shortcuts import SHORTCUT_EMOTES, DEFAULT_PLAYER_UIDS

# المتغيرات العامة
session_writer = None
chat_handler = None
running_tasks = set()
auto_emote_active = False


def generate_color():
    colors = ["[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFA500]", "[FFC0CB]"]
    return __import__('random').choice(colors)


async def send_chat_message(chat_type, message, sender_uid, chat_id, key, iv):
    """إرسال رسالة في الدردشة"""
    global chat_handler
    try:
        packet = await SEndMsG(chat_type, message, sender_uid, chat_id, key, iv)
        if chat_handler and packet:
            chat_handler.write(packet.encode() if isinstance(packet, str) else packet)
            await chat_handler.drain()
    except Exception as e:
        print(f"[CHAT] خطأ: {e}")


async def send_likes_advanced(target_uid, region, sender_uid, chat_id, chat_type, key, iv):
    """إرسال الإعجابات باستخدام النظام المتقدم"""
    total_bots = len(LIKE_BOT_ACCOUNTS)
    
    if total_bots == 0:
        await send_chat_message(chat_type, "[B][C][FF0000]\n❌ لا توجد حسابات بوت!", sender_uid, chat_id, key, iv)
        return
    
    # رسالة البداية
    start_msg = f"""[B][C][00FF00]
╔══════════════════════════════════════╗
║     💖 جاري إرسال الإعجابات          ║
╚══════════════════════════════════════╝

[FFFF00]🎯 المستهدف:[FFFFFF] {target_uid}
[FFFF00]🌍 الخادم:[FFFFFF] {get_region_flag(region)} {region}
[FFFF00]🤖 عدد البوتات:[FFFFFF] {total_bots}

[00FF00]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[FFFFFF]"""
    
    await send_chat_message(chat_type, start_msg, sender_uid, chat_id, key, iv)
    
    # إرسال الإعجابات
    results = await send_bulk_likes(
        target_uid=target_uid,
        bot_accounts=LIKE_BOT_ACCOUNTS,
        region=region,
        use_future=USE_FUTURE_PROTOCOL,
        batch_size=BATCH_SIZE
    )
    
    success_rate = (results["success"] / results["total"] * 100) if results["total"] > 0 else 0
    
    result_msg = f"""[B][C][00FF00]
╔══════════════════════════════════════╗
║     📊 تقرير الإعجابات               ║
╚══════════════════════════════════════╝

[00FF00]✅ نجح:[FFFFFF] {results['success']}
[FF0000]❌ فشل:[FFFFFF] {results['failed']}
[FFFF00]📈 نسبة النجاح:[FFFFFF] {success_rate:.1f}%

[00FF00]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[FFFFFF]"""
    
    await send_chat_message(chat_type, result_msg, sender_uid, chat_id, key, iv)


async def handle_command(command, sender_uid, chat_id, chat_type, key, iv):
    """معالجة الأوامر"""
    global auto_emote_active
    
    cmd_parts = command.strip().split()
    if not cmd_parts:
        return
    
    cmd = cmd_parts[0].lower()
    total_bots = len(LIKE_BOT_ACCOUNTS)
    
    # أمر المساعدة
    if cmd in ["/help", "/commands", "/cmd"]:
        help_text = f"""[B][C]{generate_color()}
╔══════════════════════════════════════╗
║     🤖 {BOT_NAME} v{BOT_VERSION}         ║
╚══════════════════════════════════════╝

[00FF00]/like <uid> [region]{' ':<20}[FFFFFF]إرسال {total_bots} إعجاب
[00FF00]/info <uid> [region]{' ':<20}[FFFFFF]معلومات اللاعب
[00FF00]/likes <uid> [region]{' ':<19}[FFFFFF]عدد الإعجابات
[00FF00]/search <uid> [region]{' ':<19}[FFFFFF]البحث عن لاعب
[00FF00]/emote <uid> <id>{' ':<23}[FFFFFF]إرسال إيموتة
[00FF00]/join <code>{' ':<32}[FFFFFF]انضمام للسرب
[00FF00]/ak{' ':<40}[FFFFFF]إيموتات تلقائية
[00FF00]/regions{' ':<38}[FFFFFF]قائمة الخوادم
[00FF00]/stats{' ':<38}[FFFFFF]إحصائيات البوت

[FFFF00]━━━ أمثلة ━━━[FFFFFF]
/like 123456789 ME
/info 123456789 SA

[00FF00]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[FFFFFF]"""
        
        await send_chat_message(chat_type, help_text, sender_uid, chat_id, key, iv)
    
    # أمر الإعجابات
    elif cmd == "/like":
        if len(cmd_parts) < 2:
            await send_chat_message(chat_type, "[B][C][FF0000]\n❌ استخدم: /like <uid> [region]", sender_uid, chat_id, key, iv)
            return
        
        target_uid = cmd_parts[1]
        region = normalize_region(cmd_parts[2] if len(cmd_parts) >= 3 else "ME")
        
        await send_chat_message(chat_type, f"[B][C][00FF00]\n✅ جاري تجهيز {total_bots} إعجاب...", sender_uid, chat_id, key, iv)
        asyncio.create_task(send_likes_advanced(target_uid, region, sender_uid, chat_id, chat_type, key, iv))
    
    # أمر معلومات اللاعب
    elif cmd == "/info":
        if len(cmd_parts) < 2:
            await send_chat_message(chat_type, "[B][C][FF0000]\n❌ استخدم: /info <uid> [region]", sender_uid, chat_id, key, iv)
            return
        
        target_uid = cmd_parts[1]
        region = normalize_region(cmd_parts[2] if len(cmd_parts) >= 3 else "ME")
        
        player_data = await search_player(target_uid, region.lower())
        if player_data and "basicInfo" in player_data:
            basic = player_data["basicInfo"]
            msg = f"""[B][C][00FF00]
╔════════════════════════════════╗
║     👤 معلومات اللاعب          ║
╚════════════════════════════════╝

[FFFF00]📛 الاسم:[FFFFFF] {basic.get('nickname', 'غير معروف')}
[FFFF00]⭐ المستوى:[FFFFFF] {basic.get('level', '?')}
[FFFF00]💖 الإعجابات:[FFFFFF] {basic.get('liked', 0)}
[FFFF00]🌍 الخادم:[FFFFFF] {get_region_flag(region)} {region}

[00FF00]━━━━━━━━━━━━━━━━━━━━━━━━━━[FFFFFF]"""
        else:
            msg = f"[B][C][FF0000]\n❌ لم يتم العثور على اللاعب {target_uid}"
        
        await send_chat_message(chat_type, msg, sender_uid, chat_id, key, iv)
    
    # أمر عدد الإعجابات
    elif cmd == "/likes":
        if len(cmd_parts) < 2:
            await send_chat_message(chat_type, "[B][C][FF0000]\n❌ استخدم: /likes <uid> [region]", sender_uid, chat_id, key, iv)
            return
        
        target_uid = cmd_parts[1]
        region = normalize_region(cmd_parts[2] if len(cmd_parts) >= 3 else "ME")
        
        like_count = await get_like_count(target_uid, region.lower())
        if like_count is not None:
            msg = f"[B][C][00FF00]\n💖 عدد إعجابات {target_uid}: {like_count} (خادم {region})"
        else:
            msg = f"[B][C][FF0000]\n❌ لم يتم العثور على اللاعب {target_uid}"
        
        await send_chat_message(chat_type, msg, sender_uid, chat_id, key, iv)
    
    # أمر البحث
    elif cmd == "/search":
        if len(cmd_parts) < 2:
            await send_chat_message(chat_type, "[B][C][FF0000]\n❌ استخدم: /search <uid> [region]", sender_uid, chat_id, key, iv)
            return
        
        target_uid = cmd_parts[1]
        region = normalize_region(cmd_parts[2] if len(cmd_parts) >= 3 else "ME")
        
        player_data = await search_player(target_uid, region.lower())
        if player_data and "basicInfo" in player_data:
            nickname = player_data["basicInfo"].get("nickname", "غير معروف")
            msg = f"[B][C][00FF00]\n✅ تم العثور على {nickname} (UID: {target_uid}) في خادم {region}"
        else:
            msg = f"[B][C][FF0000]\n❌ لم يتم العثور على اللاعب {target_uid}"
        
        await send_chat_message(chat_type, msg, sender_uid, chat_id, key, iv)
    
    # أمر إرسال إيموتة
    elif cmd == "/emote" and len(cmd_parts) >= 3:
        target_uid = cmd_parts[1]
        emote_id = int(cmd_parts[2])
        region = normalize_region(cmd_parts[3] if len(cmd_parts) >= 4 else "ME")
        
        packet = await Emote_k(target_uid, emote_id, key, iv, region)
        if session_writer and packet:
            session_writer.write(packet.encode() if isinstance(packet, str) else packet)
            await session_writer.drain()
        
        await send_chat_message(chat_type, f"[B][C][00FF00]\n✅ تم إرسال الإيموتة {emote_id} إلى {target_uid}", sender_uid, chat_id, key, iv)
    
    # اختصارات الإيموتات
    elif cmd in SHORTCUT_EMOTES:
        emote_id, emote_name, targets = SHORTCUT_EMOTES[cmd]
        targets = targets if targets else DEFAULT_PLAYER_UIDS
        
        for target in targets:
            packet = await Emote_k(target, emote_id, key, iv, "ME")
            if session_writer and packet:
                session_writer.write(packet.encode() if isinstance(packet, str) else packet)
                await session_writer.drain()
            await asyncio.sleep(0.3)
        
        await send_chat_message(chat_type, f"[B][C][00FF00]\n✅ تم إرسال {emote_name}", sender_uid, chat_id, key, iv)
    
    # أمر الانضمام للسرب
    elif cmd == "/join" and len(cmd_parts) >= 2:
        code = cmd_parts[1]
        packet = await GenJoinSquadsPacket(code, key, iv)
        if session_writer and packet:
            session_writer.write(packet.encode() if isinstance(packet, str) else packet)
            await session_writer.drain()
        await send_chat_message(chat_type, f"[B][C][00FF00]\n✅ جاري الانضمام إلى {code}", sender_uid, chat_id, key, iv)
    
    # أمر الخوادم
    elif cmd == "/regions":
        regions_msg = f"""[B][C][00FFFF]
╔════════════════════════════════╗
║     🌍 الخوادم المدعومة        ║
╚════════════════════════════════╝

[FFFF00]🇸🇦 ME - الشرق الأوسط
[FFFF00]🇸🇬 SG - سنغافورة
[FFFF00]🇮🇳 IND - الهند
[FFFF00]🇧🇩 BD - بنغلاديش
[FFFF00]🇧🇷 BR - البرازيل
[FFFF00]🇵🇰 PK - باكستان
[FFFF00]🇺🇸 US - أمريكا

[00FF00]━━━━━━━━━━━━━━━━━━━━━━━━━━[FFFFFF]"""
        
        await send_chat_message(chat_type, regions_msg, sender_uid, chat_id, key, iv)
    
    # أمر الإحصائيات
    elif cmd == "/stats":
        stats_msg = f"""[B][C][00FF00]
╔════════════════════════════════╗
║     📊 إحصائيات البوت          ║
╚════════════════════════════════╝

[FFFF00]🤖 بوتات الإعجاب:[FFFFFF] {total_bots}
[FFFF00]⚡ الحالة:[FFFFFF] [00FF00]● نشط[FFFFFF]
[FFFF00]🌍 الخادم الرئيسي:[FFFFFF] 🇸🇦 ME
[FFFF00]⚡ الدفعات المتزامنة:[FFFFFF] {BATCH_SIZE}

[00FF00]━━━━━━━━━━━━━━━━━━━━━━━━━━[FFFFFF]"""
        
        await send_chat_message(chat_type, stats_msg, sender_uid, chat_id, key, iv)
    
    # ترحيب
    elif cmd in ["hi", "hello", "salam", "مرحبا"]:
        welcome_msg = f"""[B][C]{generate_color()}
👋 أهلاً بك! أنا {BOT_NAME}
📝 اكتب /help لبدء الاستخدام"""
        await send_chat_message(chat_type, welcome_msg, sender_uid, chat_id, key, iv)
    
    else:
        await send_chat_message(chat_type, f"[B][C][FF0000]\n❌ أمر غير معروف: {cmd}\nاستخدم /help", sender_uid, chat_id, key, iv)


async def main():
    """تشغيل البوت"""
    if not MAIN_BOT_UID or not MAIN_BOT_PASSWORD:
        print("[ERROR] ❌ لم يتم تعيين بيانات البوت الرئيسي!")
        print("\n🔧 قم بتعديل MAIN_BOT_UID و MAIN_BOT_PASSWORD في ملف config.py")
        return
    
    os.system("clear" if os.name == "posix" else "cls")
    
    print(render(BOT_NAME.upper(), colors=["white", "green"], align="center"))
    print("")
    print("═" * 55)
    print(f"         🤖 {BOT_NAME} v{BOT_VERSION}")
    print("═" * 55)
    print(f"  📊 بوتات الإعجاب: {len(LIKE_BOT_ACCOUNTS)}")
    print(f"  🌍 الخادم الرئيسي: 🇸🇦 ME (الشرق الأوسط)")
    print(f"  🔐 التشفير: AES-256 + JWT + Protobuf")
    print(f"  ⚡ الحالة: [00FF00]● نشط وجاهز[FFFFFF]")
    print("═" * 55)
    print(f"\n  💡 /like 123456789 ME")
    print(f"  💡 /help لعرض جميع الأوامر")
    print(f"\n  [SYSTEM] ✅ البوت جاهز!")
    print(f"  [SYSTEM] اضغط Ctrl+C للإيقاف\n")
    
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n[SYSTEM] 👋 تم إيقاف البوت")


if __name__ == "__main__":
    asyncio.run(main())