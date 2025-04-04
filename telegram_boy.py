import x_bot
from dotenv import load_dotenv
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token)
dp = Dispatcher(bot)

TWITTER_LINK_PATTERN = re.compile(r'https?://(www\.)?(twitter\.com|x\.com)/[A-Za-z0-9_]+/status/\d+')


@dp.message_handler()
async def handle_message(message: types.Message):
    """conection btw telegram and x bot"""
    message_text = message.text

    if message_text:
        match = TWITTER_LINK_PATTERN.search(message_text)
        if match:
            x_data = x_bot.get_tweet_data(message_text)
            keyboard = InlineKeyboardMarkup(row_width=2)
            btn1 = InlineKeyboardButton("Option 1", callback_data="option_1")
            btn2 = InlineKeyboardButton("Option 2", callback_data="option_2")
            btn3 = InlineKeyboardButton("Option 3", callback_data="option_3")
            keyboard.add(btn1, btn2, btn3)            
            await message.answer(x_data, reply_markup=keyboard)
        else:
            return


@dp.callback_query_handler(lambda c: c.data.startswith("option"))
async def process_callback(callback_query: types.CallbackQuery):
    option = callback_query.data.replace("option_", "")
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"You chose Option {option}!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)