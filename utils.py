import re

TWITTER_LINK_PATTERN = re.compile(
    r"https?://(www\.)?(twitter\.com|x\.com)/[A-Za-z0-9_]+/status/\d+"
)
raid_status = {}
targets_text = (
    "⚙️ <b>Raid Options > {} Targets</b>\n\n"
    "You can specify the number of likes, retweets, replies, views and bookmarks that a tweet must have to be considered a valid target either for each raid or as a default setting."
)
targets_reply = (
    "⚙️ <b>Raid Options > {} Targets > {}</b>\n\n"
    "Please reply to this message with the new number of {} that a tweet must have to be considered a valid target.\n\n"
    "<b>Current {}:</b> {}"
)


def read_values():
    with open("values.txt", "r") as file:
        lines = file.readlines()
        likes_target_default = int(lines[0].strip())
        retweets_target_default = int(lines[1].strip())
        replies_target_default = int(lines[2].strip())
        views_target_default = int(lines[3].strip())
        bookmarks_target_default = int(lines[4].strip())

    return (
        likes_target_default,
        retweets_target_default,
        replies_target_default,
        views_target_default,
        bookmarks_target_default,
    )


def write_values(
    likes_target_default,
    retweets_target_default,
    replies_target_default,
    views_target_default,
    bookmarks_target_default,
):
    with open("values.txt", "w") as file:
        file.write(f"{likes_target_default}\n")
        file.write(f"{retweets_target_default}\n")
        file.write(f"{replies_target_default}\n")
        file.write(f"{views_target_default}\n")
        file.write(f"{bookmarks_target_default}\n")


def calculate_percentage(actual, target):
    if target == 0:
        return 0  # Avoid division by zero
    percentage = round((actual / target) * 100, 2)
    return min(percentage, 100)


def get_emoji(percentage):
    if percentage <= 50:
        return "🟥"  # Red square emoji for <= 50%
    elif percentage < 100:
        return "🟨"  # Yellow square emoji for < 100%
    else:
        return "🟦"  # Blue square emoji for >= 100%
