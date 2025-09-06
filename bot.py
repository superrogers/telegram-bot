from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ---- STEP 1: Bot Token ----
BOT_TOKEN = "8138993256:AAEG-2jqRM5WHj2kwj9VMcNcwua9XOl4X14"

# ---- STEP 2: User data temporary storage ----
user_data = {}

# ---- STEP 3: /start command ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_data[chat_id] = {}
    await update.message.reply_text("Welcome! Please enter your Name:")

# ---- STEP 4: Collect user details ----
async def collect_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text

    if chat_id not in user_data:
        user_data[chat_id] = {}

    if "name" not in user_data[chat_id]:
        user_data[chat_id]["name"] = text
        await update.message.reply_text("Got it ✅ Now enter your Branch:")
    elif "branch" not in user_data[chat_id]:
        user_data[chat_id]["branch"] = text
        await update.message.reply_text("Nice 👍 Now enter your College:")
    elif "college" not in user_data[chat_id]:
        user_data[chat_id]["college"] = text
        await update.message.reply_text("Great! Finally enter your Email:")
    elif "email" not in user_data[chat_id]:
        user_data[chat_id]["email"] = text
        details = user_data[chat_id]

        # Razorpay Payment Button
        keyboard = [
            [InlineKeyboardButton("Pay Now 💳", url="https://rzp.io/rzp/W4JTqq3F")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        msg = (
            f"✅ Details saved:\n\n"
            f"Name: {details['name']}\n"
            f"Branch: {details['branch']}\n"
            f"College: {details['college']}\n"
            f"Email: {details['email']}\n\n"
            "👉 Complete your payment by clicking the button below:"
        )

        await update.message.reply_text(msg, reply_markup=reply_markup)

# ---- STEP 5: Main function ----
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_data))
    app.run_polling()

if __name__ == "__main__":
    main()