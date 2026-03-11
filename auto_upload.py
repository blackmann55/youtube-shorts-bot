import os
import requests
import random
import hashlib
import pickle
from moviepy.editor import VideoFileClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PEXELS_API="qYSrqLORUC6G5NExtzE4ij69cGjH919KOwGaztP6txDwzNkD5YQ9AMAm"

LOG_FILE="uploaded.txt"


def get_hash(file):
    with open(file,'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def downloaded_before(h):

    if not os.path.exists(LOG_FILE):
        return False

    with open(LOG_FILE) as f:
        lines=f.read().splitlines()

    return h in lines


def save_hash(h):

    if not os.path.exists(LOG_FILE):
        open(LOG_FILE,"w").close()

    with open(LOG_FILE) as f:
        lines=f.read().splitlines()

    lines.append(h)

    # sadece son 5 video tutulur
    lines=lines[-5:]

    with open(LOG_FILE,"w") as f:
        for l in lines:
            f.write(l+"\n")


def download_video():

    query=random.choice(["cat","dog"])

    url=f"https://api.pexels.com/videos/search?query={query}&orientation=portrait&per_page=20"

    headers={
        "Authorization":PEXELS_API
    }

    r=requests.get(url,headers=headers).json()

    if "videos" not in r or len(r["videos"]) == 0:
        print("API video bulamadı")
        return None

    videos=r["videos"]

    random.shuffle(videos)

    for v in videos:

        file=v["video_files"][0]["link"]

        try:

            data=requests.get(file,timeout=30)

            path="video.mp4"

            with open(path,"wb") as f:
                f.write(data.content)

            return path

        except:
            continue

    return None


def add_music(video):

    clip=VideoFileClip(video)

    audio=AudioFileClip("music/music.mp3")

    audio=audio.set_duration(clip.duration)

    final=clip.set_audio(audio)

    output="final.mp4"

    final.write_videofile(output,codec="libx264",audio_codec="aac")

    return output


def upload(video):

    with open("token.pickle","rb") as f:
        creds=pickle.load(f)

    youtube=build("youtube","v3",credentials=creds)

    title=random.choice([
        "Cute Cats & Dogs 🐶🐱 #shorts",
        "Funny Cat & Dog Moment 🐱🐶 #shorts",
        "Cute Animal Friends 🐶🐱 #shorts"
    ])

    description="Cute cats and dogs 🐶🐱 #shorts #cats #dogs #pets #animals"

    request=youtube.videos().insert(

        part="snippet,status",

        body={

            "snippet":{
                "title":title,
                "description":description,
                "tags":["shorts","cats","dogs","pets","animals"],
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


print("Video indiriliyor...")

video=download_video()

if video is None:
    print("Video bulunamadı script bitiyor")
    exit()


h=get_hash(video)

if downloaded_before(h):
    print("Video daha önce yüklenmiş, yeni video aranıyor")
    os.remove(video)
    exit()


print("Müzik ekleniyor...")

final=add_music(video)

print("YouTube'a yükleniyor...")

upload(final)

save_hash(h)

os.remove(video)
os.remove(final)

print("Tamamlandı")
