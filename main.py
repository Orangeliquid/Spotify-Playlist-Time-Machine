import requests
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

# CLIENT_ID is given via Spotify
# CLIENT_SECRET is given via Spotify
# SPOTIFY_USERNAME is given via Spotify
# EXAMPLE_URL is given via Spotify
# All of these variables are environmental variables for security
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
SPOTIFY_USERNAME = os.environ["SPOTIFY_USERNAME"]
EXAMPLE_URL = os.environ["EXAMPLE_URL"]

# Getting the top 100 from UI # - Top 100 starting from year 1956
year_prompt = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year_prompt}"

try:
    response = requests.get(url=URL)
    response.raise_for_status()  # Raise an exception for bad responses

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="wikitable")

    # Map the column names to their indices
    column_indices = {"no.": 0, "title": 1, "artist": 2}

    top_100 = []
    for row in table.find_all("tr")[1:]:  # Skip the header row
        columns = row.find_all("td")

        # Check if the number of columns is as expected
        if len(columns) >= 3:  # At least 3 columns (no., title, artist)
            song = columns[column_indices["title"]].text.strip()
            artist = columns[column_indices["artist"]].text.strip()
            top_100.append({"song": song, "artist": artist})

    # Separate the first artist from the featured artists
    for artist_info in top_100:
        original_artist = artist_info['artist']

        if 'featuring' in original_artist:
            first_artist = original_artist.split('featuring')[0].strip()
        else:
            # If "featuring" is not found, split on "and"
            first_artist = original_artist.split('and')[0].strip()

        artist_info['artist'] = first_artist


except requests.RequestException as e:
    print(f"Error during request: {e}")

except Exception as e:
    print(f"An error occurred: {e}")


# Spotify Authentication #
# token.txt is given via Spotify and added to a text file named "token.txt" placed in same directory as main.py
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=SPOTIFY_USERNAME
    )
)

user_id = sp.current_user()["id"]

song_uris = []
songs_found = 0
print("Working.....\n")
for song in top_100:
    query = f"track:{song['song']} artist:{song['artist']}"

    try:
        result = sp.search(q=query, type="track")
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
        songs_found += 1
    except IndexError:
        print(f"Song not found: {query}")


# Creating a new Spotify playlist
playlist = sp.user_playlist_create(user=sp.me()["id"], name=f"{year_prompt} Billboard 100", public=False)

# Adding top 100 songs to the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("\nAbove are the songs that the application could not find, feel free to add manually!\n")
print(f"New playlist '{year_prompt} Billboard 100' created successfully")
print(f"{songs_found} songs added to playlist!")
