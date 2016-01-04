import tweepy
import spotipy
import spotipy.util as util
import time
from tweepy import OAuthHandler

#Twitter keys and access tokens
consumer_key="[ENTER KEY HERE]"
consumer_secret = "[ENTER SECRET HERE]"
access_token="[ENTER TOKEN HERE]"
access_token_secret="[ENTER TOKEN SECRET HERE]"

#Spotify keys and access tokens
username = "[ENTER USERNAME HERE]"
scope = "playlist-modify-private"
playlist_id = "[ENTER REQUIRED PLAYLIST ID]"
token=util.prompt_for_user_token(
            username,
            scope,
            client_id="[ENTER SPOTIFY CLIENT ID HERE]",
            client_secret="[ENTER CLIENT SECRET HERE]",
            redirect_uri="[ENTER REDIRECT HERE]" # I believe this can be any web address
            )
playlistList = []
trackURI = ""

#Twitter OAuth stuff
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

#Creates instance
api=tweepy.API(auth)
sp = spotipy.Spotify(auth=token)
sp.trace=False


##Searches through playlist and adds URIs to list
results = sp.user_playlist(username,playlist_id,fields="tracks")
tracks = results["tracks"]
for i, item in enumerate(tracks["items"]):
    track = item["track"]
    trackURI = track["uri"].replace("spotify:track:","")
    playlistList.append([trackURI])
    
while True:
    #returns 50 items from api.search for #[Whatever your hashtag is!]
    rPiTweet = tweepy.Cursor(api.search,q="#[ENTER HASHTAG HERE]").items(50)
    for tweet in rPiTweet:
        #removes hashtag from tweet
        tweetSong = tweet.text.replace("#[ENTER YOUR HASHTAG HERE]","")
        
        ## Searches for and displays first item from Spotify
        ## Outputs as item, song title 
        searchResults = sp.search(tweetSong,limit=1)
        for i, t in enumerate(searchResults["tracks"]["items"]):   
            trackId = [t["href"].replace("https://api.spotify.com/v1/tracks/","")]
        ##print ("current ID =",trackId)
        ##print ("current playlistList =",playlistList)
            print (tweet.user.name,"requested",t["name"])
        
        ##Searches playlist list to see if track already exists   
        if trackId in playlistList:
            print ("We've already got it!")
        else:
            print ("Adding it now!")
            playlistList.append(trackId)
            addTrack=sp.user_playlist_add_tracks(username,playlist_id,trackId,position=0)
    #print (playlistList)
       
    time.sleep(5)
