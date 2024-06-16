import os
from PIL import Image, ImageFilter, ImageEnhance
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

# قائمة الفلاتر
FILTERS = [
    ('Mocha', ImageFilter.CONTOUR),
    ('Orange Teal', ImageEnhance.Color),
    ('Blur', ImageFilter.BLUR),
    ('Detail', ImageFilter.DETAIL),
    ('Edge Enhance', ImageFilter.EDGE_ENHANCE),
    ('Emboss', ImageFilter.EMBOSS),
    ('Sharpen', ImageFilter.SHARPEN),
    ('Brightness', ImageEnhance.Brightness),
    ('Contrast', ImageEnhance.Contrast),
    ('Sharpness', ImageEnhance.Sharpness),
]

# دالة بدء البوت
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مرحبًا! أرسل صورة لتطبيق الفلاتر عليها.')

# دالة لاستلام الصور
def handle_photo(update: Update, context: CallbackContext) -> None:
    photo_file = update.message.photo[-1].get_file()
    photo_path = 'received_image.jpg'
    photo_file.download(photo_path)

    # إنشاء قائمة الأزرار للفلاتر
    keyboard = [[InlineKeyboardButton(flt[0], callback_data=flt[0])] for flt in FILTERS]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('اختر أحد الفلاتر التالية:', reply_markup=reply_markup)

# دالة لتطبيق الفلتر
def apply_filter(image_path, filter_name):
    img = Image.open(image_path)
    
    for flt in FILTERS:
        if flt[0] == filter_name:
            if isinstance(flt[1], ImageFilter.Filter):
                img = img.filter(flt[1])
            elif isinstance(flt[1], type(ImageEnhance.Color(img))):
                enhancer = flt[1](img)
                img = enhancer.enhance(2)  # يمكنك تعديل مستوى التأثير هنا
            # أضف المزيد من الفلاتر هنا إذا لزم الأمر...

    output_path = 'output_image.jpg'
    img.save(output_path)
    return output_path

# دالة لاختيار الفلتر
def filter_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    filter_name = query.data

    query.answer()
    photo_path = 'received_image.jpg'
    output_path = apply_filter(photo_path, filter_name)

    # إرسال الصورة بعد تطبيق الفلتر
    query.message.reply_photo(photo=open(output_path, 'rb'))
    query.message.reply_text(f'تمت إضافة التأثير بنجاح: {filter_name}')

def main() -> None:
    # إعداد البوت باستخدام التوكن الخاص بك
    updater = Updater("6987466658:AAEWjl7aoa_LSqQSx0s4REM5gyT6vUz_6sc")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
    dispatcher.add_handler(CallbackQueryHandler(filter_callback))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
