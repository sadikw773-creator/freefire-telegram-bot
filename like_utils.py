# like_utils.py - نسخة تعمل مع aiohttp فقط (بدون httpx)

import asyncio
import json
import time
from typing import Tuple, Optional, Dict
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import aiohttp

# استيراد protobuf
try:
    from generated_proto import MajoRLoGinrEq_pb2 as MajorLoginRequest
    from generated_proto import MajoRLoGinrEs_pb2 as MajorLoginResponse
    PROTO_AVAILABLE = True
except ImportError:
    PROTO_AVAILABLE = False
    print("[WARN] Protobuf modules not available")

# Encryption Constants
MAIN_KEY = b'Yg&tc%DEuh6%Zc^8'
MAIN_IV = b'6oyZDr22E3ychjM%'
RELEASEVERSION = "OB50"
USERAGENT = "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)"

# Region to server URL mapping
REGION_URLS = {
    "IND": "https://client.ind.freefiremobile.com",
    "BD": "https://clientbp.ggblueshark.com",
    "PK": "https://clientbp.ggblueshark.com",
    "BR": "https://client.us.freefiremobile.com",
    "US": "https://client.us.freefiremobile.com",
    "SG": "https://clientbp.ggblueshark.com",
    "ID": "https://clientbp.ggblueshark.com",
    "TH": "https://clientbp.ggblueshark.com",
    "VN": "https://clientbp.ggblueshark.com",
    "MY": "https://clientbp.ggblueshark.com",
    "ME": "https://clientbp.ggblueshark.com",
    "default": "https://clientbp.ggblueshark.com"
}


def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    """Encrypt data using AES-CBC mode"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext, AES.block_size)
    return cipher.encrypt(padded)


def encode_varint(value: int) -> bytes:
    """Encode integer as protobuf varint"""
    result = []
    while value > 0x7F:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value & 0x7F)
    return bytes(result)


def create_protobuf_field(field_number: int, wire_type: int, value) -> bytes:
    """Create a protobuf field with tag"""
    tag = (field_number << 3) | wire_type
    tag_bytes = encode_varint(tag)
    
    if wire_type == 0:  # Varint
        return tag_bytes + encode_varint(value)
    elif wire_type == 2:  # Length-delimited
        if isinstance(value, str):
            value = value.encode('utf-8')
        return tag_bytes + encode_varint(len(value)) + value
    return tag_bytes


def create_simple_like_protobuf(uid: int, region: str) -> bytes:
    """Create protobuf-like message manually"""
    msg = create_protobuf_field(1, 0, uid)
    msg += create_protobuf_field(2, 2, region)
    return msg


def create_future_like_protobuf(uid: int, region: str, timestamp: int = None) -> bytes:
    """Create advanced protobuf message with future support"""
    if timestamp is None:
        timestamp = int(time.time())
    
    msg = create_protobuf_field(1, 0, uid)
    msg += create_protobuf_field(2, 2, region)
    msg += create_protobuf_field(3, 0, timestamp)
    msg += create_protobuf_field(4, 0, 1)
    return msg


async def get_jwt_from_guest(uid: str, password: str) -> Tuple[Optional[str], Optional[str]]:
    """Get JWT token from Free Fire guest account credentials"""
    try:
        # Step 1: Get access token from OAuth
        oauth_url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        oauth_payload = {
            "uid": uid,
            "password": password,
            "response_type": "token",
            "client_type": "2",
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_id": "100067"
        }
        oauth_headers = {
            'User-Agent': USERAGENT,
            'Content-Type': "application/x-www-form-urlencoded"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(oauth_url, data=oauth_payload, headers=oauth_headers, timeout=30) as response:
                if response.status != 200:
                    print(f"[LIKE] OAuth failed: {response.status}")
                    return None, None
                
                data = await response.json()
                access_token = data.get("access_token")
                open_id = data.get("open_id")
                
                if not access_token or not open_id:
                    print(f"[LIKE] Failed to get access token for {uid}")
                    return None, None
                
                print(f"[LIKE] OAuth successful for {uid}")
        
        # Step 2: Login to Free Fire and get JWT
        if not PROTO_AVAILABLE:
            print("[LIKE] Protobuf not available, using mock token")
            return "mock_token_" + uid, "SG"
        
        from datetime import datetime
        
        # Create MajorLogin protobuf
        major_login = MajorLoginRequest.MajorLogin()
        major_login.event_time = str(datetime.now())[:-7]
        major_login.game_name = "free fire"
        major_login.platform_id = 1
        major_login.client_version = "1.114.1"
        major_login.system_software = "Android OS 13 / API-33"
        major_login.system_hardware = "Handheld"
        major_login.telecom_operator = "Grameenphone"
        major_login.network_type = "WIFI"
        major_login.screen_width = 1920
        major_login.screen_height = 1080
        major_login.screen_dpi = "280"
        major_login.processor_details = "ARM64 FP ASIMD AES"
        major_login.memory = 3003
        major_login.gpu_renderer = "Adreno (TM) 640"
        major_login.gpu_version = "OpenGL ES 3.1"
        major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
        major_login.client_ip = "103.43.149.100"
        major_login.language = "en"
        major_login.open_id = open_id
        major_login.open_id_type = "4"
        major_login.device_type = "Handheld"
        
        # Add memory available
        memory_available = major_login.memory_available
        memory_available.version = 55
        memory_available.hidden_value = 81
        
        major_login.access_token = access_token
        major_login.platform_sdk_id = 1
        major_login.network_operator_a = "Grameenphone"
        major_login.network_type_a = "WIFI"
        major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
        major_login.external_storage_total = 36235
        major_login.external_storage_available = 31335
        major_login.internal_storage_total = 2519
        major_login.internal_storage_available = 703
        major_login.game_disk_storage_available = 25010
        major_login.game_disk_storage_total = 26628
        major_login.external_sdcard_avail_storage = 32992
        major_login.external_sdcard_total_storage = 36235
        major_login.login_by = 3
        major_login.library_path = "/data/app/com.dts.freefireth/lib/arm64"
        major_login.reg_avatar = 1
        major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth/base.apk"
        major_login.channel_type = 3
        major_login.cpu_type = 2
        major_login.cpu_architecture = "64"
        major_login.client_version_code = "2019118695"
        major_login.graphics_api = "OpenGLES2"
        major_login.supported_astc_bitset = 16383
        major_login.login_open_id_type = 4
        major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0OUgsvA1snWlBaO1kFYg=="
        major_login.loading_time = 13564
        major_login.release_channel = "android"
        major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
        major_login.android_engine_init_flag = 110009
        major_login.if_push = 1
        major_login.is_vpn = 1
        major_login.origin_platform_type = "4"
        major_login.primary_platform_type = "4"
        
        serialized = major_login.SerializeToString()
        encrypted = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, serialized)
        
        # Send to MajorLogin
        login_url = "https://loginbp.ggblueshark.com/MajorLogin"
        login_headers = {
            "User-Agent": USERAGENT,
            "Content-Type": "application/octet-stream",
            "X-Unity-Version": "2018.4.11f1",
            "ReleaseVersion": RELEASEVERSION,
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(login_url, data=encrypted, headers=login_headers, timeout=30) as response:
                if response.status != 200:
                    print(f"[LIKE] MajorLogin failed: {response.status}")
                    return None, None
                
                response_data = await response.read()
                proto = MajorLoginResponse.MajorLoginRes()
                proto.ParseFromString(response_data)
                
                jwt_token = proto.token
                region = getattr(proto, 'region', 'SG')
                
                print(f"[LIKE] JWT token obtained for {uid}, region: {region}")
                return jwt_token, region
        
    except Exception as e:
        print(f"[LIKE] Error getting JWT: {e}")
        import traceback
        traceback.print_exc()
        return None, None


async def search_player(uid: str, region: str = "BD") -> Optional[Dict]:
    """Search for a Free Fire player by UID"""
    try:
        api_url = f"https://info-ob49.vercel.app/api/account/?uid={uid}&region={region.lower()}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=30) as response:
                if response.status == 200:
                    return await response.json()
                return None
    except Exception as e:
        print(f"[SEARCH] Error: {e}")
        return None


async def get_like_count(uid: str, region: str = "BD") -> Optional[int]:
    """Get the current like count for a player"""
    player_data = await search_player(uid, region)
    if player_data and "basicInfo" in player_data:
        return player_data["basicInfo"].get("liked", 0)
    return None


async def send_like_to_player(target_uid: str, bot_uid: str, bot_password: str, region: str = "BD", max_retries: int = 1, use_future: bool = False) -> bool:
    """Send a like from bot account to target player"""
    try:
        # Get JWT token
        jwt_token, bot_region = await get_jwt_from_guest(bot_uid, bot_password)
        
        if not jwt_token:
            print(f"[LIKE] ❌ Failed to authenticate {bot_uid}")
            return False
        
        await asyncio.sleep(0.5)
        
        # Create like protobuf payload
        if use_future:
            like_message = create_future_like_protobuf(int(target_uid), region)
        else:
            like_message = create_simple_like_protobuf(int(target_uid), region)
        
        # Encrypt payload
        encrypted_payload = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, like_message)
        
        # Determine server URL
        server_url = REGION_URLS.get(region.upper(), REGION_URLS["default"])
        like_url = f"{server_url}/LikeProfile"
        
        # Prepare headers
        headers = {
            "User-Agent": USERAGENT,
            "Content-Type": "application/octet-stream",
            "Authorization": f"Bearer {jwt_token}",
            "X-Unity-Version": "2018.4.11f1",
            "ReleaseVersion": RELEASEVERSION,
        }
        
        # Send like request
        async with aiohttp.ClientSession() as session:
            await asyncio.sleep(0.3)
            async with session.post(like_url, data=encrypted_payload, headers=headers, timeout=30) as response:
                if response.status == 200:
                    print(f"[LIKE] ✅ Sent like to {target_uid} from {bot_uid}!")
                    return True
                elif response.status == 401:
                    # Retry with fresh token
                    print(f"[LIKE] ⚠️ Token error for {bot_uid}, retrying...")
                    await asyncio.sleep(1.0)
                    
                    jwt_token, _ = await get_jwt_from_guest(bot_uid, bot_password)
                    if jwt_token:
                        headers["Authorization"] = f"Bearer {jwt_token}"
                        async with session.post(like_url, data=encrypted_payload, headers=headers, timeout=30) as retry_response:
                            if retry_response.status == 200:
                                print(f"[LIKE] ✅ Success on retry!")
                                return True
                    return False
                else:
                    print(f"[LIKE] ❌ Failed. Status: {response.status}")
                    return False
                
    except Exception as e:
        print(f"[LIKE] ❌ Error: {e}")
        return False


async def send_bulk_likes(target_uid: str, bot_accounts: list, region: str = "BD", use_future: bool = False, batch_size: int = 10) -> dict:
    """Send likes from multiple bot accounts in batches"""
    results = {
        "total": len(bot_accounts),
        "success": 0,
        "failed": 0,
        "successful_bots": [],
        "failed_bots": []
    }
    
    for i in range(0, len(bot_accounts), batch_size):
        batch = bot_accounts[i:i + batch_size]
        
        for bot_uid, bot_password in batch:
            if not bot_uid or not bot_password:
                results["failed"] += 1
                results["failed_bots"].append(bot_uid)
                continue
            
            try:
                success = await send_like_to_player(target_uid, bot_uid, bot_password, region, use_future=use_future)
                if success:
                    results["success"] += 1
                    results["successful_bots"].append(bot_uid)
                else:
                    results["failed"] += 1
                    results["failed_bots"].append(bot_uid)
                await asyncio.sleep(0.5)
            except Exception as e:
                results["failed"] += 1
                results["failed_bots"].append(bot_uid)
                print(f"[BULK] Error with {bot_uid}: {e}")
        
        # Delay between batches
        if i + batch_size < len(bot_accounts):
            await asyncio.sleep(1.5)
    
    return results


async def send_like_with_retry(target_uid: str, bot_uid: str, bot_password: str, region: str = "BD", max_retries: int = 3) -> bool:
    """Send like with automatic retry"""
    for attempt in range(max_retries):
        success = await send_like_to_player(target_uid, bot_uid, bot_password, region)
        if success:
            return True
        await asyncio.sleep(2)
    return False


async def validate_region(region: str) -> bool:
    """Check if region is valid"""
    return region.upper() in REGION_URLS


async def get_all_regions() -> list:
    """Get list of all supported regions"""
    return list(REGION_URLS.keys())