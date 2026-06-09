import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from websocket_handler import FreeFireWebSocket
from crypto_utils import AESCipher
import config

# تهيئة البوت
app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

# تهيئة WebSocket
ff_ws = FreeFireWebSocket()

# تهيئة التشفير
cipher = AESCipher(config.AES_KEY)

@app.post_init
async def init_websocket():
    """تشغيل WebSocket عند بداية البوت"""
    await ff_ws.connect(config.FF_API_KEY)

async def like_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /like <id> <type>"""
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("⚠️ استخدم: /like <player_id> <normal/me/clap>")
            return
        
        player_id = args[0]
        like_type = args[1] if len(args) > 1 else "normal"
        
        # إرسال لايك عن طريق WebSocket
        result = await ff_ws.send_like(player_id)
        
        if result:
            await update.message.reply_text(f"✅ تم إرسال {like_type} لايك للاعب {player_id}")
        else:
            await update.message.reply_text("❌ فشل إرسال اللايك")
            
    except Exception as e:
        await update.message.reply_text(f"⚠️ خطأ: {e}")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /stats <id>"""
    try:
        player_id = context.args[0]
        stats = await ff_ws.get_player_stats(player_id)
        
        if stats:
            msg = f"""
📊 *إحصائيات اللاعب {player_id}*
🎮 المستوى: {stats.get('level', 'N/A')}
❤️ اللايكات المستلمة: {stats.get('likes_received', 0)}
🏆 عدد مرات BOOYAH: {stats.get('booyah_count', 0)}
"""
            await update.message.reply_text(msg, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ لم يتم العثور على اللاعب")
            
    except Exception as e:
        await update.message.reply_text(f"⚠️ خطأ: {e}")

# إضافة الأوامر
app.add_handler(CommandHandler("like", like_command))
app.add_handler(CommandHandler("stats", stats_command))

if __name__ == "__main__":
    print("🚀 تشغيل البوت...")
    app.run_polluting()