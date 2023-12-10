"""
Simple Calculator Bot.
It can add, subtract, multiply and divide
"""

#for logging errors on dev terminal
import logger

#for loading api_key from .env file
import os
from dotenv import load_dotenv 

#all necessary libraries to communicate with the bot
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

#bot functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the conversation"""

    await update.message.reply_text(
        "Hi! I am a Calculator Bot. I can perform Simple Calculations. "
        "Send /cancel to stop talking to me.\n\n"
        "Send /calc to see available operations.",
    )

    return None


async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provides Operations Available"""

    await update.message.reply_text(
        "Select Operation to perform\n"
        "/add - Addition\n"
        "/sub - Subtraction\n"
        "/mul - Multiply\n"
        "/div - Divide\n\n"
        "Select command and follow it up with the numbers.\n"
        "Example - /add 100 200",
    )

    return None


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Addition Operation"""
    text = update.message.text
    text = text.split()
    num1, num2 = int(text[-2]), int(text[-1])
    await update.message.reply_text(
        f"{num1} + {num2} = {num1+num2}"
    )

    return None

async def sub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Subtraction Operation"""
    text = update.message.text
    text = text.split()
    num1, num2 = int(text[-2]), int(text[-1])
    await update.message.reply_text(
        f"{num1} - {num2} = {num1-num2}"
    )

    return None

async def mul(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Multiplication Operation"""
    text = update.message.text
    text = text.split()
    num1, num2 = int(text[-2]), int(text[-1])
    await update.message.reply_text(
        f"{num1} x {num2} = {num1*num2}"
    )

    return None

async def div(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Division Operation"""
    text = update.message.text
    text = text.split()
    num1, num2 = int(text[-2]), int(text[-1])
    await update.message.reply_text(
        f"{num1} ÷ {num2} = {num1/num2}"
    )

    return None


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Bye!"
    )

    return ConversationHandler.END

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handle any errors in the handlers"""
    logger.error("Exception while handling an update:", exc_info=context.error)

    user = update.message.from_user

    await update.message.reply_text(
        f"An error occured! Please try again."
    )
    
async def bad_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Raise an error to trigger the error handler."""
    await context.bot.wrong_method_name()
    

def main() -> None:
    """Run the bot."""

    # Get api_key from env file
    load_dotenv()
    api_key = os.getenv('API_KEY')

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(api_key).build()

    #adding handlers to the bot
    application.add_handler(CommandHandler("start", start))


    application.add_handler(CommandHandler("calc", calc))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("sub", sub))
    application.add_handler(CommandHandler("mul", mul))
    application.add_handler(CommandHandler("div", div))
    application.add_handler(CommandHandler("bad_command", bad_command))
    application.add_handler(CommandHandler("cancel", cancel))

    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()