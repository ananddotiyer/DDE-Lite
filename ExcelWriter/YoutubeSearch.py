#############################################################################################################################################
__filename__ = "YoutubeSearch.py"
__description__ = """Youtube search by text and similar functions.  Wrapped in functions.py

"""

__author__ = "Anand Iyer"
__copyright__ = "Copyright 2016-17, Anand Iyer"
__credits__ = ["Anand Iyer"]
__version__ = "2.6"
__maintainer__ = "Anand Iyer"
__email__ = "anand.iyer@moolya.com"
__status__ = "Testing" #Upgrade to Production once tested to function.
#############################################################################################################################################
from apiclient.discovery import build
import support

DEVELOPER_KEY = support.get_key("youtube")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build (YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

write_header = True

video_dict = {}
videos_list = []

class PlaylistClass:
    def __init__(self, playlist_url="", channel_url=None, playlistId=None, kind="video"):
        self.kind = kind
        self.playlist_url = playlist_url
        self.maxResults = 50
        self.part = "snippet" #id, snippet
        self.channel_url = channel_url
        self.playlistId = playlistId

class YoutubeClass:
    def __init__(self, q=None, relatedToVideoId=None, channelId=None, videoDuration="any", result_type="playlist,video"):
        self.q = q
        self.maxResults = 50
        self.relevanceLanguage = "en"
        self.part = "snippet" #id, snippet
        self.order = "viewCount" #date, rating, relevance, title, videoCount (for channels), viewCount
        self.channelId = channelId
        self.videoDuration = videoDuration #any, long, medium, short
        self.type = result_type #playlist, video, channel
        self.relatedToVideoId = relatedToVideoId #video_id
        
def get_videos_in_playlist (playlist_object, nextPageToken=None):
    response = youtube.playlistItems().list(
        pageToken=nextPageToken,
        playlistId=playlist_object.playlistId,
        part=playlist_object.part,
        maxResults=playlist_object.maxResults
      ).execute()
    for video in response["items"]:
        url = "https://www.youtube.com/watch?v=" + video["snippet"]["resourceId"]["videoId"].encode('ascii','ignore')
        title = video["snippet"]["title"].encode('ascii','ignore').translate (None, "'\"")
        description = video["snippet"]["description"].encode('ascii','ignore').translate (None, "'\"")
        embed_url = '=HYPERLINK("' + url + '","' + title+ '")'
        
        playlist_url = "https://www.youtube.com/playlist?list=" + playlist_object.playlistId
        kind_url = '=HYPERLINK("' + playlist_url + '","' + "playlist" + '")'
        
        video_dict["Title"] = embed_url
        video_dict["Description"] = description
        video_dict["Kind"] = kind_url
        videos_list.append (video_dict.copy())

    try:
      return response["nextPageToken"]
    except:
      pass
    
#############################################################get_playlists_and videos#################################################
#gets playlists or videos, depending on the 'type' parameter.
#If playlist need to be drilled down to get videos in it, 'get_playlist_videos' parameter should be True.
#In case, there's a relatedToVideoId passed to options, the method will find all related playlists/videos, depending on the 'type'
#'Type' must be video, if video-based parameters are used, including relatedToVideoId and videoDuration, else comment them here.
#############################################################get_playlists_and videos#################################################
def get_playlists_and_videos (youtube_object, get_playlist_videos=True, nextPageToken = None):
    response = youtube.search().list(
      pageToken=nextPageToken,
      relatedToVideoId=youtube_object.relatedToVideoId,
      channelId=youtube_object.channelId,
      videoDuration=youtube_object.videoDuration,
      q=youtube_object.q,
      type=youtube_object.type,
      relevanceLanguage=youtube_object.relevanceLanguage,
      part=youtube_object.part,
      order=youtube_object.order,
      maxResults=youtube_object.maxResults
    ).execute()

    for each in response["items"]:
      if youtube_object.channelId:
        channel_url = "https://youtube.com/channel/" + youtube_object.channelId
      else:
        channel_url = ""
      title = each["snippet"]["title"].encode('ascii','ignore').translate (None, "'\"")
      description = each["snippet"]["description"].encode('ascii','ignore').translate (None, "'\"")
      kind = each["id"]["kind"].encode('ascii','ignore')
      if "playlist" in kind:
        playlist_url = "https://youtube.com/playlist?list=" + each["id"]["playlistId"].encode('ascii','ignore')
        if get_playlist_videos:
            playlist_object = PlaylistClass (playlist_url,channel_url, each["id"]["playlistId"])

            nextPageToken_videos = get_videos_in_playlist (playlist_object, None) #nextPageToken defaults to None
            while nextPageToken_videos != None: #Until it's None again
                nextPageToken_videos = get_videos_in_playlist (playlist_object, nextPageToken_videos)
        else:
          embed_url = '=HYPERLINK("' + playlist_url + '","' + title+ '")'
          kind_url = '=HYPERLINK("' + channel_url + '","' + "channel" + '")'
          video_dict["Title"] = embed_url
          video_dict["Description"] = description
          video_dict["Kind"] = kind_url
          videos_list.append (video_dict.copy())
      elif "video" in kind:
        video_id = each["id"]["videoId"].encode('ascii','ignore')
        video_url = "https://youtube.com/watch?v=" + video_id
        embed_url = '=HYPERLINK("' + video_url + '","' + title + '")'
        kind_url = "video"

        video_dict["Title"] = embed_url
        video_dict["Description"] = description
        video_dict["Kind"] = kind_url
        videos_list.append (video_dict.copy())
        
    try:
      return response["nextPageToken"]
    except:
      pass
    
#############################################################Youtube related functions############################################################
#Get playlists/videos.
#Query using a query term, or from a particular channel id.
#Two ways to get channel id
#1. https://www.googleapis.com/youtube/v3/channels?key=AIzaSyCmIRuGHNlk_lQzL9_VnTMWNMvDneBwSkQ&forUsername=GoogleDevelopers&part=id
#2. About tab of the channel.
#Note that a one-time query (including using pageToken) can return a maximum of 500 results.
#Use with possible parameters include query, order, type, videoDefinition, videoDimension, videoDuration, relatedToVideoId
#Use these parameters with different values, or in combinations, in separate queries.  Note all combinations aren't valid.
#############################################################Main Program############################################################

def video_search (q):
    youtube_object = YoutubeClass (q=q,result_type="playlist,video,channel")
    
    nextPageToken_playlists = get_playlists_and_videos (youtube_object, True, None) #nextPageToken defaults to None
    counter = 0
    while nextPageToken_playlists != None and counter < 100: #Until it's None again or utmost 100 times
        counter += 1
        nextPageToken_playlists = get_playlists_and_videos (youtube_object, True, nextPageToken_playlists)
        
    return videos_list

def video_similar (relatedToVideoId):
    youtube_object = YoutubeClass (relatedToVideoId=relatedToVideoId, result_type="video")

    nextPageToken_playlists = get_playlists_and_videos (youtube_object, True, None) #nextPageToken defaults to None
    counter = 0
    while nextPageToken_playlists != None and counter < 100: #Until it's None again or utmost 100 times
        counter += 1
        nextPageToken_playlists = get_playlists_and_videos (youtube_object, True, nextPageToken_playlists)
        
    return videos_list