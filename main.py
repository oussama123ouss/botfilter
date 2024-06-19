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

# Channel details
CHANNEL_ID = -1002013781137
CHANNEL_USERNAME = 'elkhabur'

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_member = context.bot.get_chat_member(CHANNEL_ID, user_id)

    if user_member.status in ['member', 'administrator', 'creator']:
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
    else:
        keyboard = [
            [InlineKeyboardButton("⚠️ متابعة ⚡️", url="https://t.me/elkhabur")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "⚠️  عذراً عزيزي \n"
            "⚙️  يجب عليك متابعة حسابي على تلغرام أولا\n"
            "📮  تابع ثم ارسل /start ⬇️",
            reply_markup=reply_markup
        )

def apply_filter(image: Image.Image, filter_name: str) -> Image.Image:
    if filter_name == 'Soft Contrast':
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(1.2)
    elif filter_name == 'Warm Glow':
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(1.3)
    elif filter_name == 'Vintage':
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.7)
        return image.filter(ImageFilter.GaussianBlur(1))
    elif filter_name == 'Cool Tone':
        r, g, b = image.split()
        b = b.point(lambda i: i * 1.2)
        return Image.merge('RGB', (r, g, b))
    elif filter_name == 'Brighten':
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(1.5)
    elif filter_name == 'Sharpen':
        return image.filter(ImageFilter.SHARPEN)
    elif filter_name == 'Smooth':
        return image.filter(ImageFilter.SMOOTH_MORE)
    elif filter_name == 'Sepia':
        sepia = [(r//2 + 100, g//2 + 50, b//2) for (r, g, b) in image.getdata()]
        image.putdata(sepia)
        return image
    elif filter_name == 'B&W':
        return image.convert('L')
    elif filter_name == 'High Contrast':
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2.0)
    elif filter_name == 'Soft Blur':
        return image.filter(ImageFilter.BLUR)
    elif filter_name == 'Detail Enhance':
        return image.filter(ImageFilter.DETAIL)
    elif filter_name == 'Edge Enhance':
        return image.filter(ImageFilter.EDGE_ENHANCE)
    elif filter_name == 'Emboss':
        return image.filter(ImageFilter.EMBOSS)
    elif filter_name == 'Contour':
        return image.filter(ImageFilter.CONTOUR)
    elif filter_name == 'Glow':
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(1.1)
    elif filter_name == 'Desaturate':
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(0.5)
    elif filter_name == 'Posterize':
        return image.convert("P", palette=Image.ADAPTIVE, colors=8)
    elif filter_name == 'Solarize':
        return image.point(lambda p: p if p < 128 else 255 - p)
    elif filter_name == 'Invert':
        return ImageOps.invert(image)
    else:
        return image

def send_filters_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Soft Contrast", callback_data='Soft Contrast'), InlineKeyboardButton("Warm Glow", callback_data='Warm Glow'), InlineKeyboardButton("Vintage", callback_data='Vintage')],
        [InlineKeyboardButton("Cool Tone", callback_data='Cool Tone'), InlineKeyboardButton("Brighten", callback_data='Brighten'), InlineKeyboardButton("Sharpen", callback_data='Sharpen')],
        [InlineKeyboardButton("Smooth", callback_data='Smooth'), InlineKeyboardButton("Sepia", callback_data='Sepia'), InlineKeyboardButton("B&W", callback_data='B&W')],
        [InlineKeyboardButton("High Contrast", callback_data='High Contrast'), InlineKeyboardButton("Soft Blur", callback_data='Soft Blur'), InlineKeyboardButton("Detail Enhance", callback_data='Detail Enhance')],
        [InlineKeyboardButton("Edge Enhance", callback_data='Edge Enhance'), InlineKeyboardButton("Emboss", callback_data='Emboss'), InlineKeyboardButton("Contour", callback_data='Contour')],
        [InlineKeyboardButton("Glow", callback_data='Glow'), InlineKeyboardButton("Desaturate", callback_data='Desaturate'), InlineKeyboardButton("Posterize", callback_data='Posterize')],
        [InlineKeyboardButton("Solarize", callback_data='Solarize'), InlineKeyboardButton("Invert", callback_data='Invert')]
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
