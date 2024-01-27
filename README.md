# Spotify Billboard Playlist Creator

## Overview
This Python script creates a Spotify playlist based on the Billboard Year-End Hot 100 singles for a specified year. It scrapes data from Wikipedia, searches for each song on Spotify, and adds them to a new playlist on your Spotify account.

## Prerequisites
Before running the script, ensure you have the following environmental variables set:
- `CLIENT_ID`: Spotify client ID.
- `CLIENT_SECRET`: Spotify client secret.
- `SPOTIFY_USERNAME`: Your Spotify username.
- `EXAMPLE_URL`: Spotify example URL (for authentication).

Make sure to obtain these values from the Spotify Developer Dashboard.

## Usage
1. Run the script using:
    ```bash
    python spotify_playlist_creator.py
    ```
2. Input the year you want to travel to when prompted.
3. The script fetches the top 100 songs from Billboard for the specified year and creates a new Spotify playlist.

## Spotify Authentication
- The script uses the SpotifyOAuth authentication manager, and you will be prompted to log in and authenticate during the first run.
- A file named `token.txt` is used for caching authentication tokens.

## Note
- Ensure all environmental variables are set correctly before running the script.
- If a song is not found on Spotify, it will be displayed in the console, and you can add it manually to the playlist.

## Dependencies
- requests
- spotipy
- bs4 (BeautifulSoup)

## License
This project is licensed under the [MIT License](LICENSE.txt).
