import x_bot
from dotenv import load_dotenv
import os
import re
from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

TWITTER_LINK_PATTERN = re.compile(r'https?://(www\.)?(twitter\.com|x\.com)/[A-Za-z0-9_]+/status/\d+')


def calculate_percentage(actual, target):
    percentage = round((actual / target) * 100, 2)
    return min(percentage, 100)

def get_emoji(percentage):
    if percentage <= 50:
        return "🟥"  # Red square emoji for <= 50%
    elif percentage < 100:
        return "🟨"  # Yellow square emoji for < 100%
    else:
        return "🟦"  # Blue square emoji for >= 100%


@dp.message()
async def handle_message(message: types.Message):
    """conection btw telegram and x bot"""
    message_text = message.text

    if message_text:
        match = TWITTER_LINK_PATTERN.search(message_text)
        if match:            
            global link
            global likes_target
            global retweets_target
            global replies_target
            global views_target
            global bookmarks_target
            link = message_text
            likes_target = 10
            retweets_target = 3
            replies_target = 5
            views_target = 0
            bookmarks_target = 0
            formatted = (
                f"🔗 Link: {link}\n"
                f"💙 Likes: {likes_target}\n"
                f"🔄 Retweets: {retweets_target}\n"
                f"💬 Replies: {replies_target}\n"
                f"👀 Views: {views_target}\n"
                f"🔖 Bookmarks: {bookmarks_target}"
            )
            global keyboard_message
            keyboard_message = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="💥 Start Raid 💥", callback_data="option_1")],
                    [InlineKeyboardButton(text="🎯 Targets", callback_data="option_2")],
                    [InlineKeyboardButton(text="🚪 Close", callback_data="option_3")],
                ]
            )          
            await message.answer(formatted, reply_markup=keyboard_message)
        else:
            return
        
@dp.callback_query(lambda c: c.data.startswith("target_"))
async def handle_target(callback_query: types.CallbackQuery):
    target = callback_query.data.replace("target_", "")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text = "🔙 Back", callback_data="target_7")]
        ]
    )

    if target == "1":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='⚙️ Raid Options > Targets > Likes\n\n'
                'Please reply to this message with the new number of likes that a tweet must have to be considered a valid target.\n\n'
                f'Current Likes: {likes_target}',
            reply_markup=keyboard
        )
        await bot.answer_callback_query(callback_query.id)
    
    if target == "2":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='⚙️ Raid Options > Targets > Retweets\n\n'
                'Please reply to this message with the new number of retweets that a tweet must have to be considered a valid target.\n\n'
                f'Current Retweets: {retweets_target}',
            reply_markup=keyboard
        )
        await bot.answer_callback_query(callback_query.id)

    if target == "3":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='⚙️ Raid Options > Targets > Replies\n\n'
                'Please reply to this message with the new number of replies that a tweet must have to be considered a valid target.\n\n'
                f'Current Replies: {replies_target}',
            reply_markup=keyboard
        )
        await bot.answer_callback_query(callback_query.id)
    
    if target == "4":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='⚙️ Raid Options > Targets > Views\n\n'
                'Please reply to this message with the new number of views that a tweet must have to be considered a valid target.\n\n'
                f'Current Views: {views_target}',
            reply_markup=keyboard
        )
        await bot.answer_callback_query(callback_query.id)
    
    if target == "5":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='⚙️ Raid Options > Targets > Bookmarks\n\n'
                'Please reply to this message with the new number of bookmarks that a tweet must have to be considered a valid target.\n\n'
                f'Current Bookmarks: {bookmarks_target}',
            reply_markup=keyboard
        )
        await bot.answer_callback_query(callback_query.id)
    


    if target == "6":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=f"🔗 Link: {link}\n"
                f"💙 Likes: {likes_target}\n"
                f"🔄 Retweets: {retweets_target}\n"
                f"💬 Replies: {replies_target}\n"
                f"👀 Views: {views_target}\n"
                f"🔖 Bookmarks: {bookmarks_target}",
            reply_markup=keyboard_message
        )
        await bot.answer_callback_query(callback_query.id)
    
    if target == "7":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="⚙️ Raid Options > Targets\n\n"
                "You can specify the number of likes, retweets, replies, views and bookmarks that a tweet must have to be considered a valid target below.",
            reply_markup=keyboard_target
        )
        await bot.answer_callback_query(callback_query.id)



@dp.callback_query(lambda c: c.data.startswith("option"))
async def process_callback(callback_query: types.CallbackQuery):
    option = callback_query.data.replace("option_", "")      

    if option == "1":
        #x_data = x_bot.get_tweet_data(link)
        x_data = {'1':0}
        likes = x_data.get("Likes", 2)
        retweets = x_data.get("Retweets", 4)
        replies = x_data.get("Replies", 2)
        likes_percentage = calculate_percentage(likes, likes_target)
        retweets_percentage = calculate_percentage(retweets, retweets_target)
        replies_percentage = calculate_percentage(replies, replies_target)

        percentages = f"{get_emoji(likes_percentage)} Likes {likes} | {likes_target}  [{'💯' if likes_percentage==100 else likes_percentage }%]\n" + f"{get_emoji(retweets_percentage)} Retweets {retweets} | {retweets_target}  [{'💯' if retweets_percentage==100 else retweets_percentage }%]\n" + f"{get_emoji(replies_percentage)} Replies {replies} | {replies_target}  [{'💯' if replies_percentage==100 else replies_percentage}%]\n\n" + f"{link}\n\n"

        if likes_percentage == 100 and retweets_percentage == 100 and replies_percentage == 100:
            raid_message =  "🎊 Raid Ended - Targets Reached!\n\n" + percentages + "⏰ Duration: 0 minutes"
        else:
            raid_message =  "⚡️ Raid Started!\n\n" + percentages 

        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.message.chat.id, raid_message)
    elif option == "2":
        global keyboard_target
        keyboard_target = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"💙 Likes ({likes_target})", callback_data="target_1")],
                [InlineKeyboardButton(text=f"🔄 Retweets ({retweets_target})", callback_data="target_2")],
                [InlineKeyboardButton(text=f"💬 Replies ({replies_target})", callback_data="target_3")],
                [InlineKeyboardButton(text=f"👀 Views ({views_target})", callback_data="target_4")],
                [InlineKeyboardButton(text=f"🔖 Bookmarks ({bookmarks_target})", callback_data="target_5")],
                [InlineKeyboardButton(text="🔙 Back", callback_data="target_6")],
            ]
        )



        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="⚙️ Raid Options > Targets\n\n"
                "You can specify the number of likes, retweets, replies, views and bookmarks that a tweet must have to be considered a valid target below.",
            reply_markup=keyboard_target
        )
        await bot.answer_callback_query(callback_query.id)


    elif option == "3":
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

@dp.message(F.reply_to_message)
async def reply_handler(message: types.Message):
    # Check if the original message was from the bot
    if message.reply_to_message.from_user.id == (await bot.me()).id:
        await message.answer("I see you replied to me 👀")
    else:
        await message.answer("You're replying to someone else, not me.")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())