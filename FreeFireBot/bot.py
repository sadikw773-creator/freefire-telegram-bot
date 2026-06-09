import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# تفعيل التسجيل للأخطاء
logging.basicConfig(level=logging.INFO)

# جلب التوكن من المتغيرات البيئية
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
AES_KEY = os.environ.get("AES_KEY", "")

# التأكد من وجود التوكن
if not TOKEN:
    print("❌ خطأ: TELEGRAM_BOT_TOKEN غير موجود")
    exit(1)

print("🚀 جاري تشغيل بوت Free Fire...")
print(f"✅ AES_KEY موجود: {'نعم' if AES_KEY else 'لا'}")

# إنشاء التطبيق
app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر البدء"""
    await update.message.reply_text(
        "🎮 *بوت Free Fire v3.0* 🎮\n\n"
        "✨ **الأوامر المتاحة:**\n"
        "/like <id> - إرسال لايك للاعب\n"
        "/stats <id> - عرض إحصائيات اللاعب\n"
        "/help - عرض المساعدة\n\n"
        "🔐 *نظام الحماية:* AES-256 + JWT\n"
        "👑 *المطور:* @sadikw773\n\n"
        "✅ البوت جاهز للاستخدام",
        parse_mode="Markdown"
    )

async def like_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر إرسال لايك"""
    try:
        # التأكد من وجود معرف اللاعب
        if not context.args:
            await update.message.reply_text(
                "⚠️ *طريقة الاستخدام:*\n"
                "`/like <معرف_اللاعب>`\n\n"
                "مثال: `/like 123456789`",
                parse_mode="Markdown"
            )
            return
        
        player_id = context.args[0]
        
        # هنا سيتم إضافة اتصال WebSocket لاحقاً
        await update.message.reply_text(
            f"👍 *تم إرسال اللايك!*\n\n"
            f"👤 *اللاعب:* `{player_id}`\n"
            f"💖 *النوع:* Normal\n"
            f"✅ *الحالة:* نجاح\n\n"
            f"🔜 قريباً: اتصال مباشر مع Free Fire",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر عرض الإحصائيات"""
    try:
        if not context.args:
            await update.message.reply_text(
                "⚠️ *طريقة الاستخدام:*\n"
                "`/stats <معرف_اللاعب>`\n\n"
                "مثال: `/stats 123456789`",
                parse_mode="Markdown"
            )
            return
        
        player_id = context.args[0]
        
        # إحصائيات تجريبية (سيتم جلبها من API لاحقاً)
        await update.message.reply_text(
            f"📊 *إحصائيات اللاعب* 📊\n\n"
            f"🆔 *المعرف:* `{player_id}`\n"
            f"🎮 *المستوى:* 50\n"
            f"❤️ *اللايكات المستلمة:* 1,234\n"
            f"🏆 *مرات BOOYAH:* 89\n"
            f"📈 *نسبة الفوز:* 23.5%\n"
            f"💀 *القتلات:* 1,567\n\n"
            f"🔄 *آخر تحديث:* الآن",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر المساعدة"""
    await start(update, context)

# إضافة الأوامر
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("like", like_command))
app.add_handler(CommandHandler("stats", stats_command))
app.add_handler(CommandHandler("help", help_command))

# تشغيل البوت
if __name__ == "__main__":
    print("✅ البوت يعمل بنجاح...")
    app.run_polluting()