import spotipy
import sys
import tkinter
import time
import io
import requests
import PIL.Image
import PIL.ImageTk
import webbrowser
import os
import re
import mutagen

from pytube import YouTube
from urllib.request import urlopen
from tkinter import font
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from tkinter import *
from tkinter import ttk
from functools import partial
from moviepy.editor import *
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3

#variables
global spotify_user

##authorisation with spotify utilising keys: ID and SECRET
auth_manager = spotipy.SpotifyClientCredentials(client_id=CLIENT_ID_HERE, client_secret=CLIENT_SECRET_HERE)
sp = spotipy.Spotify(auth_manager=auth_manager, client_credentials_manager=auth_manager)

# test ID: ""

#app functions
def web(url): #visit website
    webbrowser.open(url)

def image_url_to_data(url): #try and get image data
    response = requests.get(url)
    if response.status_code == 200:
        img = io.BytesIO(response.content)
        image = PIL.Image.open(img)
        finalimage = PIL.ImageTk.PhotoImage(image)
        return finalimage
    else:
        return ""

def image_url_to_data2(url, x, y): #try and get image data
    response = requests.get(url)
    if response.status_code == 200:
        img = io.BytesIO(response.content)
        image = PIL.Image.open(img).resize((x,y))
        finalimage = PIL.ImageTk.PhotoImage(image)
        return finalimage
    else:
        return ""

global mainframe
global playlistdownload
global currentframe
global songframe
global userid
currentframe = "Home" # prevent the cloning glitch of frame
global playlistoptions
global converterframe

global currentPlaylist
global label_playlist
global playlistopenonlinebtn
global tracksamount
global downloadplaylist
global console
global finaloutput

global singlesoutput
singlesoutput = None

global opts
global curopt
global curplay
global curlbl
global curopen
global curtracks
global console2

def singledownload(x):
    global singlesoutput
    track = sp.track(x.get())
    a = track["album"]["artists"][0]["name"]
    t = track["name"]
    b = requestYoutube(a+" - "+t+" [Official Audio]")
    print(a + " - " + t + " [Official Audio]")
    if b != False:
        song = downloadsingle(b)
        if singlesoutput != None:
            singlesoutput.destroy()
        if song:
            add_meta = EasyID3(song)
            add_meta["title"] = track["name"]
            add_meta["date"] = track["album"]["release_date"]
            add_meta["isrc"] = track["external_ids"]["isrc"]
            add_meta["artist"] = track["artists"][0]["name"]
            add_meta["tracknumber"] = str(track["track_number"])
            add_meta["album"] = track["album"]["name"]
            add_meta.save()

            add_img = ID3(song)
            with urlopen(track["album"]["images"][1]["url"]) as art:
                add_img["APIC"] = APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=art.read())
            add_img.save(v2_version=3)
            os.replace(song, f"Downloads/{os.path.basename(song)}")
            singlesoutput = ttk.Label(songframe, text="Downloaded!", font=("Poppins", 10), background="lightgray")
            singlesoutput.place(relx=0.46, rely=0.28)
        else:
            singlesoutput = ttk.Label(songframe, text="Failed/Skipped!", font=("Poppins", 10), background="lightgray")
            singlesoutput.place(relx=0.45, rely=0.28)

        

def requestYoutube(x):
    youtubelink = "https://www.youtube.com/results?search_query=" + x.replace(" ", "+")
    reattempts = 5
    while reattempts > 0:
        try:
            getlink = urlopen(youtubelink)
            break
        except:
            reattempts -= 1
    else:
        print("Skipped.")
    if reattempts > 0:
        finallink = "https://www.youtube.com/watch?v=" + re.findall(r"watch\?v=(\S{11})", getlink.read().decode())[0]
        return finallink
    else: #prevents download function from downloading causing an error
        return False

def download(x):
    global finaloutput
    link = YouTube(x)
    link.title = "".join([char for char in link.title if char not in ["/", "\\", "|", "?", "*", ":", ">", "<", '"']])
    ##check if file is in directory##
    if os.path.exists(finaloutput + f"/{link.title}.mp3"):
        return False #skips file
    
    file_ = link.streams.filter(only_audio=True).first()
    thefile = file_.download(output_path=finaloutput + "/")
    mp3 = os.path.splitext(thefile)[0]
    finalfile = mp3 + ".mp3"
    mp4tomp3 = AudioFileClip(thefile)
    mp4tomp3.write_audiofile(finalfile, logger=None)
    mp4tomp3.close()
    os.remove(thefile)
    os.replace(finalfile, finaloutput + f"/{link.title}.mp3")
    finalfile = finaloutput + f"/{link.title}.mp3"
    return finalfile

def downloadsingle(x):
    link = YouTube(x)
    link.title = "".join([char for char in link.title if char not in ["/", "\\", "|", "?", "*", ":", ">", "<", '"']])
    ##check if file is in directory##
    if os.path.exists(f"Downloads/{link.title}.mp3"):
        return False #skips file
    file_ = link.streams.filter(only_audio=True).first()
    thefile = file_.download(output_path="Downloads/")
    mp3 = os.path.splitext(thefile)[0]
    finalfile = mp3 + ".mp3"
    mp4tomp3 = AudioFileClip(thefile)
    mp4tomp3.write_audiofile(finalfile, logger=None)
    mp4tomp3.close()
    os.remove(thefile)
    os.replace(finalfile, f"Downloads/{link.title}.mp3")
    finalfile = f"Downloads/{link.title}.mp3"
    return finalfile 

def downloadtest(x):
    global console
    global finaloutput
    ez = sp.user_playlists(userid)["items"][x-1]["uri"]
    curplay = sp.playlist_tracks(ez)
    for i, track in enumerate(curplay["items"], start=1): #get playlist tracks names and IDs
        tname = track["track"]["name"]
        aname = track["track"]["artists"][0]["name"]
        links = track["track"]["external_urls"]["spotify"]
        print(str(i) + ". " + tname + " by " + aname + ": " + links) #identify songs by artist name and song name and links

        grab_link = requestYoutube(aname + " - " + tname + " audio ")
        if grab_link != False:
            song = download(grab_link)
            if song:
                os.replace(song, finaloutput + f"/{os.path.basename(song)}")
                console.configure(state="normal")
                console.insert(str(i)+".0", tname + " by " + aname + " downloaded!\n")
                console.configure(state="disabled")
            else:
                console.configure(state="normal")
                console.insert(str(i)+".0", tname + " by " + aname + " skipped!\n")
                console.configure(state="disabled")

def addto(x):
    global console2
    y = sp.user_playlists(userid)["items"][x-1]["uri"]
    for i, track in enumerate(sp.playlist_tracks(y)["items"], start=1):
        t = track["track"]["name"]
        a = track["track"]["artists"][0]["name"]
        l = track["track"]["external_urls"]["spotify"]
        
        grab = requestYoutube(a + " - " + t + " audio")
        if grab != False:
            console2.configure(state="normal")
            console2.insert(str(i)+".0", grab +"\n")
            console2.configure(state="disabled")

        


def change_playlist(x): ##will replace all the GUI modules with updated list
    global playlistdownload
    global playlistoptions
    global currentPlaylist
    global label_playlist
    global playlistopenonlinebtn
    global tracksamount
    global downloadplaylist
    global finaloutput
    #print(x)
    currentPlaylist = ttk.Label(playlistdownload, text=playlistoptions[x], font=("Poppins", 12), background="lightgray", wraplength=200)
    currentPlaylist.place(relx=0.145, rely=0.25)
    playlistimage = sp.user_playlists(userid)["items"][x-1]["images"][0]["url"]
    playlisttest = image_url_to_data2(playlistimage, 300, 300)
    label_playlist = ttk.Label(playlistdownload, image=playlisttest)
    label_playlist.photo = playlisttest
    label_playlist.place(relx=0.04, rely=0.30)
    tracks = sp.user_playlists(userid)["items"][x-1]["tracks"]["total"]
    tracksamount = ttk.Label(playlistdownload, text="Tracks: " + str(tracks), font=("Poppins", 12), background="lightgray")
    tracksamount.place(relx=0.18, rely=0.8)
    link = partial(web, sp.user_playlists(userid)["items"][x-1]["external_urls"]["spotify"])
    playlistopenonlinebtn = ttk.Button(playlistdownload, text="Open In Spotify", command=link)
    playlistopenonlinebtn.place(relx=0.11, rely=0.85, relwidth=0.25)

    dn = partial(downloadtest, x)
    downloadplaylist = ttk.Button(playlistdownload, text="Download Playlist", command=dn)
    downloadplaylist.place(relx=0.11, rely=0.9, relwidth=0.25)
    finaloutput = ""
    for i in range(len(playlistoptions[x])):
        if playlistoptions[x][i].isascii():
            finaloutput += playlistoptions[x][i]
        if playlistoptions[x][i].isdigit():
            finaloutput += playlistoptions[x][i]

def change_converter(x): #same as change playlist for converter could have made this optimised and less lines of code
    global converterframe
    global opts
    global curopt
    global curplay
    global curlbl
    global curopen
    global curtracks
    curplay = ttk.Label(converterframe, text=opts[x], font=("Poppins", 12), background="lightgray")
    curplay.place(relx=0.145, rely=0.25)
    curimg = image_url_to_data2(sp.user_playlists(userid)["items"][x-1]["images"][0]["url"], 300, 300)
    curlbl = ttk.Label(converterframe, image=curimg)
    curlbl.photo = curimg
    curlbl.place(relx=0.04, rely=0.3)
    curtracks = ttk.Label(converterframe, text="Tracks: " + str(sp.user_playlists(userid)["items"][x-1]["tracks"]["total"]), font=("Poppins", 12), background="lightgray")
    curtracks.place(relx=0.18, rely=0.8)
    op = partial(web, sp.user_playlists(userid)["items"][x-1]["external_urls"]["spotify"])
    curopen = ttk.Button(converterframe, text="Open In Spotify", command=op)
    curopen.place(relx=0.11, rely=0.85, relwidth=0.25)
    

global selectedpl

def fixup(s):
    global currentPlaylist
    global label_playlist
    global playlistoptions
    global playlistopenonlinebtn
    global tracksamount
    selectedpl.set(playlistoptions[playlistoptions.index(s)])
    print(selectedpl.get())
    currentPlaylist.destroy()
    label_playlist.destroy()
    playlistopenonlinebtn.destroy()
    tracksamount.destroy()
    downloadplaylist.destroy()
    change_playlist(playlistoptions.index(s))

def fixup2(s):
    global converterframe
    global curopt
    global opts
    global curplay
    global curlbl
    global curopen
    global curtracks
    curopt.set(opts[opts.index(s)])
    print(curopt.get())
    curplay.destroy()
    curlbl.destroy()
    curopen.destroy()
    curtracks.destroy()
    change_converter(opts.index(s))

def open_converter():
    global mainframe
    global converterframe
    global songframe
    global playlistdownload
    global currentframe
    global opts
    global curopt
    global curplay
    global curlbl
    global curopen
    global curtracks
    global console2
    if currentframe != "conv":
        if currentframe == "Song":
            songframe.destroy()
        if currentframe == "PLD":
            playlistdownload.destroy()
        currentframe = "conv"
        converterframe = Frame(mainframe, bg="lightgray", width=800, height=655)
        converterframe.place(relx=0.15, rely=0.01)

        converterlabel = ttk.Label(converterframe, text="Playlist Converter", background="lightgray", font=("Poppins", 20)).place(relx=0.35, rely=0.02)
        #print(sp.user_playlists(userid))
        opts = [""]
        for i in range(sp.user_playlists(userid)["total"]):
            opts.append(sp.user_playlists(userid)["items"][i]["name"])

        curopt = StringVar()
        curopt.set(opts[1])

        optsel = ttk.Label(converterframe, text="Playlist Select", background="lightgray", font=("Poppins", 14))
        optsel.place(relx=0.15, rely=0.1)
        optdrop = ttk.OptionMenu(converterframe, curopt, *opts, command=fixup2)
        optdrop.place(relx=0.09, rely=0.15, relwidth=0.25)
        change_converter(opts.index(curopt.get()))

        ##add options for conversion here## <YouTube>
        useLabel = ttk.Label(converterframe, text="Converters: ", background="lightgray", font=("Poppins", 14))
        useLabel.place(relx=0.6, rely=0.1)
        cmd = partial(addto, opts.index(curopt.get()))
        useYoutube = ttk.Button(converterframe, text="Convert To Youtube", command=cmd)
        useYoutube.place(relx=0.6, rely=0.15, relwidth=0.25)

        loglbl2 = ttk.Label(converterframe, text="Console: ", font=("Poppins", 12), background="lightgray")
        loglbl2.place(relx=0.6, rely=0.2)
        console2 = Text(converterframe, state="disabled", width=40, font=("Poppins", 8), height=30)
        console2.place(relx=0.6, rely=0.25)

def open_playlist_downloader(): #opens playlist downloader frame
    global mainframe
    global playlistdownload
    global currentframe
    global playlistoptions
    global selectedpl
    global console
    global songframe
    global converterframe
    if currentframe != "PLD":
        if currentframe == "song":
            songframe.destroy()
        if currentframe == "conv":
            converterframe.destroy()
        playlistdownload = Frame(mainframe, bg="lightgray", width=800, height=655)
        playlistdownload.place(relx=0.15, rely=0.01)

        playlistdownloadlabel = ttk.Label(playlistdownload, text="Playlist Downloader", font=("Poppins", 20), background="lightgray").place(relx=0.35, rely=0.02)
        #print(sp.user_playlists(userid))##for the dictionary
        playlistoptions = [""] ##add playlist to array and "" to prevent 0 bug
        for i in range(sp.user_playlists(userid)["total"]):
            playlistoptions.append(sp.user_playlists(userid)["items"][i]["name"])
        
        selectedpl = StringVar()
        selectedpl.set(playlistoptions[1])

        playlistselect = ttk.Label(playlistdownload, text="Playlist Select", background="lightgray", font=("Poppins", 14))
        playlistselect.place(relx=0.15, rely=0.1)
        playlistdrop = ttk.OptionMenu(playlistdownload, selectedpl, *playlistoptions, command=fixup)
        playlistdrop.place(relx=0.09, rely=0.15, relwidth=0.25)
        change_playlist(playlistoptions.index(selectedpl.get())) #set the first playlist identified
        
        currentframe = "PLD"

        loglbl = ttk.Label(playlistdownload, text="Console: ", font=("Poppins", 12), background="lightgray")
        loglbl.place(relx=0.6, rely=0.1)
        console = Text(playlistdownload, state="disabled", width=40, font=("Poppins", 8), height=30)
        console.place(relx=0.6, rely=0.15)
        consolenotice = ttk.Label(playlistdownload, text="Warning: During downloads the\napplication may freeze until\ndownloads are finished and\nthe time it takes is based\non your internet speed and\ncomputer's overall performance!", background="lightgray", font=("Poppins", 12), justify="center")
        consolenotice.place(relx=0.61, rely=0.8)
    else:
        return
    
global songimage
global songlink
global songcredentials
songimage = None
songlink = None
songcredentials = None
    
def songsearcher(artist, track): ##retrieves song data
    global songframe
    global songimage
    global songlink
    global songcredentials

    print(artist.get() + ": " + track.get())
    results = sp.search(q="artist:" + artist.get() + " track:" + track.get(), type="track", limit=1)
    print(results)

    if songimage != None and songlink != None and songcredentials != None: #prevent overflow of GUI
        songimage.destroy()
        songlink.destroy()
        songcredentials.destroy()
    
    r = results["tracks"]["items"]

    song_imga = image_url_to_data2(r[0]["album"]["images"][1]["url"], 200, 200)
    songimage = ttk.Label(songframe, image=song_imga)
    songimage.photo = song_imga
    songimage.place(relx=0.38, rely=0.55)

    songlink = ttk.Entry(songframe)
    songlink.insert(0, r[0]["external_urls"]["spotify"])
    songlink.place(relx=0.35, rely=0.89, relwidth=0.32)

    creds = r[0]["name"]
    songcredentials = ttk.Label(songframe, text=creds, background="lightgray", font=("Poppins", 10), wraplength=250)
    songcredentials.place(relx=0.37, rely=0.94)
    
def open_song_downloader():
    global mainframe
    global currentframe
    global songframe
    global playlistdownload
    global converterframe
    if currentframe != "song":
        if currentframe == "PLD":
            playlistdownload.destroy()
        if currentframe == "conv":
            converterframe.destroy()
        currentframe = "song"
        songframe = Frame(mainframe, bg="lightgray", width=800, height=655)
        songframe.place(relx=0.15, rely=0.01)
        #actual downloading part
        songdownloadlbl = ttk.Label(songframe, text="Song Downloader", font=("Poppins", 20), background="lightgray").place(relx=0.37, rely=0.02)
        songinstructlbl = ttk.Label(songframe, text="Enter Song Link Below: ", font=("Poppins", 12), background="lightgray").place(relx=0.4, rely=0.12)
        songlink = ttk.Entry(songframe)
        songlink.place(relx=0.35, rely=0.17, relwidth=0.32)
        beginsongdownload = partial(singledownload, songlink)
        checkbtn = ttk.Button(songframe, text="Download Song", command=beginsongdownload)
        checkbtn.place(relx=0.35, rely=0.21, relwidth=0.32)

        #song searcher for just incase its needed
        songsearchlbl = ttk.Label(songframe, text="Song Searcher", font=("Poppins", 12), background="lightgray")
        songsearchlbl.place(relx=0.445, rely=0.35)
        songsearch = ttk.Entry(songframe)
        songsearch.place(relx=0.35, rely=0.4, relwidth=0.32)
        songsearch_lbl = ttk.Label(songframe, text="Artist Name: ", background="lightgray", font=("Poppins", 12))
        songsearch_lbl.place(relx=0.21, rely=0.395)

        tracksearch = ttk.Entry(songframe)
        tracksearch.place(relx=0.35, rely=0.45, relwidth=0.32)
        tracksearchlbl = ttk.Label(songframe, text="Song Name: ", background="lightgray", font=("Poppins", 12))
        tracksearchlbl.place(relx=0.21, rely=0.445)
        songsearchbtn = ttk.Button(songframe, text="Search for Song", command=partial(songsearcher, songsearch, tracksearch))
        songsearchbtn.place(relx=0.35, rely=0.5, relwidth=0.32)
    else:
        return

def open_home(): #destroys all other frames to return back home
    global currentframe
    if currentframe != "Home":
        if currentframe == "PLD": ##using this method will prevent unfound bug
            playlistdownload.destroy()
        if currentframe == "song":
            songframe.destroy()
        currentframe = "Home"
    else:
        return

def open_fullapp(): #creates app beyond user ID grab
    global mainframe
    app.geometry("1000x800")

    fix_spotify_user_image = spotify_user["images"][0]["url"] #300x300 icon
    test = image_url_to_data(fix_spotify_user_image)
    label4 = ttk.Label(app, image=test)
    label4.photo = test
    label4.place(relx=0.025, rely=0.01)
    
    namelabel = ttk.Label(app, text="Welcome, " + spotify_user["display_name"], font=("Poppins", 16))
    namelabel.place(relx=0.1, rely=0.01)
    followerslabel = ttk.Label(app, text="Your Followers: " + str(spotify_user["followers"]["total"]))
    followerslabel.place(relx=0.1, rely=0.04)

    profileopen = partial(web, spotify_user["external_urls"]["spotify"])
    viewprofile = ttk.Button(app, text="View Profile in Web", command=profileopen)
    viewprofile.place(relx=0.1, rely=0.065)

    #frame for allowing multiple tabs
    mainframe = Frame(app, bg="white", width=950, height=670)
    mainframe.place(relx=0.025, rely=0.13)

    homeframe = Frame(mainframe, bg="lightgray", width=800, height=655)
    homeframe.place(relx=0.15, rely=0.01)
    ##home frame content##
    hometitle = ttk.Label(homeframe, text="Welcome To The Spotify Multi-Tool", font=("Poppins", 22), background="lightgray")
    hometitle.place(relx=0.22, rely=0.05)
    homedesc = ttk.Label(homeframe, text="This python application is developed by Alex Walker [AlexW03x]\nUtilising Spotify API and Public Python Modules\nFor Convenience and To Save Time!\n\n\nApplication will contain the following:\n*Playlist Converter\n*Playlist Downloader\n*Song Downloader\n*Maybe More Soon", background="lightgray", font=("Poppins", 12), justify="center")
    homedesc.place(relx=0.23, rely=0.13)
    
    viewgithubbtn = ttk.Button(homeframe, text="View Developer GitHub", padding=False)
    viewgithubbtn.place(relx=0.30, rely=0.45, relwidth=0.4)
    viewwebbtn = ttk.Button(homeframe, text="View Developer Website")
    viewwebbtn.place(relx=0.3, rely=0.5, relwidth=0.4)
    #buttons for adjusting frames#
    optlabel = ttk.Label(mainframe, text="Options: ", background="white").place(relx=0.045, rely=0.02)
    homebutton = ttk.Button(mainframe, text="Home", command=open_home).place(relx=0.02, rely=0.07, relwidth=0.11)
    playlistdownloader = ttk.Button(mainframe, text="Playlist Download", command=open_playlist_downloader).place(relx=0.02, rely=0.12, relwidth=0.11)
    playlistconverter = ttk.Button(mainframe, text="Playlist Converter", command=open_converter).place(relx=0.02, rely=0.17, relwidth=0.11)
    songdownloader = ttk.Button(mainframe, text="Song Download", command=open_song_downloader).place(relx=0.02, rely=0.22, relwidth=0.11)

def checkid(identification):
    identificationtext = identification.get()
    global userid
    global spotify_user
    try:
        spotify_user = sp.user(identificationtext)
        userid = identificationtext
        label2.configure(text="Status: User Found!")
        print("User found!") #for terminal viewing purpose
        label2.destroy()
        label1.destroy()
        identificationx.destroy()
        identification_button.destroy()
        open_fullapp()
        
    except:
        print("User not found!")
        label2.configure(text="Status: User doesn't exist!")

#begin application creation
app = Tk()
app.title("AlexW03x - Spotify Multitool")
app.iconbitmap("assets/spotify.ico")
app.resizable(False, False)

app.geometry("300x200")
label1 = ttk.Label(app, 
                   text="Enter Your Spotify Username:"
)
label1.place(relx=0.225, rely=0.225)

identificationx = ttk.Entry(app)
identificationx.place(relx=0.225, rely=0.375, width=155)

check_id = partial(checkid, identificationx)

identification_button = ttk.Button(app, text="Submit", command=check_id)
identification_button.place(relx=0.225, rely=0.5, width=155)

label2 = ttk.Label(app, text="Status: Pending User ID")
label2.place(relx=0.265, rely=0.65)
#execute application
app.mainloop()