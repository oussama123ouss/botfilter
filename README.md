# Telegram Image Filter Bot

This bot applies various filters to images sent by users. Filters are defined using `.cube` LUT files.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/oussama123ouss/botfilter.git
    cd TelegramImageFilterBot
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Place your `.cube` filter files in the `filters` directory.

4. Update the `6987466658:AAEWjl7aoa_LSqQSx0s4REM5gyT6vUz_6sc` in `main.py` with your Telegram bot API key.

## Running the Bot

```sh
python bot.py
