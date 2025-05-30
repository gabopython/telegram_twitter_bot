import x_bot
from utils import *
from config import BOT_TOKEN
from db import *

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
from datetime import datetime
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile,
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAnimation,
    Message,
    BotCommand,
)
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import os


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
resend_message = {}
resend_ongoing = True
commands = [
    BotCommand(command="/login", description="Login to X"),
    BotCommand(command="/stop", description="Stop the ongoing raid"),
    BotCommand(command="/trending", description="Set up a trending slot"),
]


@dp.message(Command("stop"))
async def stop_command(message: Message):
    # Check if the sender is an admin
    chat_id = message.chat.id
    user_id = message.from_user.id

    member = await message.bot.get_chat_member(chat_id, user_id)
    if member.status not in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}:
        return  # User is not an admin, ignore message

    chat_id = message.chat.id
    if raid_status.get(chat_id):
        await bot.delete_message(
            chat_id=chat_id, message_id=resend_message[chat_id]["message_id"]
        )
        raid_status[chat_id] = False
        if chat_id in timer:
            start_time = timer.pop(chat_id)
            elapsed_time = datetime.now() - start_time
            seconds = elapsed_time.total_seconds()
            minutes = int(seconds // 60)
        else:
            minutes = 0
        minutes = (
            f"⏰ <b>Duration</b>: 1 minute"
            if minutes == 1
            else f"⏰ <b>Duration</b>: {minutes} minutes"
        )
        caption = (
            "🛑 <b>Raid Ended - Stopped by admin</b>\n\n"
            + percentages[chat_id]
            + minutes
        )
        file_name = str(chat_id)
        file_type = await get_file_type(chat_id, "end")
        if file_type == "":
            file_type = await get_file_type(chat_id, "raid")
            if file_type == "":
                file_type = await get_file_type(chat_id, "start")
                file_path = os.path.join(
                    MEDIA_DIR_START,
                    file_name + (".mp4" if file_type == ".gif" else file_type),
                )
            else:
                file_path = os.path.join(
                    MEDIA_DIR_RAID,
                    file_name + (".mp4" if file_type == ".gif" else file_type),
                )
        else:
            file_path = os.path.join(
                MEDIA_DIR_END,
                file_name + (".mp4" if file_type == ".gif" else file_type),
            )
        file = None if file_type == "" else FSInputFile(file_path)

        if file_type == "":
            await message.answer(caption)
        elif file_type == ".jpg":
            await message.answer_photo(file, caption=caption)
        elif file_type == ".mp4":
            await message.answer_video(file, caption=caption)
        elif file_type == ".gif":
            await message.answer_animation(file, caption=caption)
    else:
        await message.answer("❌ <b>There is no ongoing raid in this group</b>")


@dp.message(Command("login"))
async def login_handler(message: Message):
    bot_username = (await bot.get_me()).username
    login_url = f"https://t.me/{bot_username}?login_dm=login"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="In Private", url=login_url)]]
    )

    await message.answer(
        "🔒 For your privacy, please continue login in DM. 👇", reply_markup=keyboard
    )


@dp.message(Command("login_dm"))
async def login_dm_handler(message: Message):
    if message.chat.type == "private" and message.text == "/login_dm login":
        login_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Login to X",
                        url="https://x.com/i/flow/login",
                    )
                ]
            ]
        )
        await message.answer(
            "Let's proceed with logging in to X.", reply_markup=login_keyboard
        )


@dp.message(Command("trending"))
async def trending_handler(message: Message):
    bot_username = (await bot.get_me()).username
    trending_url = f"https://t.me/{bot_username}?trending_dm=trending"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="In Private", url=trending_url)]]
    )

    await message.answer("Please continue in private 👇", reply_markup=keyboard)


@dp.message(Command("trending_dm"))
async def trending_dm_handler(message: Message):
    if message.chat.type == "private" and message.text == "/trending_dm trending":
        await message.answer(
            "Reply with your Token's Contract/Issuer Address to set up a trending slot:"
        )


@dp.message(F.reply_to_message)
async def reply_handler(message: Message):
    # Check if the sender is an admin
    chat_id = message.chat.id
    user_id = message.from_user.id

    member = await message.bot.get_chat_member(chat_id, user_id)
    if member.status not in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}:
        return  # User is not an admin, ignore message

    bot_id = (await bot.me()).id
    message_reply = (
        message.reply_to_message.text if message.reply_to_message.text else ""
    )
    if message.reply_to_message.from_user.id == bot_id:
        if "new number" in message_reply:
            if "default" in message_reply.lower():
                if "Likes" in message_reply:
                    try:
                        if likes_default_target[chat_id] == int(message.text):
                            bot_message = await message.answer(
                                same_value.format("Default", "Likes")
                            )
                            await asyncio.sleep(3)
                            await bot_message.delete()
                            await bot.delete_message(
                                chat_id=chat_id, message_id=message.message_id
                            )
                            return
                        likes_default_target[chat_id] = int(message.text)
                        await update_likes_default_target(
                            chat_id, likes_default_target[chat_id]
                        )
                        likes_target[chat_id] = likes_default_target[chat_id]
                        await update_likes_target(chat_id, likes_target[chat_id])
                        await bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message.reply_to_message.message_id,
                            text=target_saved.format(
                                "likes", "default ", "Likes", likes_target[chat_id]
                            ),
                            reply_markup=keyboard_default_back,
                        )
                    except ValueError:
                        bot_message = await message.answer(
                            "❌ <b>Invalid input. Please enter a valid number.</b>"
                        )
                        await asyncio.sleep(5)
                        await bot_message.delete()
                elif "Retweets" in message_reply:
                    try:
                        if retweets_default_target[chat_id] == int(message.text):
                            bot_message = await message.answer(
                                same_value.format("Default", "Retweets")
                            )
                            await asyncio.sleep(3)
                            await bot_message.delete()
                            await bot.delete_message(
                                chat_id=chat_id, message_id=message.message_id
                            )
                            return
                        retweets_default_target[chat_id] = int(message.text)
                        await update_retweets_default_target(
                            chat_id, retweets_default_target[chat_id]
                        )
                        retweets_target[chat_id] = retweets_default_target[chat_id]
                        await update_retweets_target(chat_id, retweets_target[chat_id])
                        await bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message.reply_to_message.message_id,
                            text=target_saved.format(
                                "retweets",
                                "default ",
                                "Retweets",
                                retweets_target[chat_id],
                            ),
                            reply_markup=keyboard_default_back,
                        )
                    except ValueError:
                        bot_message = await message.answer(
                            "❌ <b>Invalid input. Please enter a valid number.</b>"
                        )
                        await asyncio.sleep(5)
                        await bot_message.delete()
                elif "Replies" in message_reply:
                    try:
                        if replies_default_target[chat_id] == int(message.text):
                            bot_message = await message.answer(
                                same_value.format("Default", "Replies")
                            )
                            await asyncio.sleep(3)
                            await bot_message.delete()
                            await bot.delete_message(
                                chat_id=chat_id, message_id=message.message_id
                            )
                            return
                        replies_default_target[chat_id] = int(message.text)
                        await update_replies_default_target(
                            chat_id, replies_default_target[chat_id]
                        )
                        replies_target[chat_id] = replies_default_target[chat_id]
                        await update_replies_target(chat_id, replies_target[chat_id])
                        await bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message.reply_to_message.message_id,
                            text=target_saved.format(
                                "replies",
                                "default ",
                                "Replies",
                                replies_target[chat_id],
                            ),
                            reply_markup=keyboard_default_back,
                        )
                    except ValueError:
                        bot_message = await message.answer(
                            "❌ <b>Invalid input. Please enter a valid number.</b>"
                        )
                        await asyncio.sleep(5)
                        await bot_message.delete()
                elif "Views" in message_reply:
                    try:
                        if views_default_target[chat_id] == int(message.text):
                            bot_message = await message.answer(
                                same_value.format("Default", "Views")
                            )
                            await asyncio.sleep(3)
                            await bot_message.delete()
                            await bot.delete_message(
                                chat_id=chat_id, message_id=message.message_id
                            )
                            return
                        views_default_target[chat_id] = int(message.text)
                        await update_views_default_target(
                            chat_id, views_default_target[chat_id]
                        )
                        views_target[chat_id] = views_default_target[chat_id]
                        await update_views_target(chat_id, views_target[chat_id])
                        await bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message.reply_to_message.message_id,
                            text=target_saved.format(
                                "views", "default ", "Views", views_target[chat_id]
                            ),
                            reply_markup=keyboard_default_back,
                        )
                    except ValueError:
                        bot_message = await message.answer(
                            "❌ <b>Invalid input. Please enter a valid number.</b>"
                        )
                        await asyncio.sleep(5)
                        await bot_message.delete()
                elif "Bookmarks" in message_reply:
                    try:
                        if bookmarks_default_target[chat_id] == int(message.text):
                            bot_message = await message.answer(
                                same_value.format("Default", "Bookmarks")
                            )
                            await asyncio.sleep(3)
                            await bot_message.delete()
                            await bot.delete_message(
                                chat_id=chat_id, message_id=message.message_id
                            )
                            return
                        bookmarks_default_target[chat_id] = int(message.text)
                        await update_bookmarks_default_target(
                            chat_id, bookmarks_default_target[chat_id]
                        )
                        bookmarks_target[chat_id] = bookmarks_default_target[chat_id]
                        await update_bookmarks_target(
                            chat_id, bookmarks_target[chat_id]
                        )
                        await bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message.reply_to_message.message_id,
                            text=target_saved.format(
                                "bookmarks",
                                "default ",
                                "Bookmarks",
                                bookmarks_target[chat_id],
                            ),
                            reply_markup=keyboard_default_back,
                        )
                    except ValueError:
                        bot_message = await message.answer(
                            "❌ <b>Invalid input. Please enter a valid number.</b>"
                        )
                        await asyncio.sleep(5)
                        await bot_message.delete()
            elif "Likes" in message_reply:
                try:
                    if likes_target[chat_id] == int(message.text):
                        bot_message = await message.answer(
                            same_value.format("", "Likes")
                        )
                        await asyncio.sleep(3)
                        await bot_message.delete()
                        await bot.delete_message(
                            chat_id=chat_id, message_id=message.message_id
                        )
                        return
                    likes_target[chat_id] = int(message.text)
                    await update_likes_target(chat_id, likes_target[chat_id])
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message.reply_to_message.message_id,
                        text=target_saved.format(
                            "likes", "", "Likes", likes_target[chat_id]
                        ),
                        reply_markup=keyboard_back,
                    )
                except ValueError:
                    bot_message = await message.answer(
                        "❌ <b>Invalid input. Please enter a valid number.</b>"
                    )
                    await asyncio.sleep(5)
                    await bot_message.delete()
            elif "Retweets" in message_reply:
                try:
                    if retweets_target[chat_id] == int(message.text):
                        bot_message = await message.answer(
                            same_value.format("", "Retweets")
                        )
                        await asyncio.sleep(3)
                        await bot_message.delete()
                        await bot.delete_message(
                            chat_id=chat_id, message_id=message.message_id
                        )
                        return
                    retweets_target[chat_id] = int(message.text)
                    await update_retweets_target(chat_id, retweets_target[chat_id])
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message.reply_to_message.message_id,
                        text=target_saved.format(
                            "retweets", "", "Retweets", retweets_target[chat_id]
                        ),
                        reply_markup=keyboard_back,
                    )
                except ValueError:
                    bot_message = await message.answer(
                        "❌ <b>Invalid input. Please enter a valid number.</b>"
                    )
                    await asyncio.sleep(5)
                    await bot_message.delete()
            elif "Replies" in message_reply:
                try:
                    if replies_target[chat_id] == int(message.text):
                        bot_message = await message.answer(
                            same_value.format("", "Replies")
                        )
                        await asyncio.sleep(3)
                        await bot_message.delete()
                        await bot.delete_message(
                            chat_id=chat_id, message_id=message.message_id
                        )
                        return
                    replies_target[chat_id] = int(message.text)
                    await update_replies_target(chat_id, replies_target[chat_id])
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message.reply_to_message.message_id,
                        text=target_saved.format(
                            "replies", "", "Replies", replies_target[chat_id]
                        ),
                        reply_markup=keyboard_back,
                    )
                except ValueError:
                    bot_message = await message.answer(
                        "❌ <b>Invalid input. Please enter a valid number.</b>"
                    )
                    await asyncio.sleep(5)
                    await bot_message.delete()
            elif "Views" in message_reply:
                try:
                    if views_target[chat_id] == int(message.text):
                        bot_message = await message.answer(
                            same_value.format("", "Views")
                        )
                        await asyncio.sleep(3)
                        await bot_message.delete()
                        await bot.delete_message(
                            chat_id=chat_id, message_id=message.message_id
                        )
                        return
                    views_target[chat_id] = int(message.text)
                    await update_views_target(chat_id, views_target[chat_id])
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message.reply_to_message.message_id,
                        text=target_saved.format(
                            "views", "", "Views", views_target[chat_id]
                        ),
                        reply_markup=keyboard_back,
                    )
                except ValueError:
                    bot_message = await message.answer(
                        "❌ <b>Invalid input. Please enter a valid number.</b>"
                    )
                    await asyncio.sleep(5)
                    await bot_message.delete()
            elif "Bookmarks" in message_reply:
                try:
                    if bookmarks_target[chat_id] == int(message.text):
                        bot_message = await message.answer(
                            same_value.format("", "Bookmarks")
                        )
                        await asyncio.sleep(3)
                        await bot_message.delete()
                        await bot.delete_message(
                            chat_id=chat_id, message_id=message.message_id
                        )
                        return
                    bookmarks_target[chat_id] = int(message.text)
                    await update_bookmarks_target(chat_id, bookmarks_target[chat_id])
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message.reply_to_message.message_id,
                        text=target_saved.format(
                            "bookmarks", "", "Bookmarks", bookmarks_target[chat_id]
                        ),
                        reply_markup=keyboard_back,
                    )
                except ValueError:
                    bot_message = await message.answer(
                        "❌ <b>Invalid input. Please enter a valid number.</b>"
                    )
                    await asyncio.sleep(5)
                    await bot_message.delete()
        await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

        if "with your custom text" in message_reply:
            if len(message.text) <= 200:
                text = message.text
                await update_custom_text(chat_id, text)
                buttons_custom_text = [[remove_custom_text], [back]]
                keyboard_custom_text = InlineKeyboardMarkup(
                    inline_keyboard=buttons_custom_text
                )
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message.reply_to_message.message_id,
                    text="✅ <b>Text saved successfully!</b>\n\nPlease reply to this message with your custom text to change the current message used for ongoing raids in this group."
                    + "\n\n<b>Current Text:</b> "
                    + text,
                    reply_markup=keyboard_custom_text,
                )
            else:
                bot_message = await message.answer(
                    "❌ <b>Error: Your custom message exceeds the 200-character limit. Please try again.</b>"
                )
                await asyncio.sleep(4)
                await bot_message.delete()
            return

        if RAID_MEDIA_PROMPT not in message_reply:
            return  # Not the correct message

        file_path = None

        if "Start Media" in message_reply:
            if message.photo:
                media = message.photo[-1]
                file_path = MEDIA_DIR_START / f"{chat_id}.jpg"
                await bot.download(media, destination=file_path)
                file_type = ".jpg"
            elif message.video:
                media = message.video
                file_path = MEDIA_DIR_START / f"{chat_id}.mp4"
                await bot.download(media, destination=file_path)
                file_type = ".mp4"
            elif message.animation:
                media = message.animation
                file_path = MEDIA_DIR_START / f"{chat_id}.mp4"
                await bot.download(media, destination=file_path)
                file_type = ".gif"
            folder = "start"
            remove_data = "customization_5"
        elif "End Media" in message_reply:
            if message.photo:
                media = message.photo[-1]
                file_path = MEDIA_DIR_END / f"{chat_id}.jpg"
                await bot.download(media, destination=file_path)
                file_type = ".jpg"
            elif message.video:
                media = message.video
                file_path = MEDIA_DIR_END / f"{chat_id}.mp4"
                await bot.download(media, destination=file_path)
                file_type = ".mp4"
            elif message.animation:
                media = message.animation
                file_path = MEDIA_DIR_END / f"{chat_id}.mp4"
                await bot.download(media, destination=file_path)
                file_type = ".gif"
            folder = "end"
            remove_data = "customization_8"
        elif "Raid Media" in message_reply:
            if message.photo:
                media = message.photo[-1]
                file_path = MEDIA_DIR_RAID / f"{chat_id}.jpg"
                await bot.download(media, destination=file_path)
                file_type = ".jpg"
            elif message.video:
                media = message.video
                file_path = MEDIA_DIR_RAID / f"{chat_id}.mp4"
                await bot.download(media, destination=file_path)
                file_type = ".mp4"
            elif message.animation:
                media = message.animation
                file_path = MEDIA_DIR_RAID / f"{chat_id}.mp4"
                await bot.download(media, destination=file_path)
                file_type = ".gif"
            folder = "raid"
            remove_data = "customization_7"

        if file_path:
            await save_media(chat_id, file_type, folder)
            if file_type == ".jpg":
                current_type = "Image"
            elif file_type == ".mp4":
                current_type = "Video"
            elif file_type == ".gif":
                current_type = "GIF"
            keyboard_raid_media = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="❌ Remove File", callback_data=remove_data
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🔙 Back",
                            callback_data="customization_6",
                        )
                    ],
                ]
            )
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message.reply_to_message.message_id,
                text="✅ <b>Media saved successfully!</b>\n\nReply to this message with a video or image to change the current media used for ongoing raids in this group."
                + "\n\n<b>Current Media:</b> "
                + current_type,
                reply_markup=keyboard_raid_media,
            )
        else:
            bot_message = await message.answer(
                "❌ <b>Failed to save media. Upload a valid file.</b>"
            )
            await asyncio.sleep(4)
            await bot_message.delete()


@dp.message()
async def handle_message(message: Message):
    # Check if message has text
    message_text = message.text
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not message_text:
        return

    likes_default_target[chat_id] = await get_likes_default_target(chat_id)
    retweets_default_target[chat_id] = await get_retweets_default_target(chat_id)
    replies_default_target[chat_id] = await get_replies_default_target(chat_id)
    views_default_target[chat_id] = await get_views_default_target(chat_id)
    bookmarks_default_target[chat_id] = await get_bookmarks_default_target(chat_id)

    match = TWITTER_LINK_PATTERN.search(message_text)

    if message_text.startswith("/raid"):
        parts = message_text.split()

        if len(parts) < 2:
            bot_message = await message.answer(
                "❌ <b>Invalid syntax. Usage: /raid [TWEET_URL] [❤️,🔄,💬,👀,🔖]</b>"
            )
            await asyncio.sleep(4)
            await bot_message.delete()
            return

        link[chat_id] = parts[1]
        if not match:
            bot_message = await message.answer(
                "❌ <b>Invalid Twitter link. Please provide a valid link.</b>"
            )
            await asyncio.sleep(4)
            await bot_message.delete()
            return

        try:
            numbers = [int(part) for part in parts[2:]]
        except ValueError:
            return

        while len(numbers) < 5:
            numbers.append(0)

        numbers = numbers[:5]

        await update_likes_target(chat_id, numbers[0])
        await update_retweets_target(chat_id, numbers[1])
        await update_replies_target(chat_id, numbers[2])
        await update_views_target(chat_id, numbers[3])
        await update_bookmarks_target(chat_id, numbers[4])
        likes_target[chat_id] = numbers[0]
        retweets_target[chat_id] = numbers[1]
        replies_target[chat_id] = numbers[2]
        views_target[chat_id] = numbers[3]
        bookmarks_target[chat_id] = numbers[4]
        await handle_start_raid(message, user_id)
        return
    else:
        likes_target[chat_id] = likes_default_target[chat_id]
        retweets_target[chat_id] = retweets_default_target[chat_id]
        replies_target[chat_id] = replies_default_target[chat_id]
        views_target[chat_id] = views_default_target[chat_id]
        bookmarks_target[chat_id] = bookmarks_default_target[chat_id]
        link[chat_id] = message_text

    await update_likes_target(chat_id, likes_target[chat_id])
    await update_retweets_target(chat_id, retweets_target[chat_id])
    await update_replies_target(chat_id, replies_target[chat_id])
    await update_views_target(chat_id, views_target[chat_id])
    await update_bookmarks_target(chat_id, bookmarks_target[chat_id])

    member = await message.bot.get_chat_member(chat_id, user_id)
    if member.status not in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}:
        return  # User is not an admin, ignore message

    if match:
        formatted = (
            "⚙️ <b>Raid Options</b>\n\n"
            f"🔗 <b>Link:</b> {link[chat_id]}\n"
            f"💙 <b>Likes:</b> {likes_target[chat_id]}\n"
            f"🔄 <b>Retweets:</b> {retweets_target[chat_id]}\n"
            f"💬 <b>Replies:</b> {replies_target[chat_id]}\n"
            f"👀 <b>Views:</b> {views_target[chat_id]}\n"
            f"🔖 <b>Bookmarks:</b> {bookmarks_target[chat_id]}"
        )

        global keyboard_message
        keyboard_message = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💥 Start Raid 💥", callback_data="start raid"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🎨  Customization", callback_data="option_4"
                    )
                ],
                [InlineKeyboardButton(text="🎯 Targets", callback_data="option_2")],
                [InlineKeyboardButton(text="🚪 Close", callback_data="option_3")],
            ]
        )
        await message.answer(
            formatted,
            reply_markup=keyboard_message,
        )

    global resend_ongoing
    if raid_status.get(chat_id) and resend_ongoing:
        resend_ongoing = False
        await asyncio.sleep(12)
        try:
            await bot.delete_message(
                chat_id=chat_id, message_id=resend_message[chat_id]["message_id"]
            )
        except Exception as e:
            return
        file_type = resend_message[chat_id]["file_type"]
        file = resend_message[chat_id]["file"]
        caption = resend_message[chat_id]["text"]
        if file_type == "":
            bot_message = await message.answer(
                resend_message[chat_id]["text"], reply_markup=emoji_keyboard
            )
        elif file_type == ".jpg":
            bot_message = await message.answer_photo(
                file, caption=caption, reply_markup=emoji_keyboard
            )
        elif file_type == ".mp4":
            bot_message = await message.answer_video(
                file, caption=caption, reply_markup=emoji_keyboard
            )
        elif file_type == ".gif":
            bot_message = await message.answer_animation(
                file, caption=caption, reply_markup=emoji_keyboard
            )
        resend_message[chat_id]["message_id"] = bot_message.message_id
        resend_ongoing = True

        if raid_tweet.get(chat_id, True):
            await asyncio.sleep(8)
            custom_text = await get_custom_text(chat_id)
            if custom_text != "":
                custom_text += "\n\n"
            updated_caption = (
                "⚡️ <b>Raid Tweet</b>\n\n" + custom_text + percentages[chat_id]
            )
            file_type2 = await get_file_type(chat_id, "raid")
            file_path = os.path.join(
                MEDIA_DIR_RAID,
                str(chat_id) + (".mp4" if file_type2 == ".gif" else file_type2),
            )
            file = file if file_type2 == "" else FSInputFile(file_path)

            try:
                if file_type == "" and file_type2 == "":
                    await bot_message.edit_text(
                        updated_caption, reply_markup=emoji_keyboard
                    )
                    resend_message[chat_id]["file_type"] = file_type2
                elif file_type2 == "":
                    await bot_message.edit_caption(
                        caption=updated_caption, reply_markup=emoji_keyboard
                    )
                    resend_message[chat_id]["file_type"] = file_type
                else:
                    media_class = {
                        ".jpg": InputMediaPhoto,
                        ".mp4": InputMediaVideo,
                        ".gif": InputMediaAnimation,
                    }.get(file_type2)
                    await bot_message.edit_media(
                        media=media_class(media=file, caption=updated_caption),
                        reply_markup=emoji_keyboard,
                    )
                    resend_message[chat_id]["file_type"] = file_type2
                resend_message[chat_id]["text"] = updated_caption
                resend_message[chat_id]["file"] = file
                raid_tweet[chat_id] = False
            except Exception as e:
                pass
            await asyncio.sleep(1)


@dp.callback_query(lambda c: c.data.startswith("target_"))
async def handle_target(callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    target = callback_query.data.replace("target_", "")
    global keyboard_back, keyboard_default_back
    keyboard_back = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data="target_7")]
        ]
    )
    keyboard_default_back = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data="target_8")]
        ]
    )
    if target == "1":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "", "Likes", "likes", "", "Likes", likes_target[chat_id]
            ),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "2":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "", "Retweets", "retweets", "", "Retweets", retweets_target[chat_id]
            ),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "3":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "", "Replies", "replies", "", "Replies", replies_target[chat_id]
            ),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "4":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "", "Views", "views", "", "Views", views_target[chat_id]
            ),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "5":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "", "Bookmarks", "bookmarks", "", "Bookmarks", bookmarks_target[chat_id]
            ),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "6":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text="⚙️ <b>Raid Options</b>\n\n"
            f"🔗 <b>Link:</b> {link[chat_id]}\n"
            f"💙 <b>Likes:</b> {likes_target[chat_id]}\n"
            f"🔄 <b>Retweets:</b> {retweets_target[chat_id]}\n"
            f"💬 <b>Replies:</b> {replies_target[chat_id]}\n"
            f"👀 <b>Views:</b> {views_target[chat_id]}\n"
            f"🔖 <b>Bookmarks:</b> {bookmarks_target[chat_id]}",
            reply_markup=keyboard_message,
        )
        await callback_query.answer()
    elif target == "7":
        keyboard_target = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"💙 Likes ({likes_target[chat_id]})",
                        callback_data="target_1",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔄 Retweets ({retweets_target[chat_id]})",
                        callback_data="target_2",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"💬 Replies ({replies_target[chat_id]})",
                        callback_data="target_3",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"👀 Views ({views_target[chat_id]})",
                        callback_data="target_4",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔖 Bookmarks ({bookmarks_target[chat_id]})",
                        callback_data="target_5",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🎯 Change Default Targets", callback_data="target_8"
                    )
                ],
                [InlineKeyboardButton(text="🔙 Back", callback_data="target_6")],
            ]
        )
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_text.format(
                "", "either for each raid or as a default setting"
            ),
            reply_markup=keyboard_target,
        )
        await callback_query.answer()
    elif target == "8":
        keyboard_default_target = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"💙 Likes ({likes_default_target[chat_id]})",
                        callback_data="target_9",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔄 Retweets ({retweets_default_target[chat_id]})",
                        callback_data="target_10",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"💬 Replies ({replies_default_target[chat_id]})",
                        callback_data="target_11",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"👀 Views ({views_default_target[chat_id]})",
                        callback_data="target_12",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔖 Bookmarks ({bookmarks_default_target[chat_id]})",
                        callback_data="target_13",
                    )
                ],
                [InlineKeyboardButton(text=f"🔙 Back", callback_data="target_7")],
            ]
        )
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_text.format("Default", "in the default settings"),
            reply_markup=keyboard_default_target,
        )
        await callback_query.answer()
    elif target == "9":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default", "Likes", "likes", "default", "likes", likes_target[chat_id]
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "10":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default",
                "Retweets",
                "retweets",
                "default",
                "retweets",
                retweets_target[chat_id],
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "11":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default",
                "Replies",
                "replies",
                "default",
                "replies",
                replies_target[chat_id],
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "12":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default", "Views", "views", "default", "views", views_target[chat_id]
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "13":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default",
                "Bookmarks",
                "bookmarks",
                "default",
                "bookmarks",
                bookmarks_target[chat_id],
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()


async def handle_start_raid(message: Message, user_id: int):
    chat_id = message.chat.id

    # Get chat member status
    member = await bot.get_chat_member(chat_id, user_id)

    if member.status in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}:
        # x_data = x_bot.get_tweet_data(link[chat_id])
        x_data = {"1": 0}
        likes = x_data.get("Likes", 2)
        retweets = x_data.get("Retweets", 4)
        replies = x_data.get("Replies", 2)
        views = x_data.get("Views", 2)
        bookmarks = x_data.get("Bookmarks", 2)
        likes_percentage = calculate_percentage(likes, likes_target[chat_id])
        retweets_percentage = calculate_percentage(retweets, retweets_target[chat_id])
        replies_percentage = calculate_percentage(replies, replies_target[chat_id])
        views_percentage = calculate_percentage(views, views_target[chat_id])
        bookmarks_percentage = calculate_percentage(
            bookmarks, bookmarks_target[chat_id]
        )
        emoji_buttons = [
            InlineKeyboardButton(text="💬", callback_data="comment"),
            InlineKeyboardButton(text="🔁", callback_data="retweet"),
            InlineKeyboardButton(text="💙", callback_data="like"),
            InlineKeyboardButton(text="🏷️", callback_data="bookmark"),
            InlineKeyboardButton(text="👊", callback_data="smash"),
        ]
        trending_buttons = [
            InlineKeyboardButton(text="🔵", callback_data="trending_1"),
            InlineKeyboardButton(text="🔵", callback_data="trending_2"),
            InlineKeyboardButton(text="🔵", callback_data="trending_3"),
            InlineKeyboardButton(text="🔵", callback_data="trending_4"),
            InlineKeyboardButton(text="🔵", callback_data="trending_5"),
        ]
        global emoji_keyboard
        emoji_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[emoji_buttons, trending_buttons]
        )

        percentages[chat_id] = (
            (
                ""
                if likes_target[chat_id] == 0
                else f"{get_emoji(likes_percentage)} Likes <b>{likes} | {likes_target[chat_id]}</b>  [{'💯' if likes_percentage==100 else likes_percentage }%]\n"
            )
            + (
                ""
                if retweets_target[chat_id] == 0
                else f"{get_emoji(retweets_percentage)} Retweets <b>{retweets} | {retweets_target[chat_id]}</b>  [{'💯' if retweets_percentage==100 else retweets_percentage }%]\n"
            )
            + (
                ""
                if replies_target[chat_id] == 0
                else f"{get_emoji(replies_percentage)} Replies <b>{replies} | {replies_target[chat_id]}</b>  [{'💯' if replies_percentage==100 else replies_percentage }%]\n"
            )
            + (
                ""
                if views_target[chat_id] == 0
                else f"{get_emoji(views_percentage)} Views <b>{views} | {views_target[chat_id]}</b>  [{'💯' if views_percentage==100 else views_percentage}%]\n"
            )
            + (
                ""
                if bookmarks_target[chat_id] == 0
                else f"{get_emoji(bookmarks_percentage)} Bookmarks <b>{bookmarks} | {bookmarks_target[chat_id]}</b>  [{'💯' if bookmarks_percentage==100 else bookmarks_percentage}%]\n"
            )
            + f"\n{link[chat_id]}\n\n"
        )

        if raid_status.get(chat_id, False):
            bot_message = await message.answer(
                "<b>❌ There is already an ongoing raid in this group. Please use /stop to stop it.</b>"
            )
            await message.delete()
            await asyncio.sleep(5)
            await bot_message.delete()
            return

        if (
            likes_percentage == 100
            and retweets_percentage == 100
            and replies_percentage == 100
        ):
            raid_message = (
                "🎊 Raid Ended - Targets Reached!\n\n"
                + percentages[chat_id]
                + "⏰ Duration: 0 minutes"
            )
            raid_status[chat_id] = False
        else:
            raid_status[chat_id] = True
            timer[chat_id] = datetime.now()
            raid_message = "⚡️ <b>Raid Started!</b>\n\n" + percentages[chat_id]
        await message.delete()

        file_name = str(chat_id)
        if raid_status[chat_id]:
            file_type = await get_file_type(chat_id, "start")
            if file_type == "":
                file_type = await get_file_type(chat_id, "raid")
                file_path = os.path.join(
                    MEDIA_DIR_RAID,
                    file_name + (".mp4" if file_type == ".gif" else file_type),
                )
                file = None if file_type == "" else FSInputFile(file_path)
            else:
                file_path = os.path.join(
                    MEDIA_DIR_START,
                    file_name + (".mp4" if file_type == ".gif" else file_type),
                )
                file = None if file_type == "" else FSInputFile(file_path)
        else:
            file_type = await get_file_type(chat_id, "end")
            if file_type == "":
                file_type = await get_file_type(chat_id, "raid")
                if file_type == "":
                    file_type = await get_file_type(chat_id, "start")
                    file_path = os.path.join(
                        MEDIA_DIR_START,
                        file_name + (".mp4" if file_type == ".gif" else file_type),
                    )
                    file = None if file_type == "" else FSInputFile(file_path)
                else:
                    file_path = os.path.join(
                        MEDIA_DIR_RAID,
                        file_name + (".mp4" if file_type == ".gif" else file_type),
                    )
                    file = None if file_type == "" else FSInputFile(file_path)
            else:
                file_path = os.path.join(
                    MEDIA_DIR_END,
                    file_name + (".mp4" if file_type == ".gif" else file_type),
                )
                file = None if file_type == "" else FSInputFile(file_path)

        if file_type == ".jpg":
            bot_message = await message.answer_photo(
                file, caption=raid_message, reply_markup=emoji_keyboard
            )
        elif file_type == ".mp4":
            bot_message = await message.answer_video(
                file, caption=raid_message, reply_markup=emoji_keyboard
            )
        elif file_type == ".gif":
            bot_message = await message.answer_animation(
                file, caption=raid_message, reply_markup=emoji_keyboard
            )
        else:
            bot_message = await message.answer(
                raid_message, reply_markup=emoji_keyboard
            )
        resend_message[chat_id] = {
            "message_id": bot_message.message_id,
            "text": raid_message,
            "file": file if file else None,
            "file_type": file_type,
        }

        raid_tweet[chat_id] = True

        if raid_status[chat_id]:
            await asyncio.sleep(20)
            file_type2 = await get_file_type(chat_id, "raid")
            file_path = os.path.join(
                MEDIA_DIR_RAID,
                file_name + (".mp4" if file_type2 == ".gif" else file_type2),
            )
            file = file if file_type2 == "" else FSInputFile(file_path)
            custom_text = await get_custom_text(chat_id)
            if custom_text != "":
                custom_text += "\n\n"
            updated_caption = (
                "⚡️ <b>Raid Tweet</b>\n\n" + custom_text + percentages[chat_id]
            )

            try:
                if file_type == "" and file_type2 == "":
                    await bot_message.edit_text(
                        updated_caption, reply_markup=emoji_keyboard
                    )
                    resend_message[chat_id]["file_type"] = file_type2
                elif file_type2 == "":
                    await bot_message.edit_caption(
                        caption=updated_caption, reply_markup=emoji_keyboard
                    )
                    resend_message[chat_id]["file_type"] = file_type
                else:
                    media_class = {
                        ".jpg": InputMediaPhoto,
                        ".mp4": InputMediaVideo,
                        ".gif": InputMediaAnimation,
                    }.get(file_type2)
                    await bot_message.edit_media(
                        media=media_class(media=file, caption=updated_caption),
                        reply_markup=emoji_keyboard,
                    )
                    resend_message[chat_id]["file_type"] = file_type2
                resend_message[chat_id]["text"] = updated_caption
                resend_message[chat_id]["file"] = file if file else None
                raid_tweet[chat_id] = False
            except Exception as e:
                pass

            await asyncio.sleep(1)

    else:
        await message.answer(
            "🛑 You must be an admin to interact with WAOxrpBot.", show_alert=True
        )


@router.callback_query(F.data == "start raid")
async def star_raid_callback(callback: CallbackQuery):
    await callback.answer()
    await handle_start_raid(callback.message, callback.from_user.id)


@dp.callback_query(lambda c: c.data.startswith("option"))
async def process_callback(callback_query: CallbackQuery):
    option = callback_query.data.replace("option_", "")
    chat_id = callback_query.message.chat.id

    if option == "2":
        global keyboard_target
        keyboard_target = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"💙 Likes ({likes_target[chat_id]})",
                        callback_data="target_1",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔄 Retweets ({retweets_target[chat_id]})",
                        callback_data="target_2",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"💬 Replies ({replies_target[chat_id]})",
                        callback_data="target_3",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"👀 Views ({views_target[chat_id]})",
                        callback_data="target_4",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔖 Bookmarks ({bookmarks_target[chat_id]})",
                        callback_data="target_5",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🎯 Change Default Targets", callback_data="target_8"
                    )
                ],
                [InlineKeyboardButton(text="🔙 Back", callback_data="target_6")],
            ]
        )
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=targets_text.format(
                "", "either for each raid or as a default setting"
            ),
            reply_markup=keyboard_target,
        )
        await callback_query.answer()
    elif option == "3":
        await bot.delete_message(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
        )
    elif option == "4":
        global keyboard_customization
        keyboard_customization = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚀  Start Media", callback_data="customization_1"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🖼  Raid Media", callback_data="customization_2"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🏁  End Media",
                        callback_data="customization_3",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📝  Custom Text",
                        callback_data="customization_4",
                    )
                ],
                [InlineKeyboardButton(text="🔙 Back", callback_data="target_6")],
            ]
        )
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=callback_query.message.message_id,
            text=customization_text.format(
                "",
                "You can set custom media for ongoing raids and end media for when a raid is completed",
            ),
            reply_markup=keyboard_customization,
        )
        await callback_query.answer()


@router.callback_query(F.data.startswith("customization_"))
async def process_callback(callback: CallbackQuery):
    option = callback.data.replace("customization_", "")
    chat_id = callback.message.chat.id
    file_type_raid = await get_file_type(chat_id, "raid")
    file_path_raid = os.path.join(
        MEDIA_DIR_RAID,
        str(chat_id) + (".mp4" if file_type_raid == ".gif" else file_type_raid),
    )
    is_file_raid = os.path.isfile(file_path_raid)

    file_type_start = await get_file_type(chat_id, "start")
    file_path_start = os.path.join(
        MEDIA_DIR_START,
        str(chat_id) + (".mp4" if file_type_start == ".gif" else file_type_start),
    )
    is_file_start = os.path.isfile(file_path_start)

    file_type_end = await get_file_type(chat_id, "end")
    file_path_end = os.path.join(
        MEDIA_DIR_END,
        str(chat_id) + (".mp4" if file_type_end == ".gif" else file_type_end),
    )
    is_file_end = os.path.isfile(file_path_end)

    if option == "1":
        keyboard_start_media = InlineKeyboardMarkup(
            inline_keyboard=[
                (
                    [
                        InlineKeyboardButton(
                            text="❌ Remove File", callback_data="customization_5"
                        )
                    ]
                    if is_file_start
                    else []
                ),
                [
                    InlineKeyboardButton(
                        text="🔙 Back",
                        callback_data="customization_6",
                    )
                ],
            ]
        )
        file_type_start = await get_file_type(chat_id, "start")
        if file_type_start == ".jpg":
            current_type = "Image"
        elif file_type_start == ".mp4":
            current_type = "Video"
        elif file_type_start == ".gif":
            current_type = "GIF"
        await callback.message.edit_text(
            customization_text.format(
                "> Start Media",
                (
                    "Reply to this message with a video or image to change the current media used for raids in this group"
                    if is_file_start
                    else "Reply to this message with a video or image to set it as media for raids in this group"
                ),
            )
            + ("\n\n<b>Current Media:</b> " + current_type if is_file_start else ""),
            reply_markup=keyboard_start_media,
        )
    elif option == "2":
        keyboard_raid_media = InlineKeyboardMarkup(
            inline_keyboard=[
                (
                    [
                        InlineKeyboardButton(
                            text="❌ Remove File", callback_data="customization_7"
                        )
                    ]
                    if is_file_raid
                    else []
                ),
                [
                    InlineKeyboardButton(
                        text="🔙 Back",
                        callback_data="customization_6",
                    )
                ],
            ]
        )
        file_type_raid = await get_file_type(chat_id, "raid")
        if file_type_raid == ".jpg":
            current_type = "Image"
        elif file_type_raid == ".mp4":
            current_type = "Video"
        elif file_type_raid == ".gif":
            current_type = "GIF"
        await callback.message.edit_text(
            customization_text.format(
                "> Raid Media",
                (
                    "Reply to this message with a video or image to change the current media used for ongoing raids in this group"
                    if is_file_raid
                    else "Reply to this message with a video or image to set it as media for ongoing raids in this group"
                ),
            )
            + ("\n\n<b>Current Media:</b> " + current_type if is_file_raid else ""),
            reply_markup=keyboard_raid_media,
        )
    elif option == "3":
        keyboard_end_media = InlineKeyboardMarkup(
            inline_keyboard=[
                (
                    [
                        InlineKeyboardButton(
                            text="❌ Remove File", callback_data="customization_8"
                        )
                    ]
                    if is_file_end
                    else []
                ),
                [
                    InlineKeyboardButton(
                        text="🔙 Back",
                        callback_data="customization_6",
                    )
                ],
            ]
        )
        file_type_end = await get_file_type(chat_id, "end")
        if file_type_end == ".jpg":
            current_type = "Image"
        elif file_type_end == ".mp4":
            current_type = "Video"
        elif file_type_end == ".gif":
            current_type = "GIF"
        await callback.message.edit_text(
            customization_text.format(
                "> End Media",
                (
                    "Reply to this message with a video or image to change the current media used for raids in this group"
                    if is_file_end
                    else "Reply to this message with a video or image to set it as media for raids in this group"
                ),
            )
            + ("\n\n<b>Current Media:</b> " + current_type if is_file_end else ""),
            reply_markup=keyboard_end_media,
        )
    elif option == "4":
        custom_text = await get_custom_text(chat_id)
        global keyboard_custom_text, remove_custom_text, back, buttons_custom_text
        remove_custom_text = InlineKeyboardButton(
            text="❌ Remove Custom Text",
            callback_data="customization_9",
        )
        back = InlineKeyboardButton(
            text="🔙 Back",
            callback_data="customization_6",
        )
        buttons_custom_text = [[back]]
        message_custom_text = "Please reply to this message with your custom text."
        if custom_text != "":
            buttons_custom_text.insert(0, [remove_custom_text])
            message_custom_text = "Please reply to this message with your custom text to change the current message used for ongoing raids in this group."
        keyboard_custom_text = InlineKeyboardMarkup(inline_keyboard=buttons_custom_text)
        await callback.message.edit_text(
            message_custom_text, reply_markup=keyboard_custom_text
        )

    elif option == "5":
        await save_media(chat_id, "", "start")
        await callback.message.edit_text(
            customization_text.format(
                "",
                "You can set custom media for ongoing raids and end media for when a raid is completed",
            ),
            reply_markup=keyboard_customization,
        )
    elif option == "6":
        await callback.message.edit_text(
            customization_text.format(
                "",
                "You can set custom media for ongoing raids and end media for when a raid is completed",
            ),
            reply_markup=keyboard_customization,
        )
    elif option == "7":
        await save_media(chat_id, "", "raid")
        await callback.message.edit_text(
            customization_text.format(
                "",
                "You can set custom media for ongoing raids and end media for when a raid is completed",
            ),
            reply_markup=keyboard_customization,
        )
    elif option == "8":
        await save_media(chat_id, "", "end")
        await callback.message.edit_text(
            customization_text.format(
                "",
                "You can set custom media for ongoing raids and end media for when a raid is completed",
            ),
            reply_markup=keyboard_customization,
        )
    elif option == "9":
        await update_custom_text(chat_id, "")
        await callback.message.edit_text(
            customization_text.format(
                "",
                "You can set custom media for ongoing raids and end media for when a raid is completed",
            ),
            reply_markup=keyboard_customization,
        )


async def main():
    print("🚀 Bot is up and running! Waiting for updates...")
    dp.include_router(router)
    # await init_db()
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
