import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📰 ثبت خبر", callback_data="news")],
        [InlineKeyboardButton("🖼️ ساخت کاور", callback_data="cover")],
        [InlineKeyboardButton("📊 عملکرد شهرداری", callback_data="performance")],
    ]

    await update.message.reply_text(
        "سلام 👋\n"
        "به سامانه اخبار و عملکرد شهرداری میاندوآب خوش آمدید.\n\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "news":
        await query.message.reply_text(
            "📰 ثبت خبر\n\n"
            "لطفاً عکس پروژه را ارسال کنید."
        )

    elif query.data == "cover":
        await query.message.reply_text(
            "🖼️ ساخت کاور\n\n"
            "لطفاً عکس پروژه را ارسال کنید."
        )

    elif query.data == "performance":
        keyboard = [
            [InlineKeyboardButton("🏗️ عمرانی", callback_data="civil")],
            [InlineKeyboardButton("🧹 خدمات شهری", callback_data="services")],
            [InlineKeyboardButton("🌳 فضای سبز", callback_data="green")],
            [InlineKeyboardButton("🎨 زیباسازی", callback_data="beauty")],
            [InlineKeyboardButton("🪦 آرامستان", callback_data="cemetery")],
            [InlineKeyboardButton("📰 روابط عمومی", callback_data="public_relations")],
        ]

        await query.message.reply_text(
            "📊 عملکرد شهرداری\n\n"
            "دسته‌بندی مورد نظر را انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    else:
        categories = {
            "civil": "عمرانی",
            "services": "خدمات شهری",
            "green": "فضای سبز",
            "beauty": "زیباسازی",
            "cemetery": "آرامستان",
            "public_relations": "روابط عمومی",
        }

        category = categories.get(query.data)

        if category:
            context.user_data["category"] = category

            await query.message.reply_text(
                f"✅ دسته‌بندی انتخاب شد:\n\n"
                f"📊 {category}\n\n"
                f"حالا عنوان خبر را ارسال کنید."
            )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if context.user_data.get("category"):
        context.user_data["title"] = text

        await update.message.reply_text(
            "✅ عنوان دریافت شد:\n\n"
            f"📝 {text}\n\n"
            "در نسخه بعدی، چکیده خبر بر اساس عنوان به‌صورت خودکار تولید خواهد شد."
        )
    else:
        await update.message.reply_text(
            "برای شروع، دستور /start را بزنید."
        )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📷 عکس دریافت شد.\n\n"
        "در نسخه بعدی، عکس به‌صورت خودکار در سایز 1080×1350 آماده می‌شود "
        "و کاور PNG روی آن قرار خواهد گرفت."
    )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده است.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
