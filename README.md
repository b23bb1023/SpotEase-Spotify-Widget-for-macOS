# Spotify OAuth Integration & Currently Playing Tracker

Securely authenticate with Spotify, automatically refresh access tokens, and retrieve real-time playback data in a lightweight Flask app.

## Project Snapshot
A two-file Python project that implements Spotify's full OAuth 2.0 Authorization Code Flow.  
-  `app.py` — Flask web server that handles login redirect and token exchange  
-  `spotify_api.py` — script that uses the tokens to pull "currently playing" data and auto-refresh when expired

## Feature Matrix

| # | Capability | How It Works | Metrics / Specs |
|---|------------|-------------|-----------------|
| 1 | OAuth 2.0 sign-in | `/` route builds the Spotify authorize URL with scopes and redirects user | End-to-end auth latency ≈ 2-5 s |
| 2 | Token exchange | `/callback` swaps auth code for **access** & **refresh** tokens via `POST /api/token` | Access token TTL = 3600 s |
| 3 | Automatic refresh | `refresh_access_token()` hits `POST /api/token` with `grant_type=refresh_token` | Refresh call 200-500 ms |
| 4 | Real-time playback | `get_currently_playing()` calls `GET /v1/me/player/currently-playing` | Typical RTT 100-300 ms |
| 5 | Scope control | Requests `user-read-playback-state user-read-currently-playing playlist-read-private` | 3 fine-grained scopes |
| 6 | Error guardrails | Checks HTTP status, prints Spotify error JSON, returns clear messages | Handles 400 / 401 / 403 / 429 |
| 7 | Debug logging | Prints auth URL and raw token JSON for rapid troubleshooting | Zero-config verbose mode |
| 8 | Portable server | Runs on `0.0.0.0:5001`; deploy behind Gunicorn/HTTPS for prod | Tiny footprint < 3 kB code |

## Usage Instructions

| Step | Command / Action | Result |
|------|------------------|--------|
| 1 | `pip install -r requirements.txt` | Installs Flask + Requests |
| 2 | Replace `CLIENT_ID` / `CLIENT_SECRET` in both files | Links app to your Spotify dashboard entry |
| 3 | `python app.py` | Flask server starts on `localhost:5001` |
| 4 | Visit `http://localhost:5001/` | Browser redirected to Spotify login |
| 5 | Approve scopes → redirected to `/callback` | Terminal prints access & refresh tokens |
| 6 | Paste tokens into `spotify_api.py` | Ready to query playback |
| 7 | `python spotify_api.py` | Console shows "Currently playing track: …" |
| 8 | Need a new token? | Call `refresh_access_token()` or just re-run script |

### Troubleshooting Cheatsheet
-  `401 Unauthorized` → access token expired → run refresh  
-  `Error: No code received` → redirect URI mismatch in dashboard  
-  `429` → rate-limit; back-off & retry

## Configuration

1. **Create Spotify App**: Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. **Set Redirect URI**: Add `http://localhost:5001/callback` to your app settings
3. **Update Credentials**: Replace `CLIENT_ID` and `CLIENT_SECRET` in both Python files
4. **Install Dependencies**: Run `pip install -r requirements.txt`

## Project Structure

```
spotify-oauth-tracker/
├── app.py                 # Flask OAuth server
├── spotify_api.py         # API client with token refresh
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Requirements

- Python 3.6+
- Flask 2.0+
- Requests 2.25+
- Active Spotify Developer Account

## License

MIT License - Feel free to use and modify as needed.
