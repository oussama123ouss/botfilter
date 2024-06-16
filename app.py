import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from PIL import Image, ImageEnhance, ImageFilter

# استبدل هذا بالرمز الخاص بك من BotFather
TELEGRAM_API_TOKEN = '6987466658:AAEWjl7aoa_LSqQSx0s4REM5gyT6vUz_6sc'

# قائمة الفلاتر المتاحة
FILTERS = [
    ('Mocha', ImageFilter.BLUR), 
    ('Orange Teal', ImageEnhance.Color),
    # أضف المزيد من الفلاتر هنا...
]

def start(update: Update, context):
    update.message.reply_text('مرحباً! أرسل صورة لاستخدام الفلاتر.')

def handle_photo(update: Update, context):
    photo = update.message.photo[-1].get_file()
    photo.download('received_image.jpg')

    keyboard = [[InlineKeyboardButton(flt[0], callback_data=flt[0])] for flt in FILTERS]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('اختر فلتر لتطبيقه على الصورة:', reply_markup=reply_markup)

def apply_filter(image_path, filter_name):
    img = Image.open(image_path)
    
    for flt in FILTERS:
        if flt[0] == filter_name:
            if isinstance(flt[1], ImageFilter.Filter):
                img = img.filter(flt[1])
            elif isinstance(flt[1], ImageEnhance._Enhance):
                enhancer = flt[1](img)
                img = enhancer.enhance(2)
            # أضف المزيد من الفلاتر هنا إذا لزم الأمر...

    output_path = 'output_image.jpg'
    img.save(output_path)
    return output_path

def button(update: Update, context):
    query = update.callback_query
    query.answer()

    filter_name = query.data
    output_path = apply_filter('received_image.jpg', filter_name)
    
    query.message.reply_photo(photo=open(output_path, 'rb'), caption=f'تم تطبيق فلتر {filter_name} بنجاح.')

def main():
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
