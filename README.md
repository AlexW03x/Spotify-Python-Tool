# Spotify-Python-Tool
## What is it?
> This is my first python project focusing on implementing the coding that I've learnt into a tool that may be useful for time to time. It is a graphical user interface designed utilising the **Tkinter** module and fetches data utilising the Spotify API where users will need their **CLIENT_ID** and **CLIENT_SECRET**.

## Why Build It?
> I decided to build this project as I identified that Spotify on the desktop version regardless of membership status doesn't have the ability to download songs locally to the computer system so I built it as I want the ability to have all my songs locally too for just incase I travel or go somewhere without internet and want to listen to music whilst working.

## Lessons From Project
> Althought the project is completed, I feel as if there is a much better approach to programming this giving better performance through optimising the code. There is a lot of room where code is repeated and some parts unused, however this is a lesson to myself for future projects to be more clean with code and make it more understandable. Elsewise, my knowledge of Python has increased and I used as many different techniques as I could to make this work.

## How To Use It?
```python
Utilise the following commands: py -m pip install __module_name__ or python pip install __module_name__ or pip install __module_name__

1. py -m pip install spotipy
2. py -m pip install tk
3. py -m pip install mutagen
4. py -m pip install requests
5. py -m pip install pytube
6. py -m pip install moviepy
```
### Changing Client ID and Client Secret
![Where to change the CLIENT_ID and CLIENT_SECRET](/Images/Authorisation.JPG)

> You can find the client secret and ID by going to https://developer.spotify.com/documentation/web-api and logging into your spotify account and creating a new project. The link will guide you through how to properly do this and once done go into the source code and change those IDs in order to use the application.

## Images of The Tool:
![UserID Screen](/Images/Introduction.JPG)
![Home Screen](/Images/HomeScreen.JPG)
![Playlist Download](/Images/PlaylistDownloader.JPG)
![Playlist Converter](/Images/PlaylistConverter.JPG)
![Song Searcher and Downloader](/Images/SongSearcher.JPG)
