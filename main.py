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
URL = f"https://www.billboard.com/charts/hot-100/{year_prompt}/"

response = requests.get(url=URL)
top_100_website = response.text

soup = BeautifulSoup(top_100_website, "html.parser")
song_title = soup.find_all(name="h3", id="title-of-a-story", class_="c-title")

songs = soup.select("h3.a-font-primary-bold-s.u-letter-spacing-0021")
top_100 = [song.text.strip() for song in songs]
print(top_100)

# Spotify Authentication #
# token.txt is given via Spotify and added to a text file named "token.txt" placed in directory next to main.py
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

# Searching Spotify for songs #
song_uris = []
year = year_prompt.split("-")[0]
for song in top_100:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} does not exist in Spotify. Skipped.")

# Creating a new Spotify playlist #
playlist = sp.user_playlist_create(user=user_id, name=f"{year_prompt} Billboard 100", public=False,)

# Adding top 100 songs to new playlist #
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(f"New playlist '{year_prompt} Billboard 100' created successfully")
