import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from moviepy.editor import VideoFileClip, vfx
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
CHANNEL_USERNAME = '@elkhabur'

def check_membership(user_id, context):
    try:
        user_member = context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return user_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking membership: {e}")
        return False

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if check_membership(user_id, context):
        keyboard = [
            [InlineKeyboardButton("تابعني على تلغرام", url="https://t.me/elkhabur")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "مرحبا عزيزي 🎉\n\n"
            "أرسل الفيديو 🎥 المراد تطبيق فلاتر عليه 🔮\n\n"
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

def apply_filter(video: VideoFileClip, filter_name: str) -> VideoFileClip:
    if filter_name == 'Cinematic':
        return video.fx(vfx.colorx, 1.5).fx(vfx.lum_contrast, 0, 30, 128)
    elif filter_name == 'Soft':
        return video.fx(vfx.colorx, 1.2)
    elif filter_name == 'Black and White':
        return video.fx(vfx.blackwhite)
    elif filter_name == 'Edge Detection':
        return video.fx(vfx.lum_contrast, 0, 30, 128).fx(vfx.colorx, 0.5)
    elif filter_name == 'Vintage':
        return video.fx(vfx.lum_contrast, 0, 50, 128).fx(vfx.colorx, 0.7)
    elif filter_name == 'Invert':
        return video.fx(vfx.invert_colors)
    elif filter_name == 'Brightness':
        return video.fx(vfx.colorx, 1.3)
    elif filter_name == 'Glow':
        return video.fx(vfx.colorx, 1.1).fx(vfx.lum_contrast, 0, 40, 128)
    elif filter_name == 'Posterize':
        return video.fx(vfx.posterize, 8)
    elif filter_name == 'Solarize':
        return video.fx(vfx.lum_contrast, 0, 30, 128).fx(vfx.colorx, 0.5)
    else:
        return video

def send_filters_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Cinematic", callback_data='Cinematic'), InlineKeyboardButton("Soft", callback_data='Soft'), InlineKeyboardButton("Black and White", callback_data='Black and White')],
        [InlineKeyboardButton("Edge Detection", callback_data='Edge Detection'), InlineKeyboardButton("Vintage", callback_data='Vintage'), InlineKeyboardButton("Invert", callback_data='Invert')],
        [InlineKeyboardButton("Brightness", callback_data='Brightness'), InlineKeyboardButton("Glow", callback_data='Glow'), InlineKeyboardButton("Posterize", callback_data='Posterize')],
        [InlineKeyboardButton("Solarize", callback_data='Solarize')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('اختر أحد الفلاتر الآتية:', reply_markup=reply_markup)

def handle_video(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if check_membership(user_id, context):
        context.user_data['video'] = update.message.video.get_file().download_as_bytearray()
        send_filters_keyboard(update, context)
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

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    filter_name = query.data
    video_data = context.user_data['video']
    video = VideoFileClip(io.BytesIO(video_data))

    filtered_video = apply_filter(video, filter_name)

    bio = io.BytesIO()
    bio.name = 'video.mp4'
    filtered_video.write_videofile(bio.name, codec='libx264')
    bio.seek(0)

    keyboard = [
        [InlineKeyboardButton("تابعني على تلغرام", url="https://t.me/elkhabur")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_video(video=bio, caption=f"Filter name: {filter_name}\nتمت إضافة التأثير بنجاح.", reply_markup=reply_markup)

def main() -> None:
    updater = Updater(API_KEY)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.video, handle_video))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
