import telebot
import config
from PIL import Image
import io
from my_azure_ai_functions import analyze_receipts

# Get the token from config
token = config.TOKEN

# Create a bot instance
bot = telebot.TeleBot(token)

# List of allowed user IDs or chat IDs
ALLOWED_USERS = [config.MY_USER_ID]  # Replace with actual user IDs
ALLOWED_CHATS = []  # Replace with actual chat IDs

def is_authorized(message):
    """Check if the user or chat is authorized to use the bot"""
    return (message.from_user.id in ALLOWED_USERS) or (message.chat.id in ALLOWED_CHATS)


@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    if is_authorized(message):
        # Get the file ID of the largest version of the image
        file_id = message.photo[-1].file_id
        
        # Get file info and download the file
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Process the image using Azure AI
        receipt_text = analyze_receipts(io.BytesIO(downloaded_file))
        
        # Send a message with the extracted text
        bot.reply_to(message, f"Extracted text from receipt:\n{receipt_text}")
        

# Start the bot
if __name__ == '__main__':
    print("Bot is running...")
    bot.polling()