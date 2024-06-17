import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from PIL import Image
import cv2
import numpy as np
import io

# تثبيت مكتبة OpenCV
# pip install opencv-python-headless

# API Key
API_KEY = '6987466658:AAEWjl7aoa_LSqQSx0s4REM5gyT6vUz_6sc'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("تابعني على تلغرام", url="https://t.me/elkhabur")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "مرحبا عزيزي 🎉\n\n"
        "أرسل الصورة 🖼️ المراد تطبيق فلاتر عليها 🔮\n\n"
        "جميع الصيغ مدعومة ⚡️",
        reply_markup=reply_markup
    )

def apply_filter(image: Image.Image, filter_name: str) -> Image.Image:
    # Convert PIL Image to OpenCV image
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Load the cube file
    cube_path = f'{filter_name}.cube'
    lut = cv2.imread(cube_path, cv2.IMREAD_UNCHANGED)

    # Apply the LUT filter
    filtered_image = cv2.transform(cv_image, lut)

    # Convert back to PIL Image
    filtered_image = Image.fromarray(cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB))
    return filtered_image

def send_filters_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("فلتر 1", callback_data='filter1'), InlineKeyboardButton("فلتر 2", callback_data='filter2'), InlineKeyboardButton("فلتر 3", callback_data='filter3')],
        [InlineKeyboardButton("فلتر 4", callback_data='filter4'), InlineKeyboardButton("فلتر 5", callback_data='filter5')]
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

    keyboard = [
        [InlineKeyboardButton("تابعني على تلغرام", url="https://t.me/elkhabur")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_photo(photo=bio, caption=f"Filter name: {filter_name}\nتمت إضافة التأثير بنجاح.", reply_markup=reply_markup)

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
