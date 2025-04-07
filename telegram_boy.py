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
            link = message_text
            views = 0
            bookmarks = 0
            formatted = (
                f"🔗 Link: {link}\n"
                f"❤️ Likes: {x_data.get('Likes', None)}\n"
                f"🔄 Retweets: {x_data.get('Retweets', None)}\n"
                f"💬 Replies: {x_data.get('Replies', None)}\n"
                f"👀 Views: {views}\n"
                f"🔖 Bookmarks: {bookmarks}"
            )
            keyboard = InlineKeyboardMarkup(row_width=1)
            btn1 = InlineKeyboardButton("💥 Start Raid 💥", callback_data="option_1")
            btn2 = InlineKeyboardButton("🎯 targets", callback_data="option_2")
            btn3 = InlineKeyboardButton("🚪 Close", callback_data="option_3")
            keyboard.add(btn1, btn2, btn3)            
            await message.answer(formatted, reply_markup=keyboard)
        else:
            return


@dp.callback_query_handler(lambda c: c.data.startswith("option"))
async def process_callback(callback_query: types.CallbackQuery):
    option = callback_query.data.replace("option_", "")
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"You chose Option {option}!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)