import x_bot
from utils import *
from config import BOT_TOKEN
from db import *

from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile,
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


@dp.message(F.text == "/stop")
async def stop_command(message: types.Message):
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
        await message.answer(
            "🛑 <b>Raid Ended - Stopped by admin</b>\n\n" + percentages
        )
    else:
        await message.answer("❌ <b>There is no ongoing raid in this group</b>")


@dp.message(F.reply_to_message)
async def reply_handler(message: types.Message):
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
                        global likes_target
                        global likes_default_target
                        if likes_default_target == int(message.text):
                            bot_message = await message.answer(
                                same_value.format("Default", "Likes")
                            )
                            await asyncio.sleep(3)
                            await bot_message.delete()
                            await bot.delete_message(
                                chat_id=message.chat.id, message_id=message.message_id
                            )
                            return
                        likes_default_target = int(message.text)
                        await update_likes_default_target(chat_id, likes_default_target)
                        likes_target = likes_default_target
                        await update_likes_target(chat_id, likes_target)
                        await bot.edit_message_text(
                            chat_id=message.reply_to_message.chat.id,
                            message_id=message.reply_to_message.message_id,
                            text=target_saved.format(
                                "likes", "default ", "Likes", likes_target
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
                        global retweets_target
                        global retweets_default_target
                        if retweets_default_target == int(message.text):
                            bot_message = await message.answer(
                                same_value.format("Default", "Retweets")
                            )
                            await asyncio.sleep(3)
                            await bot_message.delete()
                            await bot.delete_message(
                                chat_id=message.chat.id, message_id=message.message_id
                            )
                            return
                        retweets_default_target = int(message.text)
                        await update_retweets_default_target(
                            chat_id, retweets_default_target
                        )
                        retweets_target = retweets_default_target
                        await update_retweets_target(chat_id, retweets_target)
                        await bot.edit_message_text(
                            chat_id=message.reply_to_message.chat.id,
                            message_id=message.reply_to_message.message_id,
                            text=target_saved.format(
                                "retweets",
                                "default ",
                                "Retweets",
                                retweets_target,
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
                        global replies_target
                        global replies_default_target
                        if replies_default_target == int(message.text):
                            bot_message = await message.answer(
                                same_value.format("Default", "Replies")
                            )
                            await asyncio.sleep(3)
                            await bot_message.delete()
                            await bot.delete_message(
                                chat_id=message.chat.id, message_id=message.message_id
                            )
                            return
                        replies_default_target = int(message.text)
                        await update_replies_default_target(
                            chat_id, replies_default_target
                        )
                        replies_target = replies_default_target
                        await update_replies_target(chat_id, replies_target)
                        await bot.edit_message_text(
                            chat_id=message.reply_to_message.chat.id,
                            message_id=message.reply_to_message.message_id,
                            text=target_saved.format(
                                "replies",
                                "default ",
                                "Replies",
                                replies_target,
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
                        global views_target
                        global views_default_target
                        if views_default_target == int(message.text):
                            bot_message = await message.answer(
                                same_value.format("Default", "Views")
                            )
                            await asyncio.sleep(3)
                            await bot_message.delete()
                            await bot.delete_message(
                                chat_id=message.chat.id, message_id=message.message_id
                            )
                            return
                        views_default_target = int(message.text)
                        await update_views_default_target(chat_id, views_default_target)
                        views_target = views_default_target
                        await update_views_target(chat_id, views_target)
                        await bot.edit_message_text(
                            chat_id=message.reply_to_message.chat.id,
                            message_id=message.reply_to_message.message_id,
                            text=target_saved.format(
                                "views", "default ", "Views", views_target
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
                        global bookmarks_target
                        global bookmarks_default_target
                        if bookmarks_default_target == int(message.text):
                            bot_message = await message.answer(
                                same_value.format("Default", "Bookmarks")
                            )
                            await asyncio.sleep(3)
                            await bot_message.delete()
                            await bot.delete_message(
                                chat_id=message.chat.id, message_id=message.message_id
                            )
                            return
                        bookmarks_default_target = int(message.text)
                        await update_bookmarks_default_target(
                            chat_id, bookmarks_default_target
                        )
                        bookmarks_target = bookmarks_default_target
                        await update_bookmarks_target(chat_id, bookmarks_target)
                        await bot.edit_message_text(
                            chat_id=message.reply_to_message.chat.id,
                            message_id=message.reply_to_message.message_id,
                            text=target_saved.format(
                                "bookmarks",
                                "default ",
                                "Bookmarks",
                                bookmarks_target,
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
                    if likes_target == int(message.text):
                        bot_message = await message.answer(
                            same_value.format("", "Likes")
                        )
                        await asyncio.sleep(3)
                        await bot_message.delete()
                        await bot.delete_message(
                            chat_id=message.chat.id, message_id=message.message_id
                        )
                        return
                    likes_target = int(message.text)
                    await update_likes_target(chat_id, likes_target)
                    await bot.edit_message_text(
                        chat_id=message.reply_to_message.chat.id,
                        message_id=message.reply_to_message.message_id,
                        text=target_saved.format("likes", "", "Likes", likes_target),
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
                    if retweets_target == int(message.text):
                        bot_message = await message.answer(
                            same_value.format("", "Retweets")
                        )
                        await asyncio.sleep(3)
                        await bot_message.delete()
                        await bot.delete_message(
                            chat_id=message.chat.id, message_id=message.message_id
                        )
                        return
                    retweets_target = int(message.text)
                    await update_retweets_target(chat_id, retweets_target)
                    await bot.edit_message_text(
                        chat_id=message.reply_to_message.chat.id,
                        message_id=message.reply_to_message.message_id,
                        text=target_saved.format(
                            "retweets", "", "Retweets", retweets_target
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
                    if replies_target == int(message.text):
                        bot_message = await message.answer(
                            same_value.format("", "Replies")
                        )
                        await asyncio.sleep(3)
                        await bot_message.delete()
                        await bot.delete_message(
                            chat_id=message.chat.id, message_id=message.message_id
                        )
                        return
                    replies_target = int(message.text)
                    await update_replies_target(chat_id, replies_target)
                    await bot.edit_message_text(
                        chat_id=message.reply_to_message.chat.id,
                        message_id=message.reply_to_message.message_id,
                        text=target_saved.format(
                            "replies", "", "Replies", replies_target
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
                    if views_target == int(message.text):
                        bot_message = await message.answer(
                            same_value.format("", "Views")
                        )
                        await asyncio.sleep(3)
                        await bot_message.delete()
                        await bot.delete_message(
                            chat_id=message.chat.id, message_id=message.message_id
                        )
                        return
                    views_target = int(message.text)
                    await update_views_target(chat_id, views_target)
                    await bot.edit_message_text(
                        chat_id=message.reply_to_message.chat.id,
                        message_id=message.reply_to_message.message_id,
                        text=target_saved.format("views", "", "Views", views_target),
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
                    if bookmarks_target == int(message.text):
                        bot_message = await message.answer(
                            same_value.format("", "Bookmarks")
                        )
                        await asyncio.sleep(3)
                        await bot_message.delete()
                        await bot.delete_message(
                            chat_id=message.chat.id, message_id=message.message_id
                        )
                        return
                    bookmarks_target = int(message.text)
                    await update_bookmarks_target(chat_id, bookmarks_target)
                    await bot.edit_message_text(
                        chat_id=message.reply_to_message.chat.id,
                        message_id=message.reply_to_message.message_id,
                        text=target_saved.format(
                            "bookmarks", "", "Bookmarks", bookmarks_target
                        ),
                        reply_markup=keyboard_back,
                    )
                except ValueError:
                    bot_message = await message.answer(
                        "❌ <b>Invalid input. Please enter a valid number.</b>"
                    )
                    await asyncio.sleep(5)
                    await bot_message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

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

        if file_path:
            await save_image(chat_id, file_type)
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
                            text="❌ Remove File", callback_data="customization_5"
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
async def handle_message(message: types.Message):
    # Check if message has text
    message_text = message.text
    chat_id = message.chat.id

    if not message_text:
        return

    # Check if the sender is an admin
    user_id = message.from_user.id

    member = await message.bot.get_chat_member(chat_id, user_id)
    if member.status not in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}:
        return  # User is not an admin, ignore message

    match = TWITTER_LINK_PATTERN.search(message_text)
    if match:
        global link
        link = message_text
        global likes_target, retweets_target, replies_target, views_target, bookmarks_target
        global likes_default_target, retweets_default_target, replies_default_target, views_default_target, bookmarks_default_target
        likes_default_target = await get_likes_default_target(chat_id)
        retweets_default_target = await get_retweets_default_target(chat_id)
        replies_default_target = await get_replies_default_target(chat_id)
        views_default_target = await get_views_default_target(chat_id)
        bookmarks_default_target = await get_bookmarks_default_target(chat_id)
        likes_target = likes_default_target
        retweets_target = retweets_default_target
        replies_target = replies_default_target
        views_target = views_default_target
        bookmarks_target = bookmarks_default_target
        await update_likes_target(chat_id, likes_target)
        await update_retweets_target(chat_id, retweets_target)
        await update_replies_target(chat_id, replies_target)
        await update_views_target(chat_id, views_target)
        await update_bookmarks_target(chat_id, bookmarks_target)

        formatted = (
            "⚙️ <b>Raid Options</b>\n\n"
            f"🔗 <b>Link:</b> {link}\n"
            f"💙 <b>Likes:</b> {likes_target}\n"
            f"🔄 <b>Retweets:</b> {retweets_target}\n"
            f"💬 <b>Replies:</b> {replies_target}\n"
            f"👀 <b>Views:</b> {views_target}\n"
            f"🔖 <b>Bookmarks:</b> {bookmarks_target}"
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
        await bot.delete_message(
            chat_id=chat_id, message_id=resend_message[chat_id]["message_id"]
        )
        bot_message = await message.answer(resend_message[chat_id]["text"])
        resend_message[chat_id]["message_id"] = bot_message.message_id
        resend_ongoing = True

        await asyncio.sleep(8)
        updated_caption = "⚡️ <b>Raid Tweet</b>\n\n" + percentages

        try:
            # if file_type == "":
            await bot_message.edit_text(updated_caption)
            resend_message[chat_id]["text"] = updated_caption
            # else:
            # await bot_message.edit_caption(caption=updated_caption)
        except Exception as e:
            pass
        await asyncio.sleep(1)


@dp.callback_query(lambda c: c.data.startswith("target_"))
async def handle_target(callback_query: types.CallbackQuery):
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
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format("", "Likes", "likes", "", "Likes", likes_target),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "2":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "", "Retweets", "retweets", "", "Retweets", retweets_target
            ),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "3":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "", "Replies", "replies", "", "Replies", replies_target
            ),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "4":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format("", "Views", "views", "", "Views", views_target),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "5":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "", "Bookmarks", "bookmarks", "", "Bookmarks", bookmarks_target
            ),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "6":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="⚙️ <b>Raid Options</b>\n\n"
            f"🔗 <b>Link:</b> {link}\n"
            f"💙 <b>Likes:</b> {likes_target}\n"
            f"🔄 <b>Retweets:</b> {retweets_target}\n"
            f"💬 <b>Replies:</b> {replies_target}\n"
            f"👀 <b>Views:</b> {views_target}\n"
            f"🔖 <b>Bookmarks:</b> {bookmarks_target}",
            reply_markup=keyboard_message,
        )
        await callback_query.answer()
    elif target == "7":
        keyboard_target = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"💙 Likes ({likes_target})", callback_data="target_1"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔄 Retweets ({retweets_target})",
                        callback_data="target_2",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"💬 Replies ({replies_target})", callback_data="target_3"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"👀 Views ({views_target})", callback_data="target_4"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔖 Bookmarks ({bookmarks_target})",
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
            chat_id=callback_query.message.chat.id,
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
                        text=f"💙 Likes ({likes_default_target})",
                        callback_data="target_9",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔄 Retweets ({retweets_default_target})",
                        callback_data="target_10",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"💬 Replies ({replies_default_target})",
                        callback_data="target_11",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"👀 Views ({views_default_target})",
                        callback_data="target_12",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔖 Bookmarks ({bookmarks_default_target})",
                        callback_data="target_13",
                    )
                ],
                [InlineKeyboardButton(text=f"🔙 Back", callback_data="target_7")],
            ]
        )
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_text.format("Default", "in the default settings"),
            reply_markup=keyboard_default_target,
        )
        await callback_query.answer()
    elif target == "9":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default", "Likes", "likes", "default", "likes", likes_target
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "10":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default",
                "Retweets",
                "retweets",
                "default",
                "retweets",
                retweets_target,
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "11":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default", "Replies", "replies", "default", "replies", replies_target
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "12":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default", "Views", "views", "default", "views", views_target
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "13":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default",
                "Bookmarks",
                "bookmarks",
                "default",
                "bookmarks",
                bookmarks_target,
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()


@router.callback_query(F.data == "start raid")
async def star_raid_callback(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    user_id = callback.from_user.id

    # Get chat member status
    member = await bot.get_chat_member(chat_id, user_id)

    if member.status in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}:
        # x_data = x_bot.get_tweet_data(link)
        x_data = {"1": 0}
        likes = x_data.get("Likes", 2)
        retweets = x_data.get("Retweets", 4)
        replies = x_data.get("Replies", 2)
        views = x_data.get("Views", 2)
        bookmarks = x_data.get("Bookmarks", 2)
        likes_percentage = calculate_percentage(likes, likes_target)
        retweets_percentage = calculate_percentage(retweets, retweets_target)
        replies_percentage = calculate_percentage(replies, replies_target)
        views_percentage = calculate_percentage(views, views_target)
        bookmarks_percentage = calculate_percentage(bookmarks, bookmarks_target)
        global percentages
        percentages = (
            f"{get_emoji(likes_percentage)} Likes <b>{likes} | {likes_target}</b>  [{'💯' if likes_percentage==100 else likes_percentage }%]\n"
            + f"{get_emoji(retweets_percentage)} Retweets <b>{retweets} | {retweets_target}</b>  [{'💯' if retweets_percentage==100 else retweets_percentage }%]\n"
            + f"{get_emoji(replies_percentage)} Replies <b>{replies} | {replies_target}</b>  [{'💯' if replies_percentage==100 else replies_percentage}%]\n"
            + (
                ""
                if views_target == 0
                else f"{get_emoji(views_percentage)} Views <b>{views} | {views_target}</b>  [{'💯' if views_percentage==100 else views_percentage}%]\n"
            )
            + (
                ""
                if bookmarks_target == 0
                else f"{get_emoji(bookmarks_percentage)} Bookmarks <b>{bookmarks} | {bookmarks_target}</b>  [{'💯' if bookmarks_percentage==100 else bookmarks_percentage}%]\n"
            )
            + f"\n{link}\n\n"
        )

        if raid_status.get(chat_id, False):
            bot_message = await callback.message.answer(
                "<b>❌ There is already an ongoing raid in this group. Please use /stop to stop it.</b>"
            )
            await callback.message.delete()
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
                + percentages
                + "⏰ Duration: 0 minutes"
            )
            raid_status[chat_id] = False
        else:
            chat_id = callback.message.chat.id
            raid_status[chat_id] = True
            raid_message = "⚡️ <b>Raid Started!</b>\n\n" + percentages
        await callback.message.delete()

        file_name = str(chat_id)
        file_type = await get_file_type(chat_id)
        file_path = os.path.join(
            MEDIA_DIR_RAID, file_name + (".mp4" if file_type == ".gif" else file_type)
        )
        file = None if file_type == "" else FSInputFile(file_path)
        if file_type == ".jpg":
            bot_message = await callback.message.answer_photo(
                file, caption=raid_message
            )
        elif file_type == ".mp4":
            bot_message = await callback.message.answer_video(
                file, caption=raid_message
            )
        elif file_type == ".gif":
            bot_message = await callback.message.answer_animation(
                file, caption=raid_message
            )
        else:
            bot_message = await callback.message.answer(raid_message)
        resend_message[chat_id] = {
            "message_id": bot_message.message_id,
            "text": raid_message,
            "file": file if file else None,
        }

        await callback.answer()
        await asyncio.sleep(20)
        updated_caption = "⚡️ <b>Raid Tweet</b>\n\n" + percentages

        try:
            if file_type == "":
                await bot_message.edit_text(updated_caption)
            else:
                await bot_message.edit_caption(caption=updated_caption)
            resend_message[chat_id]["text"] = updated_caption
        except Exception as e:
            pass
        await asyncio.sleep(1)

    else:
        await callback.answer(
            "🛑 You must be an admin to interact with WAOxrpBot.", show_alert=True
        )


@dp.callback_query(lambda c: c.data.startswith("option"))
async def process_callback(callback_query: types.CallbackQuery):
    option = callback_query.data.replace("option_", "")

    if option == "2":
        global keyboard_target
        keyboard_target = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"💙 Likes ({likes_target})", callback_data="target_1"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔄 Retweets ({retweets_target})",
                        callback_data="target_2",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"💬 Replies ({replies_target})", callback_data="target_3"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"👀 Views ({views_target})", callback_data="target_4"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔖 Bookmarks ({bookmarks_target})",
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
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_text.format(
                "", "either for each raid or as a default setting"
            ),
            reply_markup=keyboard_target,
        )
        await callback_query.answer()
    elif option == "3":
        await bot.delete_message(
            chat_id=callback_query.message.chat.id,
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
            chat_id=callback_query.message.chat.id,
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
    file_type_raid = await get_file_type(callback.message.chat.id)
    file_path_raid = os.path.join(
        MEDIA_DIR_RAID,
        str(callback.message.chat.id)
        + (".mp4" if file_type_raid == ".gif" else file_type_raid),
    )
    is_file_raid = os.path.isfile(file_path_raid)

    file_type_start = await get_file_type(callback.message.chat.id)
    file_path_start = os.path.join(
        MEDIA_DIR_START,
        str(callback.message.chat.id)
        + (".mp4" if file_type_start == ".gif" else file_type_start),
    )
    is_file_start = os.path.isfile(file_path_start)

    file_type_end = await get_file_type(callback.message.chat.id)
    file_path_end = os.path.join(
        MEDIA_DIR_END,
        str(callback.message.chat.id)
        + (".mp4" if file_type_end == ".gif" else file_type_end),
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
        file_type_start = await get_file_type(callback.message.chat.id)
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
                            text="❌ Remove File", callback_data="customization_5"
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
        file_type_raid = await get_file_type(callback.message.chat.id)
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
                            text="❌ Remove File", callback_data="customization_5"
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
        file_type_end = await get_file_type(callback.message.chat.id)
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
    elif option == "5":
        await save_image(callback.message.chat.id, "")
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


async def main():
    print("🚀 Bot is up and running! Waiting for updates...")
    dp.include_router(router)
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
