import requests
import base64

# Spotify API credentials (replace with your actual values)
CLIENT_ID = "e0b344048259402e81c1423f73401f33"
CLIENT_SECRET = "d8f11fa549604721954fe95d1ae9d553"
ACCESS_TOKEN = "BQApSFpscUo7XxgsHm1knxeFf44BTggBQ5QLrET-69B8oyhV6IdCwe8GqMG00MtcvTmTcA1q4K1RKngjZ4_cSO3JZDNt3yqX5rorXegQA_8hp_HUzrOosGlRl21J52FnnIQNqXksitanoHZwF6iXkWxmeQbd2quvz-pd2dTAz-7lt-ra1Ca90bsdTGRTxz2wREzJwNw_A9UvjS1sIN373p9NK82UWEXp"
REFRESH_TOKEN = "AQDXSc73YYx5D4obey__tUAef44G_rSQ-fEsIX0dwd2jCJAYcTaGvv4tXp8OfAromkRi95fY80R-sppCw8Gk20mE6lIG8jH2no5uYy8gGaF3oxOWy2HxrDUyjReYhtxYloc"

# Function to get currently playing track
def get_currently_playing():
    # Set the authorization header with the access token
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    # Make a GET request to the 'currently-playing' endpoint
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the current track information
        track_data = response.json()
        if track_data:
            print("Currently playing track:", track_data["name"], "by", track_data["artists"][0]["name"])
        else:
            print("No track currently playing.")
    else:
        print("Error fetching current track:", response.status_code)

# Function to refresh the access token using the refresh token
def refresh_access_token():
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    # Make the request to get a new access token
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

    if response.status_code == 200:
        tokens = response.json()
        new_access_token = tokens["access_token"]
        print("New Access Token:", new_access_token)
        return new_access_token
    else:
        print("Error refreshing access token:", response.status_code)
        return None

# Main function to call the above methods
def main():
    # Try to get the currently playing track
    get_currently_playing()

    # If the access token has expired or you need a new one, refresh it
    new_token = refresh_access_token()
    if new_token:
        print("Successfully refreshed the access token.")
        # Optionally, you could now call get_currently_playing() again with the new token

if __name__ == "__main__":
    main()


