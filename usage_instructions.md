# Spotify OAuth Integration - Usage Instructions

## Pre-requisites

### 1. Spotify Developer Account Setup
- Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- Log in with your Spotify account
- Click "Create App"
- Fill in app details:
  - **App Name**: Choose any name (e.g., "My Spotify Tracker")
  - **App Description**: Brief description of your app
  - **Redirect URI**: `http://localhost:5001/callback`
  - **Which API/SDKs are you planning to use?**: Web API

### 2. Get Your Credentials
- After creating the app, note down:
  - **Client ID**: Found in your app dashboard
  - **Client Secret**: Click "Show client secret" to reveal

## Installation Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Your App
1. Open `app.py` and replace:
   ```python
   CLIENT_ID = "your_actual_client_id_here"
   CLIENT_SECRET = "your_actual_client_secret_here"
   ```

2. Open `spotify_api.py` and replace:
   ```python
   CLIENT_ID = "your_actual_client_id_here"
   CLIENT_SECRET = "your_actual_client_secret_here"
   ```

### Step 3: Start the OAuth Flow
```bash
python app.py
```

### Step 4: Complete Authentication
1. Open browser and navigate to `http://localhost:5001/`
2. You'll be redirected to Spotify login
3. Log in with your Spotify credentials
4. Authorize the app permissions:
   - Read your currently playing content
   - Read your playback state
   - Read your private playlists
5. After authorization, you'll be redirected back to localhost
6. Copy the **Access Token** and **Refresh Token** from the browser

### Step 5: Update API Script
1. Open `spotify_api.py`
2. Replace the token placeholders:
   ```python
   ACCESS_TOKEN = "paste_your_access_token_here"
   REFRESH_TOKEN = "paste_your_refresh_token_here"
   ```

### Step 6: Test the Integration
```bash
python spotify_api.py
```

## Expected Outputs

### Successful Authentication
```
Redirecting to: https://accounts.spotify.com/authorize?...
Spotify Token Response: 200 {"access_token":"BQA...","token_type":"Bearer",...}
```

### Currently Playing Track
```
Currently playing track: Song Name by Artist Name
New Access Token: BQA...
Successfully refreshed the access token.
```

### No Track Playing
```
No track currently playing.
```

## Common Issues & Solutions

### Issue 1: "Error: No code received from Spotify"
**Cause**: Redirect URI mismatch
**Solution**: 
- Ensure redirect URI in Spotify dashboard exactly matches: `http://localhost:5001/callback`
- Check for typos, extra spaces, or incorrect protocol (http vs https)

### Issue 2: "401 Unauthorized" Error
**Cause**: Access token expired (tokens expire after 1 hour)
**Solution**: 
- Run the refresh token function in `spotify_api.py`
- Or re-run the OAuth flow to get new tokens

### Issue 3: "403 Forbidden" Error
**Cause**: Insufficient permissions/scopes
**Solution**: 
- Verify your Spotify account has an active subscription (required for some endpoints)
- Check if the required scopes are properly requested

### Issue 4: "429 Too Many Requests" Error
**Cause**: Rate limiting by Spotify API
**Solution**: 
- Wait 30-60 seconds before retrying
- Implement exponential backoff in production code

## Advanced Usage

### Automatic Token Refresh
```python
# Add this to your main script
def ensure_valid_token():
    # Check if current token is still valid
    test_response = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
    )

    if test_response.status_code == 401:
        # Token expired, refresh it
        return refresh_access_token()
    return ACCESS_TOKEN
```

### Production Deployment
For production use:
1. Use environment variables for sensitive data
2. Implement HTTPS with proper SSL certificates
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Add proper error handling and logging
5. Consider using a database to store tokens securely

## Security Notes

⚠️ **Important**: Never commit your actual CLIENT_SECRET, ACCESS_TOKEN, or REFRESH_TOKEN to version control.

Use environment variables:
```python
import os
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
```

## API Rate Limits

Spotify API limits:
- **Rate Limit**: 100 requests per minute for most endpoints
- **Token Expiry**: Access tokens expire after 1 hour
- **Refresh Token**: Does not expire but can be revoked

## Support

For issues with this implementation, check:
1. [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api/)
2. [Spotify Developer Community](https://community.spotify.com/t5/Spotify-for-Developers/bd-p/Spotify_Developer)
3. Review the console output for detailed error messages
