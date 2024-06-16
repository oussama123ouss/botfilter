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
        # تطبيق تأثير Pine
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)  # زيادة التشبع بنسبة 30%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)  # زيادة التباين بنسبة 20%

        r, g, b = image.split()
        r = r.point(lambda i: i * 1.2)
        g = g.point(lambda i: i * 1.1)
        image = Image.merge('RGB', (r, g, b))

        return image
    else:
        return image

def send_filters_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Mocha", callback_data='Mocha')],
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
