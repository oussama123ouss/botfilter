import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from PIL import Image, ImageEnhance
import io

# API Key
API_KEY = '6987466658:AAEWjl7aoa_LSqQSx0s4REM5gyT6vUz_6sc'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("مرحباً! أرسل صورة لتطبيق الفلاتر عليها.")

def apply_filter(image: Image.Image, filter_name: str) -> Image.Image:
    if filter_name == 'Mocha':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)  # زيادة التشبع بنسبة 30%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)  # زيادة التباين بنسبة 20%

        r, g, b = image.split()
        r = r.point(lambda i: i * 1.2)
        g = g.point(lambda i: i * 1.1)
        image = Image.merge('RGB', (r, g, b))

        return image

    elif filter_name == 'Blue Film':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.7)  # تقليل التشبع بنسبة 30%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # زيادة التباين بنسبة 50%

        return image
    
    elif filter_name == 'Iron':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)  # زيادة التشبع بنسبة 10%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)  # زيادة التباين بنسبة 30%

        return image
    
    elif filter_name == 'The Darkest H':
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.6)  # تقليل السطوع بنسبة 40%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.8)  # زيادة التباين بنسبة 80%

        return image
    
    elif filter_name == 'iPhone 14 Pro':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.5)  # زيادة التشبع بنسبة 50%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.4)  # زيادة التباين بنسبة 40%

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)  # زيادة السطوع بنسبة 20%

        return image

    elif filter_name == 'Shades of Wat...':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.8)  # تقليل التشبع بنسبة 20%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)  # زيادة التباين بنسبة 20%

        return image

    elif filter_name == 'Top Gun Mave...':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)  # زيادة التشبع بنسبة 10%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # زيادة التباين بنسبة 50%

        return image

    elif filter_name == 'Black Tone':
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)  # زيادة التباين بنسبة 30%

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.7)  # تقليل السطوع بنسبة 30%

        return image

    elif filter_name == 'Retro Fashion':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.9)  # تقليل التشبع بنسبة 10%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)  # زيادة التباين بنسبة 30%

        return image

    elif filter_name == 'Cinematic':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)  # زيادة التشبع بنسبة 20%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # زيادة التباين بنسبة 50%

        return image

    elif filter_name == 'filmlook':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)  # زيادة التشبع بنسبة 10%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.4)  # زيادة التباين بنسبة 40%

        return image

    elif filter_name == 'CINEMA':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)  # زيادة التشبع بنسبة 30%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # زيادة التباين بنسبة 50%

        return image

    elif filter_name == 'Ahmed Ali':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.0)  # بدون تغيير في التشبع

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)  # زيادة التباين بنسبة 20%

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.1)  # زيادة السطوع بنسبة 10%

        return image

    elif filter_name == 'Orange tea':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.5)  # زيادة التشبع بنسبة 50%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)  # زيادة التباين بنسبة 30%

        return image

    elif filter_name == 'Anime':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)  # زيادة التشبع بنسبة 20%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # زيادة التباين بنسبة 50%

        return image

    elif filter_name == 'Estetic':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)  # زيادة التشبع بنسبة 10%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)  # زيادة التباين بنسبة 20%

        return image

    elif filter_name == 'ProPortrait':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)  # زيادة التشبع بنسبة 30%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # زيادة التباين بنسبة 50%

        return image

    elif filter_name == 'iPhone 15 pro':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.4)  # زيادة التشبع بنسبة 40%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)  # زيادة التباين بنسبة 30%

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)  # زيادة السطوع بنسبة 20%

        return image

    elif filter_name == 'Vivi':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)  # زيادة التشبع بنسبة 20%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.4)  # زيادة التباين بنسبة 40%

        return image

    elif filter_name == 'CineStyle':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)  # زيادة التشبع بنسبة 30%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # زيادة التباين بنسبة 50%

        return image

    elif filter_name == 'Sam Kolder':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)  # زيادة التشبع بنسبة 10%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)  # زيادة التباين بنسبة 30%

        return image

    elif filter_name == 'Bright Sky':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.4)  # زيادة التشبع بنسبة 40%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)  # زيادة التباين بنسبة 20%

        return image

    elif filter_name == 'Dark 2024':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.8)  # تقليل التشبع بنسبة 20%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # زيادة التباين بنسبة 50%

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.7)  # تقليل السطوع بنسبة 30%

        return image

    elif filter_name == '16-3-':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)  # زيادة التشبع بنسبة 20%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)  # زيادة التباين بنسبة 30%

        return image

    elif filter_name == 'Cinematic Night':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.5)  # زيادة التشبع بنسبة 50%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.4)  # زيادة التباين بنسبة 40%

        return image

    elif filter_name == 'Deep Fall':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)  # زيادة التشبع بنسبة 10%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.4)  # زيادة التباين بنسبة 40%

        return image

    elif filter_name == 'Blue Lake':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)  # زيادة التشبع بنسبة 20%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)  # زيادة التباين بنسبة 30%

        return image

    elif filter_name == 'Smooth Face':
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(0.5)  # تقليل الحدة بنسبة 50%

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.1)  # زيادة السطوع بنسبة 10%

        return image

    else:
        return image

def send_filters_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Mocha", callback_data='Mocha')],
        [InlineKeyboardButton("Shades of Wat...", callback_data='Shades of Wat...')],
        [InlineKeyboardButton("Blue Film", callback_data='Blue Film')],
        [InlineKeyboardButton("Iron", callback_data='Iron')],
        [InlineKeyboardButton("The Darkest H", callback_data='The Darkest H')],
        [InlineKeyboardButton("iPhone 14 Pro", callback_data='iPhone 14 Pro')],
        [InlineKeyboardButton("Top Gun Mave...", callback_data='Top Gun Mave...')],
        [InlineKeyboardButton("Black Tone", callback_data='Black Tone')],
        [InlineKeyboardButton("Retro Fashion", callback_data='Retro Fashion')],
        [InlineKeyboardButton("Cinematic", callback_data='Cinematic')],
        [InlineKeyboardButton("filmlook", callback_data='filmlook')],
        [InlineKeyboardButton("CINEMA", callback_data='CINEMA')],
        [InlineKeyboardButton("Ahmed Ali", callback_data='Ahmed Ali')],
        [InlineKeyboardButton("Orange tea", callback_data='Orange tea')],
        [InlineKeyboardButton("Anime", callback_data='Anime')],
        [InlineKeyboardButton("Estetic", callback_data='Estetic')],
        [InlineKeyboardButton("ProPortrait", callback_data='ProPortrait')],
        [InlineKeyboardButton("iPhone 15 pro", callback_data='iPhone 15 pro')],
        [InlineKeyboardButton("Vivi", callback_data='Vivi')],
        [InlineKeyboardButton("CineStyle", callback_data='CineStyle')],
        [InlineKeyboardButton("Sam Kolder", callback_data='Sam Kolder')],
        [InlineKeyboardButton("Bright Sky", callback_data='Bright Sky')],
        [InlineKeyboardButton("Dark 2024", callback_data='Dark 2024')],
        [InlineKeyboardButton("16-3-", callback_data='16-3-')],
        [InlineKeyboardButton("Cinematic Night", callback_data='Cinematic Night')],
        [InlineKeyboardButton("Deep Fall", callback_data='Deep Fall')],
        [InlineKeyboardButton("Blue Lake", callback_data='Blue Lake')],
        [InlineKeyboardButton("Smooth Face", callback_data='Smooth Face')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('اختر أحد الفلاتر الآتية:', reply_markup=reply_markup)

def handle_image(update: Update, context: CallbackContext) -> None:
    context.user_data['image'] = update.message.photo[-1].get_file().download_as_bytearray()
    send_filters_keyboard(update, context)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    filter_name = query.data
    image_data = context.user_data['image']
    image = Image.open(io.BytesIO(image_data))

    filtered_image = apply_filter(image, filter_name)

    bio = io.BytesIO()
    bio.name = 'image.png'
    filtered_image.save(bio, 'PNG')
    bio.seek(0)

    query.message.reply_photo(photo=bio, caption=f"Filter name: {filter_name}\nتمت إضافة التأثير بنجاح.")

def main() -> None:
    updater = Updater(API_KEY)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
