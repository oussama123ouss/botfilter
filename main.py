import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from PIL import Image, ImageEnhance, ImageFilter
import io
import cv2
import numpy as np

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

def load_lut(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        logger.error(f"Error loading LUT file {file_path}: {e}")
        return None

    lut = []
    for line in lines:
        if line.startswith('#') or line.strip() == '':
            continue
        values = list(map(float, line.split()))
        lut.append(values)

    lut = np.array(lut)
    lut = lut.reshape((int(np.cbrt(len(lut))), int(np.cbrt(len(lut))), int(np.cbrt(len(lut))), 3))
    return lut

def apply_lut(image, lut):
    try:
        image_array = np.array(image)
        h, w, _ = image_array.shape
        lut = cv2.resize(lut, (w, h), interpolation=cv2.INTER_LINEAR)
        result = cv2.LUT(image_array, lut)
        return Image.fromarray(result)
    except Exception as e:
        logger.error(f"Error applying LUT: {e}")
        return image

# Load LUT filters
try:
    moody_yellow_lut = load_lut('/mnt/data/Moody Yellow LUT.cube_10.C1545.cube')
    colour_pop_lut = load_lut('/mnt/data/colour_pop.cube')
    cinematic_lut = load_lut('/mnt/data/Cinematic_for_Flog.cube')
except Exception as e:
    logger.error(f"Error loading LUTs: {e}")

def apply_filter(image: Image.Image, filter_name: str) -> Image.Image:
    if filter_name == 'Moody Yellow':
        return apply_lut(image, moody_yellow_lut)
    elif filter_name == 'Colour Pop':
        return apply_lut(image, colour_pop_lut)
    elif filter_name == 'Cinematic':
        return apply_lut(image, cinematic_lut)
    else:
        return image

def send_filters_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Moody Yellow", callback_data='Moody Yellow'), InlineKeyboardButton("Colour Pop", callback_data='Colour Pop')],
        [InlineKeyboardButton("Cinematic", callback_data='Cinematic')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('اختر أحد الفلاتر الآتية:', reply_markup=reply_markup)

def handle_image(update: Update, context: CallbackContext) -> None:
    try:
        context.user_data['image'] = update.message.photo[-1].get_file().download_as_bytearray()
        send_filters_keyboard(update, context)
    except Exception as e:
        logger.error(f"Error handling image: {e}")
        update.message.reply_text("حدث خطأ أثناء معالجة الصورة. يرجى المحاولة مرة أخرى.")

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
