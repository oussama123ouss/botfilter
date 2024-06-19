import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from moviepy.editor import VideoFileClip, vfx
import tempfile

# API Key
API_KEY = 'YOUR_BOT_API_TOKEN'

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

def apply_filter(video_clip, filter_name: str):
    if filter_name == 'Cinematic':
        return video_clip.fx(vfx.colorx, 1.2).fx(vfx.lum_contrast, lum=15, contrast=30)
    elif filter_name == 'Soft Glow':
        return video_clip.fx(vfx.colorx, 1.1).fx(vfx.lum_contrast, contrast=15)
    elif filter_name == 'Vintage':
        return video_clip.fx(vfx.blackwhite).fx(vfx.lum_contrast, contrast=30).fx(vfx.colorx, 0.8)
    elif filter_name == 'Cool Tone':
        return video_clip.fx(vfx.colorx, 0.9).fx(vfx.lum_contrast, contrast=10)
    elif filter_name == 'Brighten':
        return video_clip.fx(vfx.colorx, 1.3)
    elif filter_name == 'Sepia':
        return video_clip.fx(vfx.colorx, 0.8).fx(vfx.lum_contrast, contrast=20)
    elif filter_name == 'B&W':
        return video_clip.fx(vfx.blackwhite)
    elif filter_name == 'High Contrast':
        return video_clip.fx(vfx.lum_contrast, contrast=50)
    elif filter_name == 'Soft Blur':
        return video_clip.fx(vfx.gaussian_blur, sigma=2)
    elif filter_name == 'Desaturate':
        return video_clip.fx(vfx.colorx, 0.5)
    else:
        return video_clip

def send_filters_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Cinematic", callback_data='Cinematic'), InlineKeyboardButton("Soft Glow", callback_data='Soft Glow'), InlineKeyboardButton("Vintage", callback_data='Vintage')],
        [InlineKeyboardButton("Cool Tone", callback_data='Cool Tone'), InlineKeyboardButton("Brighten", callback_data='Brighten'), InlineKeyboardButton("Sepia", callback_data='Sepia')],
        [InlineKeyboardButton("B&W", callback_data='B&W'), InlineKeyboardButton("High Contrast", callback_data='High Contrast'), InlineKeyboardButton("Soft Blur", callback_data='Soft Blur')],
        [InlineKeyboardButton("Desaturate", callback_data='Desaturate')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('اختر أحد الفلاتر الآتية:', reply_markup=reply_markup)

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
