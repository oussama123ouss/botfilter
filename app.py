import telebot
import requests
from PIL import Image, ImageFilter
from io import BytesIO

# Replace with your Telegram bot API token
bot = telebot.TeleBot("6987466658:AAEWjl7aoa_LSqQSx0s4REM5gyT6vUz_6sc")

# URLs for filters .cube files
filter_urls = {
    "Filter 1": "https://drive.google.com/uc?export=download&id=14S6bx7deeUyqdcDSwFWQH3iOIhkAUEJ5",
    "Filter 2": "https://drive.google.com/uc?export=download&id=14S6c4TiDBbU87HvPOr8yxG0ePdp9dsCC",
    "Filter 3": "https://drive.google.com/uc?export=download&id=14fmZrMoIzNp3YBVP21vMKcGxum150-Uf",
    "Filter 4": "https://drive.google.com/uc?export=download&id=14nDCF8zHKChe6lfqNp-2MlvjvHni9WYD",
    "Filter 5": "https://drive.google.com/uc?export=download&id=14Pdw8K_ndshzC9F9V4hqSYyOE82apdwV"
}

# Function to apply filter .cube to image
def apply_filter_to_image(image, filter_url):
    # Download the filter .cube file
    filter_file = requests.get(filter_url).content
    
    # Apply the filter to the image
    with Image.open(BytesIO(filter_file)) as filter_image:
        filtered_image = Image.new("RGB", image.size)
        filtered_image.paste(image)
        filtered_image = Image.blend(filtered_image, filter_image, alpha=0.5)  # Adjust alpha as needed
        
    return filtered_image

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Image Filter Bot! Send me a photo to apply a filter.")

# Handler for receiving images
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Download the photo
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        
        # Open the image from URL
        image = Image.open(BytesIO(requests.get(file_url).content))
        
        # Example: Apply Filter 1 to the image
        filter_name = "Filter 1"
        filtered_image = apply_filter_to_image(image, filter_urls[filter_name])
        
        # Convert filtered image to bytes
        output_buffer = BytesIO()
        filtered_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)
        
        # Send the filtered image back to the user
        bot.send_photo(message.chat.id, output_buffer)
    
    except Exception as e:
        print(f"Error processing photo: {e}")
        bot.reply_to(message, "Sorry, something went wrong processing the photo.")

# Start the bot
bot.polling()
