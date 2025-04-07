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
            global link
            global likes
            global retweets
            global replies
            link = message_text
            likes = x_data.get("Likes", None)
            retweets = x_data.get("Retweets", None)
            replies = x_data.get("Replies", None)
            views = 0
            bookmarks = 0
            formatted = (
                f"🔗 Link: {link}\n"
                f"💙 Likes: {likes}\n"
                f"🔄 Retweets: {retweets}\n"
                f"💬 Replies: {replies}\n"
                f"👀 Views: {views}\n"
                f"🔖 Bookmarks: {bookmarks}"
            )
            keyboard = InlineKeyboardMarkup(row_width=1)
            btn1 = InlineKeyboardButton("💥 Start Raid 💥", callback_data="option_1")
            btn2 = InlineKeyboardButton("🎯 Targets", callback_data="option_2")
            btn3 = InlineKeyboardButton("🚪 Close", callback_data="option_3")
            keyboard.add(btn1, btn2, btn3)            
            await message.answer(formatted, reply_markup=keyboard)
        else:
            return


@dp.callback_query_handler(lambda c: c.data.startswith("option"))
async def process_callback(callback_query: types.CallbackQuery):
    option = callback_query.data.replace("option_", "")
    
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)

    if option == "1":
        await bot.send_message(callback_query.message.chat.id, 
            "🎊 Raid Ended - Targets Reached!\n\n"
            f"🟦 Likes {likes} | 10 [💯%]\n"
            f"🟦 Retweets {retweets} | 5 [💯%]\n"
            f"🟦 Replies {replies} | 3 [💯%]\n\n"
            f"{link}\n\n"
            "⏰ Duration: 0 minutes"
        )
    elif option == "2":
        await bot.send_message(callback_query.message.chat.id, "Targets")
    elif option == "3":
        await bot.send_message(callback_query.message.chat.id, "Close")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)