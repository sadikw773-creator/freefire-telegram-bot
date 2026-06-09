FROM python:3.11-slim

WORKDIR /app

# نسخ ملف المتطلبات من مجلد FreeFireBot
COPY FreeFireBot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملف البوت من مجلد FreeFireBot
COPY FreeFireBot/bot.py .

# تشغيل البوت
CMD ["python", "bot.py"]