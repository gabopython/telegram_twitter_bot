import tweepy
from config import TWITTER_CLIENT_KEY, TWITTER_CLIENT_SECRET, callback_url
from typing import Tuple, Optional


class XClient:
    """X (Twitter) API client wrapper"""
    
    def __init__(self):
        self.api_key = TWITTER_CLIENT_KEY
        self.api_secret = TWITTER_CLIENT_SECRET
    
    def get_oauth_handler(self) -> tweepy.OAuth1UserHandler:
        """Create OAuth handler for authentication"""
        oauth = tweepy.OAuth1UserHandler(
            self.api_key,
            self.api_secret,
            callback=callback_url
        )
        return oauth
    
    def get_authorization_url(self) -> Tuple[str, str]:
        """
        Get authorization URL for user to authenticate
        Returns: (auth_url, oauth_token)
        """
        oauth = self.get_oauth_handler()
        auth_url = oauth.get_authorization_url()
        oauth_token = oauth.request_token['oauth_token']
        return auth_url, oauth_token
    
    def get_access_token(self, oauth_token: str, oauth_verifier: str) -> Tuple[str, str]:
        """
        Exchange OAuth verifier for access token
        Returns: (access_token, access_token_secret)
        """
        oauth = self.get_oauth_handler()
        oauth.request_token = {
            'oauth_token': oauth_token,
            'oauth_token_secret': ''
        }
        access_token, access_token_secret = oauth.get_access_token(oauth_verifier)
        return access_token, access_token_secret
    
    def create_client(self, access_token: str, access_token_secret: str) -> tweepy.Client:
        """Create authenticated X API client"""
        client = tweepy.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        return client
    
    def like_tweet(self, access_token: str, access_token_secret: str, tweet_id: str) -> bool:
        """
        Like a tweet
        Returns: True if successful, False otherwise
        """
        try:
            client = self.create_client(access_token, access_token_secret)
            response = client.like(tweet_id)
            
            # Check if the response has data (indicating success)
            return response.data.get('liked', False)

        except tweepy.errors.Forbidden as e:
            print(f"403 Forbidden: Check App Project location and Write Permissions. Details: {e}")
            return False
        except Exception as e:
            print(f"Error liking tweet: {e}")
            return False
    
    def get_user_info(self, access_token: str, access_token_secret: str) -> Optional[dict]:
        """Get authenticated user's information"""
        try:
            client = self.create_client(access_token, access_token_secret)
            me = client.get_me(user_fields=['username', 'name'])
            return {
                'id': me.data.id,
                'username': me.data.username,
                'name': me.data.name
            }
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None


# Global X client instance
x_client = XClient()