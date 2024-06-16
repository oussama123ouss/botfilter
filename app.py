import telebot
from telebot import types
from PIL import Image
import requests
from io import BytesIO
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Replace "YOUR_BOT_API_TOKEN" with your actual bot API token
BOT_TOKEN = "6987466658:AAEWjl7aoa_LSqQSx0s4REM5gyT6vUz_6sc"

logger.info(f"Bot API token found: {BOT_TOKEN[:5]}...")  # Print part of the token for verification

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Filter URLs
filter_urls = {
    "فلتر رقم 1": "https://drive.google.com/uc?export=download&id=14S6bx7deeUyqdcDSwFWQH3iOIhkAUEJ5",
    "فلتر رقم 2": "https://drive.google.com/uc?export=download&id=14S6c4TiDBbU87HvPOr8yxG0ePdp9dsCC",
    "فلتر رقم 3": "https://drive.google.com/uc?export=download&id=14fmZrMoIzNp3YBVP21vMKcGxum150-Uf",
    "فلتر رقم 4": "https://drive.google.com/uc?export=download&id=14nDCF8zHKChe6lfqNp-2MlvjvHni9WYD",
    "فلتر رقم 5": "https://drive.google.com/uc?export=download&id=14Pdw8K_ndshzC9F9V4hqSYyOE82apdwV"
}

# Function to apply a filter to an image
def apply_filter(image, filter_id):
    filter_url = filter_urls[filter_id]
    filter_image_bytes = requests.get(filter_url).content
    filter_image = Image.open(BytesIO(filter_image_bytes)).convert("RGBA")

    # Resize filter image to match the input image size
    filter_image = filter_image.resize(image.size)

    # Apply the filter (overlay with transparency)
    combined_image = Image.alpha_composite(image.convert("RGBA"), filter_image)

    # Save the modified image
    output_buffer = BytesIO()
    combined_image.save(output_buffer, format='PNG')
    output_buffer.seek(0)
    
    return output_buffer

# Dictionary to store user photos
user_photos = {}

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "أهلاً بك! أرسل صورة ليتم تطبيق الفلتر عليها.")

# Handler for photo messages
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_bytes = requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}').content

    user_photos[message.chat.id] = Image.open(BytesIO(file_bytes))
    
    filter_keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(filter_name, callback_data=filter_name) for filter_name in filter_urls]
    
    for i in range(0, len(buttons), 2):
        filter_keyboard.add(*buttons[i:i + 2])
    
    bot.send_message(message.chat.id, "اختر فلتر لتطبيقه على الصورة:", reply_markup=filter_keyboard)

# Handler for callback queries
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.message.chat.id
    filter_id = call.data

    if user_id in user_photos:
        image = user_photos[user_id]
        filtered_image = apply_filter(image, filter_id)
        
        if filtered_image:
            bot.send_photo(user_id, filtered_image, caption="🤩 تم تطبيق الفلتر على صورتك!")
        else:
            bot.send_message(user_id, "خطأ في تطبيق الفلتر. الرجاء المحاولة مرة أخرى.")
        
        del user_photos[user_id]  # Remove the image from memory
    else:
        bot.send_message(user_id, "لم أتمكن من العثور على صورتك. الرجاء إرسال الصورة مرة أخرى.")
    
    # Delete the message prompting the user to choose a filter
    try:
        bot.delete_message(user_id, call.message.message_id)
    except telebot.apihelper.ApiTelegramException as e:
        logger.error(f"Error deleting message: {e}")

# Start polling
try:
    bot.polling()
except Exception as e:
    logger.error(f"Error in bot.polling: {e}")
