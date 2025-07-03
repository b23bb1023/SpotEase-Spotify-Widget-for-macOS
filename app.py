from flask import Flask, request, redirect
import requests
import base64
import json

app = Flask(__name__)

# Spotify app credentials
CLIENT_ID = "e0b344048259402e81c1423f73401f33"
CLIENT_SECRET = "d8f11fa549604721954fe95d1ae9d553"
REDIRECT_URI = "http://localhost:5001/callback"  # Replace if you used a different redirect URI

# Spotify URLs
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Step 1: Route to start the login process
@app.route("/")
def login():
    scope = "user-read-playback-state user-read-currently-playing playlist-read-private"
    auth_url = f"{SPOTIFY_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&scope={scope}&redirect_uri={REDIRECT_URI}"
    print(f"Redirecting to: {auth_url}")  # Debugging
    return redirect(auth_url)


# Step 2: Callback to handle Spotify's response
@app.route("/callback")
def callback():
    # Step 1: Extract the code from the URL
    code = request.args.get("code")
    if not code:
        return "Error: No code received from Spotify."

    # Step 2: Prepare to exchange the code for an access token
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    # Step 3: Request the access token
    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)

    # Step 4: Debugging the response
    print(f"Spotify Token Response: {response.status_code} {response.text}")

    # Check for errors
    if response.status_code != 200:
        return f"Error: Failed to fetch access token. Response: {response.text}"

    # Step 5: Parse and display the tokens
    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    return f"Access Token: {access_token}<br>Refresh Token: {refresh_token}"



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)

