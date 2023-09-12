import googleapiclient
from pprint import pprint
import pymongo as pm
import mysql.connector
from googleapiclient.discovery import build
import streamlit as st
import pandas as pd
channel_ids = ["UCYu6QgBdpTQfeKGtPSrZnKA","UCjNVDW-rkDYR0aOKp3E-2wg","UC59K-uG2A5ogwIrHw4bmlEg","UCZdGJgHbmqQcVZaJCkqDRwg","UC_4NoVAkQzeSaxCgm-to25A","UCkrkMMAyxC9vGNa6ZJYyscg","UCA2YOQHuWzVn1TWmlK5XYxA","UCJQJ4GjTiq5lmn8czf8oo0Q","UC9ufAseSDfIDdbhuQa9TwdA","UC0RhatS1pyxInC00YKjjBqQ"]

st.title("**Youtube scrapping project**")
inp = st.selectbox("select id : ",channel_ids)
# inp = st.text_input("enter channel_id: ")

@st.cache_data(ttl=60 * 60)
def get_data_from_youtube_api(n):
  api_key = 'AIzaSyBfCAz3-B2Rq0x1-VW0EeuFyMdbz1HbCG0'
  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
  channel_id = n
  response = youtube.channels().list(part='snippet,statistics,contentDetails',id=channel_id).execute()
  return response
 
but1 = st.button(label = "get details of channel_id",type = "primary")
if inp:
    if inp in channel_ids:
        if but1:
            st.subheader("successfully getting channel_data from YoutubeAPI")
        if st.checkbox("Show youtube data"):
            st.write(get_data_from_youtube_api(inp))
    else:
        st.warning("please enter valid channel_id")
      

# if inp in channel_ids:
#   if but2 == True:
#     my_col.insert_many(data)
#   if st.checkbox("Show data"):
#     for doc in data:
#       st.write(doc)
# else:
#     st.warning("Sorry we are not getting anything from channel to export to Mongodb")


# if st.session_state.button_clicked:
#   st.stop()
but2 = st.button(label = "exporting youtube channel id data to Mongodb",type ="primary")


@st.cache_data(ttl=60 * 60)
def get_data_from_youtube_api_channel(n):
  api_key = 'AIzaSyBfCAz3-B2Rq0x1-VW0EeuFyMdbz1HbCG0'
  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
  channel_id = n
  response = youtube.channels().list(part='snippet,statistics,contentDetails,status',id=channel_id).execute()
  return response["items"]

cid = []
cname = []
ctype = []
Cvc = []
Sc = []
Cd = []
Cs = []
Vc = []
pl_id = [] 

for i in channel_ids:
    res = get_data_from_youtube_api_channel(i)
    cid.append(res[0]["id"])
    cname.append(res[0]["snippet"]["title"])
    ctype.extend(["Personal channel" if len(i) == 24 else "Brand channel"])
    Cvc.append(res[0]["statistics"]["viewCount"])
    Sc.append(res[0]["statistics"]["subscriberCount"])
    Vc.append(res[0]["statistics"]["videoCount"])
    Cd.append(res[0]["snippet"]["description"])
    Cs.extend([res[0]["status"]["privacyStatus"]])
    pl_id.append(res[0]['contentDetails']['relatedPlaylists']["uploads"])
    # print(res["items"])
# st.write(cid)
# st.write(cname)
# st.write(ctype)
# st.write(Cvc)
# st.write(Cd)
# st.write(Cs)
# st.write(pl_id)
cp = {}
for i in range(len(channel_ids)):
  cp[channel_ids[i]] = pl_id[i]
# st.write(cp)

@st.cache_data(ttl=60 * 60)
def video_list(playlist_id):
  api_key = 'AIzaSyDGfIVT30FJQpZ_ODOiDVOXOie3CRAo-eQ'
  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

  response = youtube.playlistItems().list(
    part='contentDetails, snippet, status',
    playlistId=playlist_id,
    maxResults=10
  ).execute()

  video_information = []
  counter = 0
  video_ids = []
  for item in response['items']:
    video_information.append({
      'Video_id': item['contentDetails']['videoId'],
      'Video_name': item['snippet']['title'],
      'Video_description': item['snippet']['description'],
      'Published_date': item['snippet']['publishedAt'],
    })
    counter += 1
    if counter <= 10:
      video_ids.append(item['contentDetails']['videoId'])

  return video_ids

video_id = []
for i in range(len(pl_id)):
  video_id.extend(video_list(pl_id[i]))
# list_video_id = df["Video_id"].head(10)
# st.write(df)

@st.cache_data(ttl=60 * 60)
def get_data_from_youtube_api_video(vid):
    api_key = 'AIzaSyDGfIVT30FJQpZ_ODOiDVOXOie3CRAo-eQ'

    # Create a YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Get the video details
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=vid,
    )
    response = request.execute()

    return response["items"]
vid_id = []
vid_name = []
vid_thumb = []
vid_vc = []
vid_like_c = []
vid_fav_c = []
vid_dur = []
vid_com_c = []
vid_cap_stat = []
vid_desc = []
vid_publish_date = []
vid_dislike_c = []
vid_tags = []
vid_channel_id = []
vid_channel_name = []
# vid = df['Video_id'].head(10).tolist()


for i in video_id:
    res = get_data_from_youtube_api_video(i)

    vid_id.append(res[0]['id'])
    vid_name.append(res[0]['snippet']['title'])
    vid_thumb.append(res[0]['snippet']['thumbnails']['default']['url'])
    vid_vc.append(res[0]['statistics']['viewCount'])
    vid_like_c.append(res[0]['statistics']['likeCount'])
    vid_fav_c.append(res[0]['statistics']['favoriteCount'])
    vid_dur.append(res[0]['contentDetails']['duration'])
    vid_com_c.append(res[0]['statistics']['commentCount'])
    # vid_cap_stat.append(res["items"][0]['snippet']['captions']['status'])
    vid_desc.append(res[0]['snippet']['description'])
    vid_publish_date.append(res[0]['snippet']['publishedAt'])
    # vid_dislike_c.append(res["items"][0]['statistics']['dislikeCount'])
    vid_channel_id.append(res[0]['snippet']['channelId'])
    vid_channel_name.append(res[0]['snippet']['channelTitle'])
    # vid_tags.append(res[0]['snippet']['tags'])
# st.write(f"videos_ids = {vid_id}")
# st.write(f"videos_names = {vid_name}")
# st.write(f"video_like_counts = {vid_like_c}")
# st.write(f"video_comment_counts = {vid_com_c}")

@st.cache_data(ttl=60 * 60)
def comments(n):
  api_key = 'AIzaSyDGfIVT30FJQpZ_ODOiDVOXOie3CRAo-eQ'
  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

  try:
    request = youtube.commentThreads().list(part='id, snippet ,replies',videoId=n).execute()
    return request
  except:
    st.write(f"video with id {n} does not have any comments")

com_id = []
com_text = []
com_aut = []
com_pub = []
com_vid_id = []
# com_replies = []

for i in video_id[:50]:
  res = comments(i)
  if res:
    for item in res["items"]:
      com_id.append(item['snippet']['topLevelComment']['id'])
      com_text.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
      com_aut.append(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
      com_pub.append(item['snippet']['topLevelComment']['snippet']['publishedAt'])
      com_vid_id.append(i)
  else:
    print(f"video with id {i} does not have any comments")

# st.write(f"comment_ids = {com_id}")

vid_cap = []
for i in range(len(video_id[:10])):
    vid_cap.append("Not available")

dislike = []
for i in range(len(video_id)):
    dislike.append(0)

conn = pm.MongoClient("mongodb+srv://root:Ganesha143@cluster0.huqo0pe.mongodb.net/")
db = conn["youtubeAPI"]
my_col = db["youtube_to_MongoDB"]
channel_name = channel_ids.index(inp)
data = [
    {
        "Channel_Name": {
            "Channel_Name": cname[channel_name],
            "Channel_Id": cid[channel_name],
            "Subscription_Count": Sc[channel_name],
            "Channel_Views": Cvc[channel_name],
            "Channel_Description": Cd[channel_name],
            "Playlist_Id": pl_id[channel_name]
        },
        "Video_Id_1": {
            "Video_Id": video_id[0 if channel_name == 0 else channel_name*10],
            "Video_Name": vid_name[0 if channel_name == 0 else channel_name*10],
            "Video_Description": vid_desc[0 if channel_name == 0 else channel_name*9],
            "Tags": None,
            "PublishedAt": vid_publish_date[0 if channel_name == 0 else channel_name*10],
            "View_Count": vid_vc[0 if channel_name == 0 else channel_name*10],
            "Like_Count": vid_like_c[0 if channel_name == 0 else channel_name*10],
            "Dislike_Count": dislike[0 if channel_name == 0 else channel_name*10],
            "Favorite_Count": vid_fav_c[0 if channel_name == 0 else channel_name*10],
            "Comment_Count": vid_com_c[0 if channel_name == 0 else channel_name*10],
            "Duration": vid_dur[0 if channel_name == 0 else channel_name*10],
            "Thumbnail": vid_thumb[0 if channel_name == 0 else channel_name*10],
            "Caption_Status": vid_cap[0 if channel_name == 0 else channel_name],
            "Comments": {
                "Comment_Id_1": {
                    "Comment_Id": com_id[0 if channel_name == 0 else channel_name*10-1],
                    "Comment_Text": com_text[0 if channel_name == 0 else channel_name*10-1],
                    "Comment_Author": com_aut[0 if channel_name == 0 else channel_name*10-1],
                    "Comment_PublishedAt": com_pub[0 if channel_name == 0 else channel_name*10-1]
                },
                "Comment_Id_2": {
                    "Comment_Id": com_id[1 if channel_name == 0 else channel_name*10+1],
                    "Comment_Text": com_text[1 if channel_name == 0 else channel_name*10+1],
                    "Comment_Author": com_aut[1 if channel_name == 0 else channel_name*10+1],
                    "Comment_PublishedAt": com_pub[1 if channel_name == 0 else channel_name*10+1]
                }
            }
        },
        "Video_Id_2": {
            "Video_Id": video_id[1 if channel_name == 0 else channel_name*10+1],
            "Video_Name": vid_name[1 if channel_name == 0 else channel_name*10+1],
            "Video_Description": vid_desc[1 if channel_name == 0 else channel_name*10],
            "Tags": None,
            "PublishedAt": vid_publish_date[1 if channel_name == 0 else channel_name*10+1],
            "View_Count": vid_vc[1 if channel_name == 0 else channel_name*10+1],
            "Like_Count": vid_like_c[1 if channel_name == 0 else channel_name*10+1],
            "Dislike_Count": dislike[1 if channel_name == 0 else channel_name*10+1],
            "Favorite_Count": vid_fav_c[1 if channel_name == 0 else channel_name*10+1],
            "Comment_Count": vid_com_c[1 if channel_name == 0 else channel_name*10+1],
            "Duration": vid_dur[1 if channel_name == 0 else channel_name*10+1],
            "Thumbnail": vid_thumb[1 if channel_name == 0 else channel_name*10+1],
            "Caption_Status": vid_cap[1 if channel_name == 0 else channel_name],
            "Comments": {
                "Comment_Id_1": {
                    "Comment_Id": com_id[0 if channel_name == 0 else channel_name*9],
                    "Comment_Text": com_text[0 if channel_name == 0 else channel_name*9],
                    "Comment_Author": com_aut[0 if channel_name == 0 else channel_name*9],
                    "Comment_PublishedAt": com_pub[0 if channel_name == 0 else channel_name*9]
                },
                "Comment_Id_2": {
                    "Comment_Id": com_id[1 if channel_name == 0 else channel_name*10+2],
                    "Comment_Text": com_text[1 if channel_name == 0 else channel_name*10+2],
                    "Comment_Author": com_aut[1 if channel_name == 0 else channel_name*10+2],
                    "Comment_PublishedAt": com_pub[1 if channel_name == 0 else channel_name*10+2]
                }
            }
        }
    }
]

@st.cache_data(ttl=60 * 60)
def get_playlist_name(playlist_id):
    api_key = 'AIzaSyBfCAz3-B2Rq0x1-VW0EeuFyMdbz1HbCG0'

    # Create a YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Get the playlist information
    playlist_request = youtube.playlists().list(part="snippet", id=playlist_id)
    playlist_response = playlist_request.execute()

    # Extract the playlist title
    playlist_title = playlist_response["items"][0]["snippet"]["title"]
    # print(playlist_response["items"])
    return playlist_title

pl = []
for i in range(len(pl_id)):
  res = get_playlist_name(pl_id[i])
  pl.append(res)
if inp:
    if inp in channel_ids:
        if but2 == True:
            st.subheader("successfully getting channel_data from YoutubeAPI to Mongodb")
            my_col.insert_many(data)
        if st.checkbox("Show Mongodb data"):
            for doc in data:
                st.write(doc)
    else:
        st.warning("Sorry we are not getting anything from channel to export to Mongodb")
  
host = "localhost"
port = 3306
user = "root"
password = "Ganesha143@"

# Create a connection object
conn = mysql.connector.connect(host=host, port=port, user=user, password=password)
cursor = conn.cursor()
Db = cursor.execute("USE youtubeAPI")

try:
  cursor.execute("""CREATE TABLE Channel_details5(
                channel_id VARCHAR(255) PRIMARY KEY UNIQUE,
                channel_name VARCHAR(255),
                channel_type VARCHAR(255),
                channel_views BIGINT,
                video_count BIGINT,
                channel_description TEXT,
                channel_status VARCHAR(255));""")
except:
  print("Table already exists in database")

dic = {}
c_data = []
# index = ["channel_id", "channel_name", "channel_type", "channel_description", "channel_status"]
for i in range(len(cid)):
    dic["channel_id"] = cid[i]
    dic["channel_name"] = cname[i]
    dic["Channel_type"] = ctype[i]
    dic["channel_views"] = int(Cvc[i])
    # dic["Subscriber_count"] = Sc
    dic["Video_count"] = int(Vc[i])
    dic["Channel_description"] = Cd[i]
    dic["Channel_status"] = Cs[i]
# dic["playlist_id"] = pl_id
# dic["playlist_names"] = pl
    c_data.append(tuple(dic.values()))

for i in c_data:
    try:
      sql = cursor.execute(f"INSERT INTO Channel_details5(channel_id, channel_name, channel_type, channel_views,video_count,channel_description, channel_status) VALUES{i}")
    except mysql.connector.IntegrityError:
        print("Data not inserted because it was a duplicate.")

conn.commit()

try:
  cursor.execute("""CREATE TABLE playlist(
                    playlist_id VARCHAR(225),
                    playlist_name VARCHAR(255) NOT NULL,
                    channel_id VARCHAR(255) NOT NULL,
                    PRIMARY KEY (playlist_id),
                    FOREIGN KEY (channel_id) REFERENCES channel_details5(channel_id)
                  );""")
except:
  print("Table already exists in database")

dic = {}
p_data = []
# index = ["channel_id", "channel_name", "channel_type", "channel_description", "channel_status"]
for i in range(len(cid)):
    dic["playlist_id"] = pl_id[i]
    dic["playlist_names"] = pl[i]
    dic["channel_id"] = cid[i]
#     dic["channel_name"] = cname[i]
#     dic["Channel_type"] = ctype[i]
#     dic["channel_views"] = int(Cvc[i])
#     # dic["Subscriber_count"] = Sc
#     dic["Video_count"] = int(Vc[i])
#     dic["Channel_description"] = Cd[i]
#     dic["Channel_status"] = Cs[i]
# dic["playlist_id"] = pl_id
# 
    p_data.append(tuple(dic.values()))
print(p_data)
for i in p_data:
    try:
        sql = cursor.execute(f"INSERT INTO playlist(playlist_id, playlist_name, channel_id) VALUES{i}")
    except mysql.connector.IntegrityError:
        print("Data not inserted because it was a duplicate.")

conn.commit()

@st.cache_data(ttl=60 * 60)
def get_playlist_id_by_channel_id(channel_id):
  api_key = 'AIzaSyDGfIVT30FJQpZ_ODOiDVOXOie3CRAo-eQ'
  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
  channel_id = channel_id  # example channel_ID

# selected **channel** from resource menu

  response = youtube.channels().list(part='snippet,statistics,contentDetails',id=channel_id).execute()
  return response["items"][0]['contentDetails']['relatedPlaylists']["uploads"]

playlist_id = []
for i in vid_channel_id:
  playlist_id.append(get_playlist_id_by_channel_id(i))


video_df = pd.DataFrame({
    "playlist_id":playlist_id,
    "video_id": video_id,
    "video_name": vid_name,
    "video_view_count": vid_vc,
    "video_like_count": vid_like_c,
    "video_fav_count": vid_fav_c,
    "video_duration": vid_dur,
    "video_thumbnail":vid_thumb,
    "comment_count": vid_com_c,
    "video_description": vid_desc,
    "video_publish_date":vid_publish_date,
    "video_channel_id":vid_channel_id
})
video_df = video_df.drop_duplicates()

video_df['video_publish_date'] = pd.to_datetime(video_df['video_publish_date'], format='%Y-%m-%d')
# pub_date = list(video_df["video_publish_date"])
# @st.ache_data(ttl=60 * 60)
# def convert_string_to_date_without_tz(df, column_name):c
video_df['video_publish_date'] = video_df['video_publish_date'].dt.tz_localize(None)

video_pub = list(video_df['video_publish_date'])
# st.write(video_pub)

# vid_d = list(video_df["video_duration"])
# st.write(vid_d)

@st.cache_data(ttl=60 * 60)
def convert_duration_string_to_seconds(res):
  if len(res) == 8:
    minutes = int(res[2:4])
    seconds = int(res[5:7])
    return minutes * 60 + seconds
  elif len(res) == 7 and res[3] == "M":
    minutes = int(res[2:3])
    seconds = int(res[4:6])
    return minutes * 60 + seconds
  elif len(res) == 7 and res[3] == "H":
    hours = int(res[2:3])
    seconds = int(res[4:6])
    return hours * 3600 + seconds
  elif len(res) == 7:
    minutes = int(res[2:4])
    seconds = int(res[5:6])
    return minutes * 60 + seconds
  elif len(res) == 6:
    minutes = int(res[2:3])
    seconds = int(res[4:5])
    return minutes * 60 + seconds
  elif len(res) == 5 and res.endswith("S"):
    seconds = int(res[2:4])
    return seconds
  elif len(res) == 5 and res.endswith("M"):
    minutes = int(res[2:4])
    return minutes
  elif len(res) == 4 and res.endswith("M"):
    minutes = int(res[2:3])
    return minutes*60
  elif len(res) == 4 and res.endswith("S"):
    seconds = int(res[2:3])
    return seconds


video_dur_int = []
for i in vid_dur:
  video_dur_int.append(convert_duration_string_to_seconds(i))
# st.write(vid_dur)

ch_name = vid_channel_name

# st.write(ch_name)
try:
  cursor.execute("""CREATE TABLE video4(
                  Video_id VARCHAR(255),
                  Playlist_id VARCHAR(255),
                  Video_name TEXT,
                  Video_description TEXT,
                  Video_publish_date VARCHAR(255),
                  video_View_count BIGINT,
                  video_Like_count BIGINT,
                  video_Dislike_count INT,
                  video_Favourite_count INT,
                  video_comment_count INT,
                  Video_duration INT,
                  Video_thumbnail VARCHAR(255),
                  channel_id VARCHAR(255),
                  FOREIGN KEY (Playlist_id) REFERENCES playlist(playlist_id)
                  );""")
except:
  print("Table already exists in database")


dic = {}
v_data = []

for i in range(len(video_id)):
    dic["video_id"] = video_id[i]
    dic["playlist_id"] = playlist_id[i]
    dic["video_name"] = vid_name[i]
    dic["video_description"] =  vid_desc[i]
    dic["video_publish_date"] = video_pub[i]
    dic["video_view_count"] = int(vid_vc[i])
    dic["video_like_count"] = int(vid_like_c[i])
    dic["video_dislike_count"] = int(dislike[i])
    dic["video_fav_count"] = int(vid_fav_c[i])
    dic["comment_count"] =  int(vid_com_c[i])
    dic["video_duration"] = video_dur_int[i]
    dic["video_thumbnail"] = vid_thumb[i]
    dic["channel_id"] = vid_channel_id[i]
    v_data.append(tuple(dic.values()))
try:
  cursor.executemany("""INSERT INTO video4(Video_id, Playlist_id, Video_name, Video_description, video_publish_date, video_View_count, video_Like_count, video_Dislike_count,video_Favourite_count, video_comment_count, Video_duration, Video_thumbnail, channel_id) VALUES
      ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)""", v_data)
except:
   print("duplicates values not allowed")
conn.commit() # st.write(vid_channel_id)

comment_df = pd.DataFrame({
    "comment_id":com_id,
    "comment_text":com_text,
    "comment_author":com_aut,
    "comment_publish_date":com_pub,
    "Video_id":com_vid_id
})

comment_df["comment_publish_date"] = pd.to_datetime(comment_df['comment_publish_date'], format='%Y-%m-%d')
comment_df["comment_publish_date"] = comment_df["comment_publish_date"].dt.tz_localize(None)
comment_pub = list(comment_df['comment_publish_date'])
# st.write(comment_pub)
# st.write(video_pub)
try:
  cursor.execute("""CREATE TABLE comment3(
          comment_id VARCHAR(225),
          comment_text TEXT NOT NULL,
          comment_author VARCHAR(255) NOT NULL,
          comment_publish_date DATETIME,
          Video_id VARCHAR(255)
        );""")
except:
  print("Table already exists in database")
dic = {}
com_data = []
# index = ["channel_id", "channel_name", "channel_type", "channel_description", "channel_status"]
for i in range(len(video_id)):
    dic["comment_id"] = com_id[i]
    dic["comment_text"] = com_text[i]
    dic["comment_author"] = com_aut[i]
    dic["comment_pub_date"] = comment_pub[i]
    dic["Video_id"] = video_id[i]
    com_data.append(tuple(dic.values()))
try:
  cursor.executemany("""INSERT INTO comment3(comment_id,comment_text,comment_author,comment_publish_date,Video_id) VALUES(%s, %s, %s, %s ,%s)""", com_data)
except:
   print("Duplicates are not allowed")
conn.commit() # st.write(vid_channel_id)
    # except mysql.connector.IntegrityError:
    #     print("Data not inserted because it was a duplicate.")
conn.commit() # st.write(vid_channel_id)

que1 = "SELECT * FROM channel_details5"

# st.write(D)

que2 = "SELECT * FROM playlist"

que3 = "SELECT * FROM video1"

que4 = "SELECT * FROM comment3"

but3 = st.button(label = "click here to export MongoDB to sql ",type="primary")
if inp:
    if inp in channel_ids:
        if but3:
            st.subheader("successfully getting channel_data from Mongodb to Mysql")
        if st.checkbox("show channel_table"):
            df = pd.read_sql("SELECT * FROM Channel_details5",conn)
            st.write(df)
        if st.checkbox("show playlist_table"):
            df = pd.read_sql("SELECT * FROM playlist",conn)
            st.write(df)
        if st.checkbox("show video_table"):
            df = pd.read_sql("SELECT * FROM video4",conn)
            st.write(df)
        if st.checkbox("show comment_table"):
            df = pd.read_sql("SELECT * FROM comment3",conn)
            st.write(df)
    else:
        st.warning("please enter channel_id")
# st.write(D)

conn = mysql.connector.connect(host='localhost', user='root', password='Ganesha143@', database='youtubeAPI')
cursor = conn.cursor()
# conn = mysql.connector.connect(host='localhost', user='root', password='password', database='youtubeAPI')
# cursor = conn.cursor()

# Define the SQL queries
sql_queries = {
   '1.What are the names of all the videos and their corresponding channels?': """SELECT video4.Video_name, channel_details5.channel_name
FROM video4
INNER JOIN channel_details5 ON video4.channel_id = channel_details5.channel_id;
""",
    '2.Which channels have the most number of videos?': """SELECT channel_details5.channel_name, channel_details5.video_count
FROM channel_details5
GROUP BY channel_details5.channel_name
ORDER BY channel_details5.video_count DESC;
""",
    '3.What are the top 10 most viewed videos?': """SELECT video4.Video_name, video4.video_View_count, channel_details5.channel_name
FROM video4
INNER JOIN channel_details5 ON video4.channel_id = channel_details5.channel_id
GROUP BY channel_details5.channel_name
ORDER BY video4.video_View_count DESC
LIMIT 10;
""",
    '4.How many comments were made on each video?': """SELECT video4.Video_name, COUNT(comment3.comment_id) AS num_comments
FROM video4
INNER JOIN comment3 ON video4.Video_id = comment3.Video_id
GROUP BY video4.Video_id;""",
    '5.Which videos have the highest number of likes?': """SELECT video4.Video_name, video4.video_Like_count, channel_details5.channel_name
FROM video4
INNER JOIN channel_details5 ON video4.channel_id = channel_details5.channel_id
ORDER BY video4.video_Like_count DESC LIMIT 1;""",
    '6.What is the total number of likes and dislikes for each video?': """
SELECT video4.Video_name, video4.video_Like_count, video4.video_Dislike_count
FROM video4;""",
    '7.What is the total number of views for each channel and corresponding channels?': """SELECT channel_name,channel_views FROM channel_details5 GROUP BY channel_name ORDER BY channel_views ASC""",
    '8.What are the names of all the channels that have published videos in the year 2022?': """SELECT channel_details5.channel_name
FROM video4
INNER JOIN channel_details5 ON video4.channel_id = channel_details5.channel_id
WHERE video4.Video_publish_date BETWEEN '2022-01-01' AND '2022-12-31';
""",
    '9.What is the average duration of all videos in each channel?': """SELECT channel_details5.channel_name,AVG(video4.Video_duration) AS avg_duration
FROM channel_details5 INNER JOIN video4 ON channel_details5.channel_id = video4.channel_id
GROUP BY channel_details5.channel_id;
""",
    '10.Which videos have the highest number of comments?': """SELECT video4.Video_name, video4.video_comment_count, channel_details5.channel_name
FROM video4
INNER JOIN channel_details5 ON video4.channel_id = channel_details5.channel_id
ORDER BY video4.video_comment_count DESC LIMIT 1;""",
}

multiselect = st.multiselect('Select a query', list(sql_queries.keys()))

# Iterate over the checkbox values and execute the corresponding SQL query
if multiselect:
    for query in multiselect:
        df = pd.read_sql(sql_queries[query], conn)
        st.write(df)



data = pd.DataFrame({
    "Channel name": cname,
    "View count": Cvc,
    "Subscriber count": Sc,
    "Video count": Vc,
})

# Create a vertical bar graph of the subscriber count

with st.expander("statistical data of each channel"):
    st.bar_chart(
        data,
        x="Channel name",
        y=["View count", "Subscriber count", "Video count"],
        color=["#ffaa00", "#00ffff", '#09ab3b'],
        width = 0,
        height = 0
    )

# with st.expander("Bar graph of Video count of each channel"):
#     st.plotly_chart(fig_video_count)
# with st.expander("Bar graph of View count of each channel"):
#     st.plotly_chart(fig_view_count)


