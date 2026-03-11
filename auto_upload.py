import os
import time
import random
import requests
import hashlib
from moviepy.editor import VideoFileClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

PEXELS_API="qYSrqLORUC6G5NExtzE4ij69cGj919KOwGaztP6txDwzNkD5YQ9AMAm"

WAIT=3600

if not os.path.exists("videos"):
    os.makedirs("videos")


def get_hash(file):
    with open(file,'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def downloaded_before(h):

    if not os.path.exists("uploaded.txt"):
        return False

    with open("uploaded.txt") as f:
        return h in f.read()


def save_hash(h):

    with open("uploaded.txt","a") as f:
        f.write(h+"\n")


def download_video():

    query=random.choice(["cat","dog"])

    url=f"https://api.pexels.com/videos/search?query={query}&orientation=portrait&per_page=20"

    headers={
        "Authorization":PEXELS_API
    }

    r=requests.get(url,headers=headers).json()

    video=r["videos"][0]["video_files"][0]["link"]

    data=requests.get(video)

    path="videos/api_video.mp4"

    with open(path,"wb") as f:
        f.write(data.content)

    return path


def add_music(video):

    clip=VideoFileClip(video)

    audio=AudioFileClip("music/music.mp3")

    audio=audio.set_duration(clip.duration)

    final=clip.set_audio(audio)

    output="videos/final.mp4"

    final.write_videofile(output)

    return output


def upload(video):

    with open("token.pickle","rb") as f:
        creds=pickle.load(f)

    youtube=build("youtube","v3",credentials=creds)

    request=youtube.videos().insert(

        part="snippet,status",

        body={

            "snippet":{
                "title":"Cute Cats & Dogs 🐶🐱 #shorts",
                "description":"Cute cats and dogs 🐶🐱 #shorts #cats #dogs #pets",
                "tags":["shorts","cats","dogs","pets"],
                "categoryId":"15"
            },

            "status":{
                "privacyStatus":"public"
            }

        },

        media_body=MediaFileUpload(video)

    )

    response=request.execute()

    print("Video yüklendi:",response["id"])


while True:

    files=os.listdir("videos")

    videos=[f for f in files if f.endswith(".mp4")]

    if videos:
        video="videos/"+videos[0]
    else:
        print("Video yok API'den indiriliyor")
        video=download_video()

    h=get_hash(video)

    if downloaded_before(h):
        os.remove(video)
        continue

    final=add_music(video)

    upload(final)

    save_hash(h)

    os.remove(video)
    os.remove(final)

    print("Video yüklendi ve silindi")

    time.sleep(WAIT)
