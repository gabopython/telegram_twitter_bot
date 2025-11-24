import tweepy
from config import CLIENT_ID, CLIENT_SECRET

def post_tweet(token_dict, text):
    """
    Connects to X using the stored token and posts a tweet.
    Returns (True, TweetID) or (False, ErrorMessage).
    """
    try:
        # Reconstruct the client using the access token
        client = tweepy.Client(
            bearer_token=token_dict.get("access_token"),
            consumer_key=CLIENT_ID,
            consumer_secret=CLIENT_SECRET,
            access_token=token_dict.get("access_token"),
            access_token_secret=token_dict.get("access_token_secret") # Note: OAuth2 often just uses access_token
        )

        # For OAuth 2.0 User Context (which is what we did in server.py)
        # We need to ensure we are using the right client initialization.
        # If the token_dict contains 'refresh_token', we can handle refresh here if needed.
        
        # Simple attempt with just access token
        response = client.create_tweet(text=text)
        return True, response.data['id']

    except tweepy.Errors.Unauthorized:
        return False, "Unauthorized. Token might be expired. Please /login again."
    except Exception as e:
        return False, str(e)