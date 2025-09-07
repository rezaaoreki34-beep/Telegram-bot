import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Ambil token dari Railway Variables
TOKEN = os.getenv("TOKEN")

def cek_bocor(email):
    url = f"https://scylla.sh/search?q={email}&type=email"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if not data:
                return f"✅ Email {email} aman, tidak ditemukan di database Scylla."
            return f"⚠️ Email {email} ditemukan di database Scylla! Data: {data[:2]}"
        else:
            return f"❌ Error {response.status_code} dari server Scylla."
    except Exception as e:
        return f"🔥 Terjadi error: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! 👋\nKetik /cek email@example.com untuk cek kebocoran."
    )

async def cek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gunakan format: /cek email@example.com")
        return
    email = context.args[0]
    hasil = cek_bocor(email)
    await update.message.reply_text(hasil)

def main():
    print("🤖 Bot sedang berjalan...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cek", cek))
    app.run_polling()

if __name__ == "__main__":
    main()

