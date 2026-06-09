# player_utils.py
# أدوات الحصول على معلومات اللاعبين - متوافق مع like_utils.py

import os
import aiohttp
import json
from typing import Optional, Dict

# استيراد دوال البحث من like_utils
try:
    from like_utils import search_player, get_player_nickname, get_player_level, get_player_full_info
    USE_LIKE_UTILS = True
except ImportError:
    USE_LIKE_UTILS = False
    print("[WARN] like_utils غير متوفر، سيتم استخدام API بديل")


def get_api_token():
    """الحصول على توكن API من المتغيرات البيئية"""
    return os.getenv("FF_API_TOKEN", "")


async def get_player_info(uid: int, api_token: str = None, region: str = "ME") -> str:
    """
    الحصول على معلومات اللاعب وتنسيقها للعرض
    يستخدم like_utils إن وجد
    """
    if USE_LIKE_UTILS:
        try:
            # استخدام like_utils للحصول على المعلومات
            player_data = await search_player(str(uid), region.lower())
            
            if player_data and "basicInfo" in player_data:
                basic = player_data["basicInfo"]
                clan = player_data.get("clanInfo", {})
                
                nickname = basic.get("nickname", "غير معروف")
                level = basic.get("level", "?")
                likes = basic.get("liked", 0)
                signature = basic.get("signature", "لا توقيع")
                clan_name = clan.get("clan_name", "لا عشيرة")
                clan_level = clan.get("clan_level", "?")
                
                return f"""[B][C][00FFFF]
╔══════════════════════════════════════╗
║     👤 معلومات اللاعب                ║
╚══════════════════════════════════════╝

[FFFF00]🆔 UID:[FFFFFF] {uid}
[FFFF00]📛 الاسم:[FFFFFF] {nickname}
[FFFF00]⭐ المستوى:[FFFFFF] {level}
[FFFF00]💖 الإعجابات:[FFFFFF] {likes}
[FFFF00]🏰 العشيرة:[FFFFFF] {clan_name} (مستوى {clan_level})
[FFFF00]📝 التوقيع:[FFFFFF] {signature[:50]}
[FFFF00]🌍 الخادم:[FFFFFF] {region.upper()}

[00FF00]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[FFFFFF]"""
            
            return f"[B][C][FF0000]\n❌ لم يتم العثور على اللاعب {uid} في خادم {region}"
            
        except Exception as e:
            print(f"[INFO] خطأ في like_utils: {e}")
            # الاستمرار إلى API البديل
    
    # API بديل (مجاني)
    try:
        url = f"https://info-ob49.vercel.app/api/account/?uid={uid}&region={region.lower()}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and "basicInfo" in data:
                        basic = data["basicInfo"]
                        nickname = basic.get("nickname", "غير معروف")
                        level = basic.get("level", "?")
                        likes = basic.get("liked", 0)
                        
                        return f"""[B][C][00FF00]
╔════════════════════════════════╗
║     👤 معلومات اللاعب          ║
╚════════════════════════════════╝

[FFFF00]🆔 UID:[FFFFFF] {uid}
[FFFF00]📛 الاسم:[FFFFFF] {nickname}
[FFFF00]⭐ المستوى:[FFFFFF] {level}
[FFFF00]💖 الإعجابات:[FFFFFF] {likes}
[FFFF00]🌍 الخادم:[FFFFFF] {region.upper()}

[00FF00]━━━━━━━━━━━━━━━━━━━━━━━━━━[FFFFFF]"""
    except Exception as e:
        print(f"[INFO] خطأ في API البديل: {e}")
    
    return f"[B][C][FF0000]\n❌ تعذر الحصول على معلومات اللاعب {uid}"


async def get_player_name(uid: int, region: str = "ME") -> str:
    """الحصول على اسم اللاعب فقط"""
    if USE_LIKE_UTILS:
        try:
            name = await get_player_nickname(str(uid), region.lower())
            if name:
                return name
        except:
            pass
    
    # API بديل
    try:
        url = f"https://info-ob49.vercel.app/api/account/?uid={uid}&region={region.lower()}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("basicInfo", {}).get("nickname", f"Player_{uid}")
    except:
        pass
    
    return f"Player_{uid}"


async def check_player_exists(uid: int, region: str = "ME") -> bool:
    """التحقق من وجود اللاعب"""
    if USE_LIKE_UTILS:
        try:
            from like_utils import check_player_exists as check_exists
            return await check_exists(str(uid), region.lower())
        except:
            pass
    
    try:
        url = f"https://info-ob49.vercel.app/api/account/?uid={uid}&region={region.lower()}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data is not None and "basicInfo" in data
    except:
        pass
    
    return False