import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from PIL import Image
import numpy as np
import cv2
import colour
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

def load_cube(file_path):
    """Load .cube LUT file."""
    with open(file_path) as f:
        lines = f.readlines()
    
    lut_size = None
    lut = []
    
    for line in lines:
        if line.startswith('#') or line.startswith('TITLE') or line.startswith('LUT_3D_SIZE'):
            continue
        elif line.startswith('LUT_3D_SIZE'):
            lut_size = int(line.split()[1])
        else:
            lut.append([float(x) for x in line.strip().split()])
    
    return np.array(lut).reshape(lut_size, lut_size, lut_size, 3)

def apply_lut(image: Image.Image, lut: np.ndarray) -> Image.Image:
    """Apply LUT to image."""
    img = np.array(image)
    img = img / 255.0  # Normalize the image to 0-1
    
    lut_size = lut.shape[0]
    result = np.empty_like(img)
    
    for i in range(3):
        channel = img[..., i]
        result[..., i] = np.interp(channel, np.linspace(0, 1, lut_size), lut[..., i].ravel())
    
    result = (result * 255).astype(np.uint8)
    return Image.fromarray(result)

def send_filters_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Filter 1", callback_data='filter1.cube')],
        [InlineKeyboardButton("Filter 2", callback_data='filter2.cube')],
        [InlineKeyboardButton("Filter 3", callback_data='filter3.cube')]
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

    lut_path = os.path.join('path_to_filters_directory', filter_name)
    lut = load_cube(lut_path)
    
    filtered_image = apply_lut(image, lut)

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
