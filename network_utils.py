# network_utils.py
# أدوات الشبكة والتشفير مع دعم Protobuf

import json
import random
import asyncio
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# استيراد ملفات Protobuf
from generated_proto import (
    DEcwHisPErMsG_pb2 as DecodeWhisperMsg,
    MajoRLoGinrEs_pb2 as MajorLoginResponse,
    PorTs_pb2 as GetLoginDataResponse,
    MajoRLoGinrEq_pb2 as MajorLoginRequest,
    sQ_pb2 as ReceivedChat,
)

# نفس مفاتيح التشفير
MAIN_KEY = b'Yg&tc%DEuh6%Zc^8'
MAIN_IV = b'6oyZDr22E3ychjM%'
RELEASEVERSION = "OB50"
USERAGENT = "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)"


async def Ua():
    """إنشاء User-Agent عشوائي"""
    user_agents = [
        USERAGENT,
        "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        "Dalvik/2.1.0 (Linux; U; Android 12; SM-G991B Build/SP1A.210812.016)",
        "Dalvik/2.1.0 (Linux; U; Android 10; Mi 9T Pro Build/QKQ1.190825.002)",
        "Dalvik/2.1.0 (Linux; U; Android 13; Pixel 6 Pro Build/TQ1A.230205.002)",
    ]
    return random.choice(user_agents)


async def DecodE_HeX(timestamp):
    """تحويل الطابع الزمني إلى هيكس"""
    hex_string = hex(timestamp)[2:]
    if len(hex_string) % 2 != 0:
        hex_string = "0" + hex_string
    return hex_string


async def EnC_PacKeT(data, key, iv):
    """تشفير الحزمة"""
    try:
        if isinstance(data, str):
            data = data.encode()
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        padded_data = pad(data, AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return encrypted.hex()
    except Exception as e:
        print(f"[ENCRYPT] خطأ في التشفير: {e}")
        return ""


async def DeCode_PackEt(hex_data):
    """فك تشفير الحزمة"""
    try:
        cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
        decrypted = cipher.decrypt(bytes.fromhex(hex_data))
        unpadded = unpad(decrypted, AES.block_size)
        return unpadded.decode()
    except Exception as e:
        print(f"[DECODE] خطأ في فك التشفير: {e}")
        return "{}"


async def DecodeWhisperMessage(hex_packet):
    """فك تشفير رسالة الويسبر باستخدام Protobuf"""
    try:
        packet = bytes.fromhex(hex_packet)
        proto = DecodeWhisperMsg.DecodeWhisper()
        proto.ParseFromString(packet)
        return proto
    except Exception as e:
        print(f"[PROTO] خطأ في فك رسالة الويسبر: {e}")
        return None


async def decode_team_packet(hex_packet):
    """فك تشفير حزمة الفريق باستخدام Protobuf"""
    try:
        packet = bytes.fromhex(hex_packet)
        proto = ReceivedChat.recieved_chat()
        proto.ParseFromString(packet)
        return proto
    except Exception as e:
        print(f"[PROTO] خطأ في فك حزمة الفريق: {e}")
        return None


async def GeTSQDaTa(packet):
    """استخراج بيانات السرب من الحزمة"""
    try:
        owner_uid = packet.get("5", {}).get("data", {}).get("8", 0)
        chat_code = packet.get("5", {}).get("data", {}).get("16", "")
        squad_code = packet.get("5", {}).get("data", {}).get("15", "")
        return owner_uid, chat_code, squad_code
    except:
        return 0, "", ""


async def AutH_Chat(chat_type, owner_uid, chat_code, key, iv):
    """مصادقة الدردشة"""
    auth_data = {
        "type": chat_type,
        "uid": owner_uid,
        "chat_code": chat_code,
        "timestamp": int(datetime.now().timestamp())
    }
    encrypted = await EnC_PacKeT(json.dumps(auth_data), key, iv)
    return f"0500{encrypted}" if encrypted else ""


async def AuthClan(clan_id, clan_data, key, iv):
    """مصادقة العشيرة"""
    auth_data = {
        "action": "auth_clan",
        "clan_id": clan_id,
        "compiled_data": clan_data
    }
    encrypted = await EnC_PacKeT(json.dumps(auth_data), key, iv)
    return f"0500{encrypted}" if encrypted else ""


async def OpEnSq(key, iv, region="ME"):
    """فتح سرب جديد"""
    squad_data = {
        "action": "create_squad",
        "region": region,
        "max_players": 4,
        "is_private": False,
        "timestamp": int(datetime.now().timestamp())
    }
    encrypted = await EnC_PacKeT(json.dumps(squad_data), key, iv)
    return f"0500{encrypted}" if encrypted else ""


async def cHSq(squad_id, owner_uid, key, iv, region="ME"):
    """تغيير إعدادات السرب"""
    squad_data = {
        "action": "change_settings",
        "squad_id": squad_id,
        "owner_uid": owner_uid,
        "region": region
    }
    encrypted = await EnC_PacKeT(json.dumps(squad_data), key, iv)
    return f"0500{encrypted}" if encrypted else ""


async def SEnd_InV(squad_id, target_uid, key, iv, region="ME"):
    """إرسال دعوة للسرب"""
    invite_data = {
        "action": "send_invite",
        "squad_id": squad_id,
        "target_uid": target_uid,
        "region": region
    }
    encrypted = await EnC_PacKeT(json.dumps(invite_data), key, iv)
    return f"0500{encrypted}" if encrypted else ""


async def ExiT(uid, key, iv):
    """الخروج من السرب"""
    exit_data = {
        "action": "exit_squad",
        "uid": uid if uid else 0
    }
    encrypted = await EnC_PacKeT(json.dumps(exit_data), key, iv)
    return f"0500{encrypted}" if encrypted else ""


async def Emote_k(target_uid, emote_id, key, iv, region="ME"):
    """إرسال إيموتة للاعب"""
    emote_data = {
        "action": "send_emote",
        "target_uid": target_uid,
        "emote_id": emote_id,
        "region": region,
        "timestamp": int(datetime.now().timestamp())
    }
    encrypted = await EnC_PacKeT(json.dumps(emote_data), key, iv)
    return f"0500{encrypted}" if encrypted else ""


async def FS(key, iv):
    """فتح السرب السريع"""
    return await OpEnSq(key, iv)


async def GenJoinSquadsPacket(code, key, iv):
    """إنشاء حزمة الانضمام للسرب"""
    join_data = {
        "action": "join_squad",
        "code": code,
        "timestamp": int(datetime.now().timestamp())
    }
    encrypted = await EnC_PacKeT(json.dumps(join_data), key, iv)
    return f"0500{encrypted}" if encrypted else ""


async def SEndMsG(chat_type, message, sender_uid, chat_id, key, iv):
    """إرسال رسالة في الدردشة"""
    msg_data = {
        "action": "send_message",
        "chat_type": chat_type,
        "message": message,
        "sender_uid": sender_uid,
        "chat_id": chat_id,
        "timestamp": int(datetime.now().timestamp())
    }
    encrypted = await EnC_PacKeT(json.dumps(msg_data), key, iv)
    return f"0500{encrypted}" if encrypted else ""


async def transmit_network_packet(chat_handler, session_writer, packet_type, packet):
    """إرسال الحزمة عبر الشبكة"""
    try:
        if not packet:
            return
        if packet_type == "Chat" and chat_handler:
            chat_handler.write(packet if isinstance(packet, bytes) else packet.encode())
            await chat_handler.drain()
        elif packet_type == "Online" and session_writer:
            session_writer.write(packet if isinstance(packet, bytes) else packet.encode())
            await session_writer.drain()
    except Exception as e:
        print(f"[NETWORK] خطأ في الإرسال: {e}")


async def xSEndMsg(message, chat_type, sender_uid, target_uid, key, iv):
    """إرسال رسالة خاصة"""
    return await SEndMsG(chat_type, message, sender_uid, target_uid, key, iv)


async def xSEndMsgsQ(message, chat_id, key, iv):
    """إرسال رسالة للسرب"""
    return await SEndMsG(0, message, 0, chat_id, key, iv)


async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    """إنشاء توكن المصادقة"""
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:] if encrypted_packet else "00"
    
    if uid_length == 9:
        headers = "0000000"
    elif uid_length == 8:
        headers = "00000000"
    elif uid_length == 10:
        headers = "000000"
    elif uid_length == 7:
        headers = "000000000"
    else:
        headers = "0000000"
    
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"


async def cHTypE(H):
    """تحديد نوع الدردشة"""
    if not H or H == 0:
        return "Squad"
    elif H == 1:
        return "Clan"
    elif H == 2:
        return "Private"
    return "Squad"


def xMsGFixinG(value):
    """تنسيق القيم للعرض"""
    return str(value)