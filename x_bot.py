import tweepy
import re
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("X_TOKEN")

# Twitter API credentials (replace with your own keys)
BEARER_TOKEN = token

# Authenticate with Twitter API
client = tweepy.Client(bearer_token=BEARER_TOKEN)


def extract_tweet_id(url):
    """Extracts the tweet ID from an X (Twitter) post URL."""
    match = re.search(r"/status/(\d+)", url)
    return match.group(1) if match else None


def get_tweet_data(tweet_url):
    """Fetches data from a tweet given its URL."""
    tweet_id = extract_tweet_id(tweet_url)
    if not tweet_id:
        return "Invalid tweet URL"

    try:
        tweet = client.get_tweet(id=tweet_id, tweet_fields=["public_metrics"])

        if tweet.data:
            metrics = tweet.data["public_metrics"]
            return {
                "Retweets": metrics["retweet_count"],
                "Likes": metrics["like_count"],
                "Replies": metrics["reply_count"],
                "Quotes": metrics["quote_count"],
            }
        else:
            return {"Tweet not found or API restrictions applied.": None}

    except Exception as e:
        return {f"Error: {e}": None}
