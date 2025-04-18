import x_bot
from utils import (
    TWITTER_LINK_PATTERN,
    raid_status,
    targets_text,
    targets_reply,
    calculate_percentage,
    get_emoji,
    write_values,
    read_values,
)
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
(
    likes_default_target,
    retweets_default_target,
    replies_default_target,
    views_default_target,
    bookmarks_default_target,
) = read_values()
likes_target = likes_default_target
retweets_target = retweets_default_target
replies_target = replies_default_target
views_target = views_default_target
bookmarks_target = bookmarks_default_target


@dp.message(F.text == "/stop")
async def stop_command(message: types.Message):
    chat_id = message.chat.id
    if raid_status.get(chat_id):
        raid_status[chat_id] = False
        await message.answer(
            "🛑 <b>Raid Ended - Stopped by admin</b>\n\n" + percentages
        )
    else:
        await message.answer("❌ <b>There is no ongoing raid in this group</b>")


@dp.message(F.reply_to_message)
async def reply_handler(message: types.Message):
    bot_id = (await bot.me()).id
    message_reply = message.reply_to_message.text
    if message.reply_to_message.from_user.id == bot_id:
        if "Default" in message_reply:
            if "Likes" in message_reply:
                try:
                    global likes_target
                    global likes_default_target
                    likes_default_target = int(message.text)
                    likes_target = likes_default_target
                    bot_message = await message.answer(
                        f"💙 <b>Default Likes</b> updated to {likes_target}"
                    )
                    await asyncio.sleep(3)
                    await bot.edit_message_text(
                        chat_id=message.reply_to_message.chat.id,
                        message_id=message.reply_to_message.message_id,
                        text=targets_reply.format(
                            "Default", "Likes", "likes", "Likes", likes_target
                        ),
                        reply_markup=keyboard_default_back,
                    )
                except ValueError:
                    bot_message = await message.answer(
                        "❌ <b>Invalid input. Please enter a valid number.</b>"
                    )
                    await asyncio.sleep(5)
            elif "Retweets" in message_reply:
                try:
                    global retweets_target
                    global retweets_default_target
                    retweets_default_target = int(message.text)
                    retweets_target = retweets_default_target
                    bot_message = await message.answer(
                        f"🔄 <b>Default Retweets</b> updated to {retweets_target}"
                    )
                    await asyncio.sleep(3)
                    await bot.edit_message_text(
                        chat_id=message.reply_to_message.chat.id,
                        message_id=message.reply_to_message.message_id,
                        text=targets_reply.format(
                            "Default", "Retweets", "retweets", "Retweets", retweets_target
                        ),
                        reply_markup=keyboard_default_back,
                    )
                except ValueError:
                    bot_message = await message.answer(
                        "❌ <b>Invalid input. Please enter a valid number.</b>"
                    )
                    await asyncio.sleep(5)
            elif "Replies" in message_reply:
                try:
                    global replies_target
                    global replies_default_target
                    replies_default_target = int(message.text)
                    replies_target = replies_default_target
                    bot_message = await message.answer(
                        f"💬 <b>Default Replies</b> updated to {replies_target}"
                    )
                    await asyncio.sleep(3)
                    await bot.edit_message_text(
                        chat_id=message.reply_to_message.chat.id,
                        message_id=message.reply_to_message.message_id,
                        text=targets_reply.format(
                            "Default", "Replies", "replies", "Replies", replies_target
                        ),
                        reply_markup=keyboard_default_back,
                    )
                except ValueError:
                    bot_message = await message.answer(
                        "❌ <b>Invalid input. Please enter a valid number.</b>"
                    )
                    await asyncio.sleep(5)
            elif "Views" in message_reply:
                try:
                    global views_target
                    global views_default_target
                    views_default_target = int(message.text)
                    views_target = views_default_target
                    bot_message = await message.answer(
                        f"👀 <b>Default Views</b> updated to {views_target}"
                    )
                    await asyncio.sleep(3)
                    await bot.edit_message_text(
                        chat_id=message.reply_to_message.chat.id,
                        message_id=message.reply_to_message.message_id,
                        text=targets_reply.format(
                            "Default", "Views", "views", "Views", views_target
                        ),
                        reply_markup=keyboard_default_back,
                    )
                except ValueError:
                    bot_message = await message.answer(
                        "❌ <b>Invalid input. Please enter a valid number.</b>"
                    )
                    await asyncio.sleep(5)
            elif "Bookmarks" in message_reply:
                try:
                    global bookmarks_target
                    global bookmarks_default_target
                    bookmarks_default_target = int(message.text)
                    bookmarks_target = bookmarks_default_target
                    bot_message = await message.answer(
                        f"🔖 <b>Default Bookmarks</b> updated to {bookmarks_target}"
                    )
                    await asyncio.sleep(3)
                    await bot.edit_message_text(
                        chat_id=message.reply_to_message.chat.id,
                        message_id=message.reply_to_message.message_id,
                        text=targets_reply.format(
                            "Default", "Bookmarks", "bookmarks", "Bookmarks", bookmarks_target
                        ),
                        reply_markup=keyboard_default_back,
                    )
                except ValueError:
                    bot_message = await message.answer(
                        "❌ <b>Invalid input. Please enter a valid number.</b>"
                    )
                    await asyncio.sleep(5)
            write_values(
                likes_default_target,
                retweets_default_target,
                replies_default_target,
                views_default_target,
                bookmarks_default_target,
            )
        elif "Likes" in message_reply:
            try:
                likes_target = int(message.text)
                bot_message = await message.answer(
                    f"💙 <b>Likes</b> updated to {likes_target}"
                )
                await asyncio.sleep(3)
                await bot.edit_message_text(
                    chat_id=message.reply_to_message.chat.id,
                    message_id=message.reply_to_message.message_id,
                    text=targets_reply.format(
                        "", "Likes", "likes", "Likes", likes_target
                    ),
                    reply_markup=keyboard_back,
                )
            except ValueError:
                bot_message = await message.answer(
                    "❌ <b>Invalid input. Please enter a valid number.</b>"
                )
                await asyncio.sleep(5)
        elif "Retweets" in message_reply:
            try:
                retweets_target = int(message.text)
                bot_message = await message.answer(
                    f"🔄 <b>Retweets</b> updated to {retweets_target}"
                )
                await asyncio.sleep(3)
                await bot.edit_message_text(
                    chat_id=message.reply_to_message.chat.id,
                    message_id=message.reply_to_message.message_id,
                    text=targets_reply.format(
                        "", "Retweets", "retweets", "Retweets", retweets_target
                    ),
                    reply_markup=keyboard_back,
                )
            except ValueError:
                bot_message = await message.answer(
                    "❌ <b>Invalid input. Please enter a valid number.</b>"
                )
                await asyncio.sleep(5)
        elif "Replies" in message_reply:
            try:
                replies_target = int(message.text)
                bot_message = await message.answer(
                    f"💬 <b>Replies</b> updated to {replies_target}"
                )
                await asyncio.sleep(3)
                await bot.edit_message_text(
                    chat_id=message.reply_to_message.chat.id,
                    message_id=message.reply_to_message.message_id,
                    text=targets_reply.format(
                        "", "Replies", "replies", "Replies", replies_target
                    ),
                    reply_markup=keyboard_back,
                )
            except ValueError:
                bot_message = await message.answer(
                    "❌ <b>Invalid input. Please enter a valid number.</b>"
                )
                await asyncio.sleep(5)
        elif "Views" in message_reply:
            try:
                views_target = int(message.text)
                bot_message = await message.answer(
                    f"👀 <b>Views</b> updated to {views_target}"
                )
                await asyncio.sleep(3)
                await bot.edit_message_text(
                    chat_id=message.reply_to_message.chat.id,
                    message_id=message.reply_to_message.message_id,
                    text=targets_reply.format(
                        "", "Views", "views", "Views", views_target
                    ),
                    reply_markup=keyboard_back,
                )
            except ValueError:
                bot_message = await message.answer(
                    "❌ <b>Invalid input. Please enter a valid number.</b>"
                )
                await asyncio.sleep(5)
        elif "Bookmarks" in message_reply:
            try:
                bookmarks_target = int(message.text)
                bot_message = await message.answer(
                    f"🔖 <b>Bookmarks</b> updated to {bookmarks_target}"
                )
                await asyncio.sleep(3)
                await bot.edit_message_text(
                    chat_id=message.reply_to_message.chat.id,
                    message_id=message.reply_to_message.message_id,
                    text=targets_reply.format(
                        "", "Bookmarks", "bookmarks", "Bookmarks", bookmarks_target
                    ),
                    reply_markup=keyboard_back,
                )
            except ValueError:
                bot_message = await message.answer(
                    "❌ <b>Invalid input. Please enter a valid number.</b>"
                )
                await asyncio.sleep(5)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot_message.delete()


@dp.message()
async def handle_message(message: types.Message):
    message_text = message.text
    if message_text:
        match = TWITTER_LINK_PATTERN.search(message_text)
        if match:
            global link
            link = message_text
            global likes_target, retweets_target, replies_target, views_target, bookmarks_target
            likes_target = likes_default_target
            retweets_target = retweets_default_target
            replies_target = replies_default_target
            views_target = views_default_target
            bookmarks_target = bookmarks_default_target
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
                    [InlineKeyboardButton(text="🎯 Targets", callback_data="option_2")],
                    [
                        InlineKeyboardButton(text="🎨  Customization", callback_data="option_4")
                    ],
                    [InlineKeyboardButton(text="🚪 Close", callback_data="option_3")],
                ]
            )
            await message.answer(
                formatted,
                reply_markup=keyboard_message,
            )
        else:
            return


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
            text=targets_reply.format("", "Likes", "likes", "Likes", likes_target),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "2":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "", "Retweets", "retweets", "Retweets", retweets_target
            ),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "3":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "", "Replies", "replies", "Replies", replies_target
            ),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "4":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format("", "Views", "views", "Views", views_target),
            reply_markup=keyboard_back,
        )
        await callback_query.answer()
    elif target == "5":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "", "Bookmarks", "bookmarks", "Bookmarks", bookmarks_target
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
            text=targets_text.format("", 'either for each raid or as a default setting'), 
            reply_markup=keyboard_target,
        )
        await callback_query.answer()
    elif target == "8":
        keyboard_default_target = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"💙 Likes ({likes_target})", callback_data="target_9"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔄 Retweets ({retweets_target})",
                        callback_data="target_10",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"💬 Replies ({replies_target})", callback_data="target_11"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"👀 Views ({views_target})", callback_data="target_12"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"🔖 Bookmarks ({bookmarks_target})",
                        callback_data="target_13",
                    )
                ],
                [InlineKeyboardButton(text=f"🔙 Back", callback_data="target_7")],
            ]
        )
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_text.format("Default",'in the default settings'),
            reply_markup=keyboard_default_target,
        )
        await callback_query.answer()
    elif target == "9":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default", "Likes", "likes", "likes", likes_target
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "10":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default", "Retweets", "retweets", "retweets", retweets_target
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "11":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default", "Replies", "replies", "replies", replies_target
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "12":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default", "Views", "views", "views", views_target
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()
    elif target == "13":
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=targets_reply.format(
                "Default", "Bookmarks", "bookmarks", "bookmarks", bookmarks_target
            ),
            reply_markup=keyboard_default_back,
        )
        await callback_query.answer()


@router.callback_query(F.data == "start raid")
async def star_raid_callback(callback: CallbackQuery):
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
    else:
        chat_id = callback.message.chat.id
        raid_status[chat_id] = True
        raid_message = "⚡️ <b>Raid Started!</b>\n\n" + percentages

    await callback.message.delete()
    await callback.message.answer(raid_message)
    await callback.answer()


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
            text=targets_text.format("", 'either for each raid or as a default setting'),
            reply_markup=keyboard_target,
        )
        await callback_query.answer()
    elif option == "3":
        await bot.delete_message(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
        )
    elif option == "4":
        keyboard_customization = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚀  Start Media", callback_data="option_5"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🖼  Raid Media", callback_data="option_6"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🏁  End Media", callback_data="option_7",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📝  Custom Text", callback_data="option_8",
                    )
                ],
                [InlineKeyboardButton(text="🔙 Back", callback_data="target_6")],
            ]
        )
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="⚙️ <b>Raid Options > Customization</b>\n\n"
            'You can set custom media for ongoing raids and end media for when a raid is completed.',
            reply_markup=keyboard_customization,
        )
        await callback_query.answer()    


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
