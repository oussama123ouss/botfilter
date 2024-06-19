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
    if filter_name == 'Brightening':
        return video_clip.fx(vfx.colorx, 1.2)
    elif filter_name == 'Contrast Boost':
        return video_clip.fx(vfx.lum_contrast, contrast=40)
    elif filter_name == 'Warm Filter':
        def warm_filter(get_frame, t):
            frame = get_frame(t)
            frame[:, :, 0] = np.clip(frame[:, :, 0] * 1.1, 0, 255)  # Increase red channel
            frame[:, :, 2] = np.clip(frame[:, :, 2] * 0.9, 0, 255)  # Decrease blue channel
            return frame
        return video_clip.fl(warm_filter)
    elif filter_name == 'Cool Filter':
        def cool_filter(get_frame, t):
            frame = get_frame(t)
            frame[:, :, 0] = np.clip(frame[:, :, 0] * 0.9, 0, 255)  # Decrease red channel
            frame[:, :, 2] = np.clip(frame[:, :, 2] * 1.1, 0, 255)  # Increase blue channel
            return frame
        return video_clip.fl(cool_filter)
    elif filter_name == 'Saturation Boost':
        return video_clip.fx(vfx.colorx, 1.5)
    elif filter_name == 'Vintage':
        return video_clip.fx(vfx.colorx, 0.7).fx(vfx.lum_contrast, contrast=20).fx(vfx.blackwhite)
    elif filter_name == 'Black and White':
        return video_clip.fx(vfx.blackwhite)
    elif filter_name == 'Sepia':
        def sepia_filter(get_frame, t):
            frame = get_frame(t)
            r, g, b = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]
            tr = 0.393 * r + 0.769 * g + 0.189 * b
            tg = 0.349 * r + 0.686 * g + 0.168 * b
            tb = 0.272 * r + 0.534 * g + 0.131 * b
            sepia = np.stack([tr, tg, tb], axis=2)
            return np.clip(sepia, 0, 255).astype(np.uint8)
        return video_clip.fl(sepia_filter)
    elif filter_name == 'Vignette':
        def vignette_filter(get_frame, t):
            frame = get_frame(t)
            rows, cols, _ = frame.shape
            X_resultant_kernel = cv2.getGaussianKernel(cols,200)
            Y_resultant_kernel = cv2.getGaussianKernel(rows,200)
            kernel = Y_resultant_kernel * X_resultant_kernel.T
            mask = 255 * kernel / np.linalg.norm(kernel)
            output = np.copy(frame)
            for i in range(3):
                output[:,:,i] = output[:,:,i] * mask
            return output
        return video_clip.fl(vignette_filter)
    elif filter_name == 'Blur':
        return video_clip.fx(vfx.gaussian_blur, sigma=2)
    else:
        return video_clip

def send_filters_keyboard(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Brightening", callback_data='Brightening'), InlineKeyboardButton("Contrast Boost", callback_data='Contrast Boost')],
        [InlineKeyboardButton("Warm Filter", callback_data='Warm Filter'), InlineKeyboardButton("Cool Filter", callback_data='Cool Filter')],
        [InlineKeyboardButton("Saturation Boost", callback_data='Saturation Boost'), InlineKeyboardButton("Vintage", callback_data='Vintage')],
        [InlineKeyboardButton("Black and White", callback_data='Black and White'), InlineKeyboardButton("Sepia", callback_data='Sepia')],
        [InlineKeyboardButton("Vignette", callback_data='Vignette'), InlineKeyboardButton("Blur", callback_data='Blur')]
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

    try:
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
    except Exception as e:
        logger.error(f"Error applying filter: {e}")
        query.message.reply_text("حدث خطأ أثناء تطبيق الفلتر. يرجى المحاولة مرة أخرى.")
    finally:
        # Clean up the temporary files
        if os.path.exists(tmp_video_path):
            os.remove(tmp_video_path)
        if os.path.exists(tmp_output_path):
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
