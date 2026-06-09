# config.py
# الإعدادات المركزية للبوت

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# إضافة مسار generated_proto إلى sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated_proto'))

# ═══════════════════════════════════════════════════════════════════════
# 🔐 إعدادات البوت الرئيسي
# ═══════════════════════════════════════════════════════════════════════

MAIN_BOT_UID = os.getenv("MAIN_BOT_UID", "4245749321")
MAIN_BOT_PASSWORD = os.getenv("MAIN_BOT_PASSWORD", "71496B76FB9E4BA2C14F80D7A75A5DD25F75793F267E4C21B73D662881404ED1")

# ═══════════════════════════════════════════════════════════════════════
# ⚙️ إعدادات الإعجابات
# ═══════════════════════════════════════════════════════════════════════

MAX_LIKES_PER_COMMAND = 100
LIKE_DELAY_SECONDS = 0.5
LIKE_TIMEOUT_SECONDS = 10
BATCH_SIZE = 10
MAX_RETRIES = 3
USE_FUTURE_PROTOCOL = True

# ═══════════════════════════════════════════════════════════════════════
# 🌍 إعدادات المناطق
# ═══════════════════════════════════════════════════════════════════════

SUPPORTED_REGIONS = ["ME", "SG", "IND", "BD", "BR", "PK", "US", "ID", "TH", "VN", "MY"]

REGION_ALIASES = {
    "ME": ["ME", "MIDEAST", "MIDDLEEAST", "ARAB", "SAUDI", "UAE", "EGYPT", "KW", "QA", "BH", "OM", "JO", "SA", "AE", "EG"],
    "SG": ["SG", "SINGAPORE"],
    "IND": ["IND", "INDIA", "IN"],
    "BD": ["BD", "BANGLADESH"],
    "BR": ["BR", "BRAZIL"],
    "PK": ["PK", "PAKISTAN"],
    "US": ["US", "USA", "AMERICA"],
    "ID": ["ID", "INDONESIA"],
    "TH": ["TH", "THAILAND"],
    "VN": ["VN", "VIETNAM"],
    "MY": ["MY", "MALAYSIA"],
}

REGION_FLAGS = {
    "ME": "🇸🇦", "SG": "🇸🇬", "IND": "🇮🇳", "BD": "🇧🇩",
    "BR": "🇧🇷", "PK": "🇵🇰", "US": "🇺🇸", "ID": "🇮🇩",
    "TH": "🇹🇭", "VN": "🇻🇳", "MY": "🇲🇾"
}

REGION_NAMES_AR = {
    "ME": "الشرق الأوسط",
    "SG": "سنغافورة",
    "IND": "الهند",
    "BD": "بنغلاديش",
    "BR": "البرازيل",
    "PK": "باكستان",
    "US": "أمريكا",
    "ID": "إندونيسيا",
    "TH": "تايلاند",
    "VN": "فيتنام",
    "MY": "ماليزيا"
}

# ═══════════════════════════════════════════════════════════════════════
# 🔌 إعدادات الاتصال
# ═══════════════════════════════════════════════════════════════════════

RECONNECT_DELAY = 5
MAX_RECONNECT_ATTEMPTS = 10
HEARTBEAT_INTERVAL = 30

# ═══════════════════════════════════════════════════════════════════════
# 🎨 إعدادات العرض
# ═══════════════════════════════════════════════════════════════════════

BOT_NAME = "Delta Like Bot"
BOT_VERSION = "3.0.0"
BOT_DEVELOPER = "@dre.jihad"
BOT_DISCORD = "@dre.jihad"

COLORS = [
    "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]",
    "[FF00FF]", "[00FFFF]", "[FFA500]", "[FFC0CB]",
    "[FF4500]", "[32CD32]", "[9370DB]", "[FF1493]",
]


def normalize_region(region_input: str) -> str:
    """تحويل اسم المنطقة إلى الصيغة القياسية"""
    if not region_input:
        return "ME"
    
    region_upper = region_input.upper().strip()
    
    for standard_region, aliases in REGION_ALIASES.items():
        if region_upper in aliases or region_upper == standard_region:
            return standard_region
    
    return "ME"


def get_region_flag(region: str) -> str:
    """الحصول على علم المنطقة"""
    return REGION_FLAGS.get(region.upper(), "🌍")


def get_region_name(region: str) -> str:
    """الحصول على اسم المنطقة بالعربية"""
    return REGION_NAMES_AR.get(region.upper(), region.upper())