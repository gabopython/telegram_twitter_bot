from typing import Dict, Optional
import json


class UserStorage:
    """Simple in-memory storage for user sessions and tokens"""
    
    def __init__(self):
        self._users: Dict[int, dict] = {}
        self._oauth_sessions: Dict[str, int] = {}  # oauth_token -> user_id
    
    def save_oauth_session(self, oauth_token: str, user_id: int):
        """Save OAuth session mapping"""
        self._oauth_sessions[oauth_token] = user_id
    
    def get_user_by_oauth_token(self, oauth_token: str) -> Optional[int]:
        """Get user ID by OAuth token"""
        return self._oauth_sessions.get(oauth_token)
    
    def remove_oauth_session(self, oauth_token: str):
        """Remove OAuth session"""
        if oauth_token in self._oauth_sessions:
            del self._oauth_sessions[oauth_token]
    
    def save_user_tokens(self, user_id: int, access_token: str, access_token_secret: str):
        """Save user's X API tokens"""
        self._users[user_id] = {
            "access_token": access_token,
            "access_token_secret": access_token_secret
        }
    
    def get_user_tokens(self, user_id: int) -> Optional[dict]:
        """Get user's X API tokens"""
        return self._users.get(user_id)
    
    def remove_user_tokens(self, user_id: int):
        """Remove user's tokens (logout)"""
        if user_id in self._users:
            del self._users[user_id]
    
    def is_user_authenticated(self, user_id: int) -> bool:
        """Check if user is authenticated"""
        return user_id in self._users


# Global storage instance
storage = UserStorage()