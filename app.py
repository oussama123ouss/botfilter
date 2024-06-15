import telebot
from telebot import types
from PIL import Image, ImageFilter
import requests
from io import BytesIO

# Replace "YOUR_BOT_API_TOKEN" with your actual bot API token
bot = telebot.TeleBot("6987466658:AAEWjl7aoa_LSqQSx0s4REM5gyT6vUz_6sc")

# Filter URLs
filter_urls = {
    "الفلتر 1": "https://drive.google.com/uc?export=download&id=14S6bx7deeUyqdcDSwFWQH3iOIhkAUEJ5",
    "الفلتر 2": "https://drive.google.com/uc?export=download&id=14S6c4TiDBbU87HvPOr8yxG0ePdp9dsCC",
    "الفلتر 3": "https://drive.google.com/uc?export=download&id=14fmZrMoIzNp3YBVP21vMKcGxum150-Uf",
    "الفلتر 4": "https://drive.google.com/uc?export=download&id=14nDCF8zHKChe6lfqNp-2MlvjvHni9WYD",
    "الفلتر 5": "https://drive.google.com/uc?export=download&id=14Pdw8K_ndshzC9F9V4hqSYyOE82apdwV"
}

# Function to apply filter to an image
def apply_filter(image_url, filter_name):
    try:
        # Download the image
        response = requests.get(image_url)
        image_bytes = BytesIO(response.content)
        image = Image.open(image_bytes)
        
        # Apply the selected filter
        if filter_name == "الفلتر 1":
            filtered_image = image.filter(ImageFilter.BLUR)
        elif filter_name == "الفلتر 2":
            filtered_image = image.filter(ImageFilter.CONTOUR)
        elif filter_name == "الفلتر 3":
            filtered_image = image.filter(ImageFilter.EMBOSS)
        elif filter_name == "الفلتر 4":
            filtered_image = image.filter(ImageFilter.SHARPEN)
        elif filter_name == "الفلتر 5":
            filtered_image = image.filter(ImageFilter.SMOOTH)
        else:
            return None  # Invalid filter name
        
        # Save the filtered image to bytes
        output_buffer = BytesIO()
        filtered_image.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        
        return output_buffer
    
    except Exception as e:
        print(f"Error applying filter: {e}")
        return None

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create a button linking to the Telegram channel
    channel_button = types.InlineKeyboardMarkup()
    channel_button.add(types.InlineKeyboardButton("تابعني على تلغرام", url="https://t.me/elkhabur"))
    
    # Send welcome message with the button
    bot.send_message(message.chat.id, 
                     "مرحبا عزيزي  👋\n\n"
                     "أرسل الصورة المراد تطبيق فلاتر عليها\n\n"
                     "الصيغ المدعومة (PNG, JPG, HEIC)\n\n"
                     "و يكون أسفل الرسالة زر مكتوب عليه تابعني ويؤدي إلى رابط قناتي:\n"
                     "https://t.me/elkhabur", reply_markup=channel_button)

# Handler for receiving images
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Ask user to select a filter
        filter_keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [types.InlineKeyboardButton(filter_name, callback_data=filter_name) for filter_name in filter_urls]
        filter_keyboard.add(*buttons)
        
        bot.send_message(message.chat.id, "اختر أحد الفلاتر التالية لتطبيقها على الصورة:", reply_markup=filter_keyboard)
    
    except Exception as e:
        print(f"Error handling photo: {e}")

# Handler for callback queries (filter selection)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        # Get the chosen filter and original photo
        filter_name = call.data
        photo = call.message.photo[-1]
        photo_url = f"https://api.telegram.org/file/bot{bot.token}/{bot.get_file(photo.file_id).file_path}"
        
        # Apply the filter
        filtered_image = apply_filter(photo_url, filter_name)
        
        if filtered_image:
            bot.send_photo(call.message.chat.id, filtered_image)
        else:
            bot.send_message(call.message.chat.id, "خطأ في تطبيق الفلتر. الرجاء المحاولة مرة أخرى.")
        
        # Delete the message prompting the user to select a filter
        bot.delete_message(call.message.chat.id, call.message.message_id)
    
    except Exception as e:
        print(f"Error handling callback query: {e}")

# Start polling
bot.polling()