from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from x_client import x_client
from storage import storage
import asyncio
from typing import Optional


app = FastAPI(title="X OAuth Callback Server")

# Store bot instance to send messages
bot_instance = None


def set_bot_instance(bot):
    """Set the bot instance for sending messages"""
    global bot_instance
    bot_instance = bot


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "X OAuth Callback Server"}


@app.get("/callback")
async def oauth_callback(oauth_token: str, oauth_verifier: str):
    """
    OAuth callback endpoint
    X redirects users here after they authorize the app
    """
    try:
        # Get user_id from oauth_token
        user_id = storage.get_user_by_oauth_token(oauth_token)
        
        if not user_id:
            return HTMLResponse(
                content="<h1>Error</h1><p>Session not found or expired. Please try /login again.</p>",
                status_code=400
            )
        
        # Exchange verifier for access token
        access_token, access_token_secret = x_client.get_access_token(
            oauth_token, 
            oauth_verifier
        )
        
        # Save tokens
        storage.save_user_tokens(user_id, access_token, access_token_secret)
        
        # Clean up OAuth session
        storage.remove_oauth_session(oauth_token)
        
        # Get user info
        user_info = x_client.get_user_info(access_token, access_token_secret)
        
        # Send success message to user via Telegram
        if bot_instance and user_info:
            username = user_info.get('username', 'Unknown')
            asyncio.create_task(
                bot_instance.send_message(
                    user_id,
                    f"✅ Successfully logged in as @{username}!\n\n"
                    "You can now use /like to like tweets."
                )
            )
        
        return HTMLResponse(
            content=f"""
            <html>
                <head>
                    <title>Authorization Successful</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        }}
                        .container {{
                            background: white;
                            padding: 40px;
                            border-radius: 10px;
                            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                            text-align: center;
                            max-width: 500px;
                        }}
                        h1 {{
                            color: #1DA1F2;
                            margin-bottom: 20px;
                        }}
                        p {{
                            color: #333;
                            font-size: 18px;
                            line-height: 1.6;
                        }}
                        .success-icon {{
                            font-size: 60px;
                            margin-bottom: 20px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="success-icon">✅</div>
                        <h1>Authorization Successful!</h1>
                        <p>You've successfully connected your X account.</p>
                        <p>You can now close this window and return to Telegram.</p>
                    </div>
                </body>
            </html>
            """
        )
        
    except Exception as e:
        print(f"OAuth callback error: {e}")
        return HTMLResponse(
            content=f"<h1>Error</h1><p>Failed to complete authorization: {str(e)}</p>",
            status_code=500
        )

