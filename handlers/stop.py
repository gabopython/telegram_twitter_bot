from aiogram import Router
from aiogram.types import Message
from aiogram.enums.chat_member_status import ChatMemberStatus
from utils import raid_status
from aiogram.filters import Command


stop_router = Router()


@stop_router.message(Command("stop"))
async def stop_command(message: Message):
    # Check if the sender is an admin
    chat_id = message.chat.id
    user_id = message.from_user.id

    member = await message.bot.get_chat_member(chat_id, user_id)
    if member.status not in {ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR}:
        return  # User is not an admin, ignore message

    chat_id = message.chat.id
    if raid_status.get(chat_id):
        raid_status[chat_id] = False
        await message.answer(
            "🛑 <b>Raid Ended - Stopped by admin</b>\n\n" + "percentages"
        )
    else:
        await message.answer("❌ <b>There is no ongoing raid in this group</b>")
