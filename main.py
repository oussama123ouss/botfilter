import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from PIL import Image, ImageEnhance, ImageFilter
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
        # تأثير مشابه لتأثير Pine
        # 1. زياده التباين
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)  # زيادة التباين بنسبة 20%

        # 2. زياده التشبع
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)  # زيادة التشبع بنسبة 20%

        # 3. تفتيح الصورة قليلاً
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.1)  # زيادة السطوع بنسبة 10%

        return image
    elif filter_name == 'Shades of Wat...':
        return image.filter(ImageFilter.GaussianBlur(5))
    elif filter_name == 'Blue Film':
        r, g, b = image.split()
        r = r.point(lambda i: i * 0.5)
        return Image.merge('RGB', (r, g, b))
    elif filter_name == 'Iron':
        return image.filter(ImageFilter.EDGE_ENHANCE)
    elif filter_name == 'The Darkest H...':
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(0.5)
    elif filter_name == 'iPhone 14 Pro':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.5)  # زيادة التشبع بنسبة 50%
        return image
    elif filter_name == 'Top Gun Mave...':
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(1.5)
    elif filter_name == 'Black Tone':
        return image.convert('1')
    elif filter_name == 'Retro Fashion':
        return image.filter(ImageFilter.SMOOTH)
    elif filter_name == 'Cinematic':
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2.0)
    elif filter_name == 'filmlook':
        return image.filter(ImageFilter.SHARPEN)
    elif filter_name == 'CINEMA':
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(2.0)
    elif filter_name == 'Ahmed Ali':
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(1.2)
    elif filter_name == 'Orange teal':
        r, g, b = image.split()
        r = r.point(lambda i: i * 1.5)
        b = b.point(lambda i: i * 0.5)
        return Image.merge('RGB', (r, g, b))
    elif filter_name == 'Anime':
        return image.filter(ImageFilter.CONTOUR)
    elif filter_name == 'Estetic':
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(1.2)
    elif filter_name == 'ProPortrait':
        return image.filter(ImageFilter.BLUR)
    elif filter_name == 'iPhone 15 pro':
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(1.8)
    elif filter_name == 'Vivi':
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(1.8)
    elif filter_name == 'CineStyle':
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(0.7)
    elif filter_name == 'Sam Kolder':
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(2.5)
    elif filter_name == 'Bright Sky':
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(1.5)
    elif filter_name == 'Dark 2024':
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(0.3)
    elif filter_name == 'Cinematic Night':
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2.5)
    elif filter_name == 'Deep Fall':
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(0.5)
    elif filter_name == 'Blue Lake':
        r, g, b = image.split()
        b = b.point(lambda i: i * 1.5)
        return Image.merge('RGB', (r, g, b))
    elif filter_name == 'Smooth Face':
        return image.filter(ImageFilter.SMOOTH_MORE)
    else:
        return image

def send_filters_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Mocha", callback_data='Mocha'), InlineKeyboardButton("Shades of Wat...", callback_data='Shades of Wat...')],
        [InlineKeyboardButton("Blue Film", callback_data='Blue Film'), InlineKeyboardButton("Iron", callback_data='Iron')],
        [InlineKeyboardButton("The Darkest H...", callback_data='The Darkest H...'), InlineKeyboardButton("iPhone 14 Pro", callback_data='iPhone 14 Pro')],
        [InlineKeyboardButton("Top Gun Mave...", callback_data='Top Gun Mave...'), InlineKeyboardButton("Black Tone", callback_data='Black Tone')],
        [InlineKeyboardButton("Retro Fashion", callback_data='Retro Fashion'), InlineKeyboardButton("Cinematic", callback_data='Cinematic')],
        [InlineKeyboardButton("filmlook", callback_data='filmlook'), InlineKeyboardButton("CINEMA", callback_data='CINEMA')],
        [InlineKeyboardButton("Ahmed Ali", callback_data='Ahmed Ali'), InlineKeyboardButton("Orange teal", callback_data='Orange teal')],
        [InlineKeyboardButton("Anime", callback_data='Anime'), InlineKeyboardButton("Estetic", callback_data='Estetic')],
        [InlineKeyboardButton("ProPortrait", callback_data='ProPortrait'), InlineKeyboardButton("iPhone 15 pro", callback_data='iPhone 15 pro')],
        [InlineKeyboardButton("Vivi", callback_data='Vivi'), InlineKeyboardButton("CineStyle", callback_data='CineStyle')],
        [InlineKeyboardButton("Sam Kolder", callback_data='Sam Kolder'), InlineKeyboardButton("Bright Sky", callback_data='Bright Sky')],
        [InlineKeyboardButton("Dark 2024", callback_data='Dark 2024'), InlineKeyboardButton("Cinematic Night", callback_data='Cinematic Night')],
        [InlineKeyboardButton("Deep Fall", callback_data='Deep Fall'), InlineKeyboardButton("Blue Lake", callback_data='Blue Lake')],
        [InlineKeyboardButton("Smooth Face", callback_data='Smooth Face')]
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
