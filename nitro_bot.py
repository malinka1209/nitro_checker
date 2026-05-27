#!/usr/bin/env python3
import string
import random
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest

# ТОКЕН ПРЯМО В КОДЕ
BOT_TOKEN = "8673579718:AAH4_wcNYWKmdnrQ5rFrkYZ8gkhjaAkrUao"


class NitroBot:
    def __init__(self):
        self.running = False
        self.valid_codes = []
        self.invalid_count = 0
        self.total_checked = 0
        self.chars = string.ascii_letters + string.digits

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🎮 **Discord Nitro Generator Bot**\n\n"
            "📌 **Команды:**\n"
            "/gen N - начать генерацию\n"
            "/stop - остановить\n"
            "/status - статистика\n"
            "/codes - показать коды\n"
            "/clear - очистить список",
            parse_mode='Markdown'
        )

    async def generate(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.running:
            await update.message.reply_text("⚠️ Уже работаю! /stop")
            return

        if not context.args:
            await update.message.reply_text("❌ /gen 100")
            return

        try:
            num = int(context.args[0])
            if num <= 0:
                await update.message.reply_text("❌ Число > 0")
                return
        except:
            await update.message.reply_text("❌ Введи число!")
            return

        self.running = True
        self.valid_codes = []
        self.invalid_count = 0
        self.total_checked = 0

        msg = await update.message.reply_text(f"🚀 Запущено: {num} кодов")

        for i in range(num):
            if not self.running:
                break

            code = ''.join(random.choices(self.chars, k=16))
            full = f"https://discord.gift/{code}"
            self.total_checked += 1

            if await self.check(code):
                self.valid_codes.append(full)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"🎉 **ВАЛИДНЫЙ КОД!**\n`{full}`",
                    parse_mode='Markdown'
                )
            else:
                self.invalid_count += 1

            if (i + 1) % 100 == 0 or (i + 1) == num:
                await msg.edit_text(f"🔄 {i + 1}/{num} | Найдено: {len(self.valid_codes)}")

            await asyncio.sleep(0.05)

        self.running = False
        await update.message.reply_text(f"✅ Готово! Найдено: {len(self.valid_codes)}")

    async def check(self, code: str) -> bool:
        url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}"
        try:
            r = requests.get(url, timeout=5)
            return r.status_code == 200
        except:
            return False

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.running = False
        await update.message.reply_text("🛑 Остановлено!")

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            f"📊 Статус: {'🟢 Работаю' if self.running else '🔴 Остановлен'}\n"
            f"✅ Валидных: {len(self.valid_codes)}\n"
            f"❌ Невалидных: {self.invalid_count}"
        )

    async def codes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.valid_codes:
            await update.message.reply_text("📭 Нет кодов")
            return
        for code in self.valid_codes:
            await update.message.reply_text(code)
            await asyncio.sleep(0.1)

    async def clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.running:
            await update.message.reply_text("⚠️ Сначала /stop")
            return
        count = len(self.valid_codes)
        self.valid_codes = []
        self.invalid_count = 0
        self.total_checked = 0
        await update.message.reply_text(f"🗑️ Очищено {count} кодов")


def main():
    request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
        http_version='1.1'
    )
    app = ApplicationBuilder().token(BOT_TOKEN).request(request).build()

    bot = NitroBot()
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CommandHandler("gen", bot.generate))
    app.add_handler(CommandHandler("stop", bot.stop))
    app.add_handler(CommandHandler("status", bot.status))
    app.add_handler(CommandHandler("codes", bot.codes))
    app.add_handler(CommandHandler("clear", bot.clear))

    print("✅ Бот запущен!")
    print(f"🤖 Имя бота: @nitrougadaycakkbot")
    print("📋 Команды: /gen, /stop, /status, /codes, /clear")

    app.run_polling()


if __name__ == "__main__":
    main()