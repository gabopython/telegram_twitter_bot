import re
from pathlib import Path

TWITTER_LINK_PATTERN = re.compile(
    r"https?://(www\.)?(twitter\.com|x\.com)/[A-Za-z0-9_]+/status/\d+"
)
MEDIA_DIR = Path("media")
RAID_MEDIA_PROMPT = "Reply to this message"

raid_status = {}
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
    "Please reply to this message with the new number of {} that a tweet must have to be considered a valid {} target.\n\n"
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
