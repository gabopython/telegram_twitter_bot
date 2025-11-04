import re
from pathlib import Path
from aiogram.types import InlineKeyboardButton
from config import BOT_USERNAME

TWITTER_LINK_PATTERN = re.compile(
    r"https?://(www\.)?(twitter\.com|x\.com)/[A-Za-z0-9_]+/status/\d+"
)
MEDIA_DIR_RAID = Path("media/raid")
MEDIA_DIR_START = Path("media/start")
MEDIA_DIR_END = Path("media/end")
RAID_MEDIA_PROMPT = "Reply to this message"

raid_status = {}
raid_tweet = {}
timer = {}
link = {}
tweet_id = {}
likes_target = {}
retweets_target = {}
replies_target = {}
views_target = {}
bookmarks_target = {}
likes_default_target = {}
retweets_default_target = {}
replies_default_target = {}
views_default_target = {}
bookmarks_default_target = {}
percentages = {}
last_bot_message = {}
i = {}
sender_address = {}
ticker_name = {}
url_ledger = {}
raid_messages = {}
targets_text = (
    "⚙️ <b>Raid Options > {} Targets</b>\n\n"
    "You can specify the number of likes, retweets, replies, views and bookmarks that a tweet must have to be considered a valid target {}."
)
targets_reply = (
    "⚙️ <b>Raid Options > {} Targets > {}</b>\n\n"
    "Please reply to this message with the new number of {} that a tweet must have to be considered a valid {} target.\n\n"
    "<b>Current {}:</b> {}"
)
customization_text = "⚙️ <b>Raid Options > Customization {}</b>\n\n" "{}."
target_saved = (
    "✅ <b>Target saved successfully!</b>\n\n"
    "Please reply to this message with the new number of {} that a tweet must have to be considered a valid {}target.\n\n"
    "<b>Current {}:</b> {}"
)
same_value = "❌ <b>{} {} already set to this value.</b>"


def calculate_percentage(actual, target):
    if target == 0:
        return 100  # Avoid division by zero
    percentage = round((actual / target) * 100, 2)
    return min(percentage, 100)


def get_emoji(percentage):
    if percentage <= 50:
        return "🟥"  # Red square emoji for <= 50%
    elif percentage < 100:
        return "🟨"  # Yellow square emoji for < 100%
    else:
        return "🟦"  # Blue square emoji for >= 100%

def trending_buttons(spot: int = None, ticker: str = None, url: str = None):
    """Create inline keyboard for 'raid' message"""
    trending_url = f"https://t.me/{BOT_USERNAME}?start=trending"    


    trending_buttons = [
        InlineKeyboardButton(text="⃝", url=trending_url)
        for i in range(5)
    ]

    if spot:
        trending_buttons[spot - 1] = InlineKeyboardButton(
            text=ticker,
            url=url
        )

    return trending_buttons