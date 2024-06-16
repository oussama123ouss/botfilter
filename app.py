import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Replace "YOUR_BOT_API_TOKEN" with your actual bot API token
bot = telebot.TeleBot("6987466658:AAEWjl7aoa_LSqQSx0s4REM5gyT6vUz_6sc")

# Load the filters
filter_urls = {
    "فلتر رقم 1": "https://drive.google.com/uc?export=download&id=14S6bx7deeUyqdcDSwFWQH3iOIhkAUEJ5",
    "فلتر رقم 2": "https://drive.google.com/uc?export=download&id=14S6c4TiDBbU87HvPOr8yxG0ePdp9dsCC",
    "فلتر رقم 3": "https://drive.google.com/uc?export=download&id=14fmZrMoIzNp3YBVP21vMKcGxum150-Uf",
    "فلتر رقم 4": "https://drive.google.com/uc?export=download&id=14nDCF8zHKChe6lfqNp-2MlvjvHni9WYD",
    "فلتر رقم 5": "https://drive.google.com/uc?export=download&id=14Pdw8K_ndshzC9F9V4hqSYyOE82apdwV"
}

filters = {}
for name, url in filter_urls.items():
    response = requests.get(url)
    filter_image = Image.open(BytesIO(response.content)).convert("RGBA")
    filters[name] = filter_image

# Function to apply filter to an image
def apply_filter_to_image(image, filter_image):
    filter_image = filter_image.resize(image.size)
    return Image.alpha_composite(image.convert("RGBA"), filter_image)

# Dictionary to store user images
user_images = {}

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 
                     "أهلاً بك!\n"
                     "قم بإرسال صورة وسنقوم بإضافة الفلتر الذي تختاره.\n"
                     "اختر أحد الفلاتر بعد إرسال الصورة.")

# Handler for photo messages
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image = Image.open(BytesIO(downloaded_file))
    user_images[message.chat.id] = image

    filter_keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(name, callback_data=name) for name in filter_urls]
    
    for i in range(0, len(buttons), 3):
        filter_keyboard.add(*buttons[i:i + 3])

    bot.send_message(message.chat.id, "اختر أحد الفلاتر التالية:", reply_markup=filter_keyboard)

# Handler for callback queries
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.message.chat.id
    if user_id in user_images:
        user_image = user_images[user_id]
        filter_name = call.data
        filter_image = filters.get(filter_name)
        if filter_image:
            filtered_image = apply_filter_to_image(user_image, filter_image)
            output_buffer = BytesIO()
            filtered_image.save(output_buffer, format='PNG')
            output_buffer.seek(0)
            bot.send_photo(user_id, output_buffer, caption=f"تم تطبيق {filter_name} على صورتك.")
        else:
            bot.send_message(user_id, "خطأ في تطبيق الفلتر. الرجاء المحاولة مرة أخرى.")
    else:
        bot.send_message(user_id, "لم يتم العثور على صورة. الرجاء إرسال صورة أولاً.")

# Start polling
bot.polling()
