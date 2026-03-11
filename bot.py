import os
import time
import random
import requests

from moviepy.editor import VideoFileClip

# PEXELS API
PEXELS_API = "qYSrqLORUC6G5NExtzE4ij69cGjH919KOwGaztP6txDwzNkD5YQ9AMAm"

# VIDEO ARAMA
def get_video():

    query = random.choice(["cat","dog"])

    url = f"https://api.pexels.com/videos/search?query={query}&orientation=portrait&per_page=15"

    headers = {
        "Authorization":PEXELS_API
    }

    r = requests.get(url,headers=headers)

    data = r.json()

    video = random.choice(data["videos"])

    return video["video_files"][0]["link"]


# VIDEO İNDİR
def download_video(url):

    print("video indiriliyor...")

    r = requests.get(url)

    with open("video.mp4","wb") as f:
        f.write(r.content)

    print("video indirildi")


# SHORTS KES
def cut_short():

    print("video kesiliyor...")

    clip = VideoFileClip("video.mp4")

    short = clip.subclip(0,15)

    short.write_videofile("short.mp4")

    print("short hazır")


# YOUTUBE YÜKLE
def upload_youtube():

    print("youtube upload başlatılıyor")

    os.system("python upload.py")

    print("youtube upload tamam")


# DOSYA TEMİZLE
def clean_files():

    if os.path.exists("video.mp4"):
        os.remove("video.mp4")

    if os.path.exists("short.mp4"):
        os.remove("short.mp4")

    print("dosyalar silindi")


# ANA ÇALIŞMA
def main():

    video = get_video()

    download_video(video)

    cut_short()

    upload_youtube()

    clean_files()


while True:

    main()

    print("1 saat bekleniyor...")

    time.sleep(3600)
