from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import cohere
import os

# Your tokens here
TELEGRAM_TOKEN = "7835527307:AAGfZSW4wN2_gHo4QRmeL089bEIDNH1ZYG0"
COHERE_API_KEY = "MsrH0XVMBeSYwXxVyXMjfWlMwZdLajVGmPrmnoLP"

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello! I am an AI-powered bot using Cohere. Ask me anything!'
    )

# Handle user messages with Cohere LLM
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Show typing indicator
    await update.message.chat.send_action(action="typing")
    
    try:
        # Call Cohere API
        response = co.chat(
            message=user_message,
            model="command-a-03-2025",  # You can use "command", "command-light", or "command-r-plus"
            temperature=0.7,
            max_tokens=500
        )
        
        # Get the response text
        bot_reply = response.text
        
        # Send reply to user
        await update.message.reply_text(bot_reply)
        
    except Exception as e:
        await update.message.reply_text(
            f"Sorry, I encountered an error: {str(e)}"
        )

def main():
    # Create application
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()