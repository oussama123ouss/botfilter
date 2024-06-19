import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from moviepy.editor import VideoFileClip, vfx
import tempfile
import numpy as np

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
            "أرسل الفيديو 🎥 المراد تطبيق الفلاتر عليه 🔮\n\n"
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

def apply_filter(video_clip, filter_name: str):
    if filter_name == 'Color Enhancement':
        return video_clip.fx(vfx.colorx, 1.2).fx(vfx.lum_contrast, contrast=30)
    elif filter_name == 'Soft Blur':
        return video_clip.fx(vfx.gaussian_blur, sigma=1.5)
    else:
        return video_clip

def send_filters_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("تعزيز الألوان", callback_data='Color Enhancement'), InlineKeyboardButton("تنعيم ناعم", callback_data='Soft Blur')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('اختر أحد الفلاتر الآتية لتطبيقه على الفيديو:', reply_markup=reply_markup)

def handle_video(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if check_membership(user_id, context):
        video_file = update.message.video.get_file()
        video_bytes = video_file.download_as_bytearray()
        context.user_data['video'] = video_bytes
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

    # Write the video data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_video:
        tmp_video.write(video_data)
        tmp_video_path = tmp_video.name

    video_clip = VideoFileClip(tmp_video_path)

    filtered_video = apply_filter(video_clip, filter_name)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_output:
        filtered_video.write_videofile(tmp_output.name, codec='libx264')
        tmp_output_path = tmp_output.name

    with open(tmp_output_path, 'rb') as video_file:
        keyboard = [
            [InlineKeyboardButton("تابعني على تلغرام", url="https://t.me/elkhabur")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_video(video=video_file, caption=f"Filter name: {filter_name}\nتمت إضافة التأثير بنجاح.", reply_markup=reply_markup)

    # Clean up the temporary files
    os.remove(tmp_video_path)
    os.remove(tmp_output_path)

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
