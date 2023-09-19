from youtuber import Youtuber
from video_convertor import Video_convertor
import logging

logging.basicConfig(level=logging.DEBUG)
download_path = "video_download"
audio_path = "audio"
resolution = "480p"

youtuber = Youtuber(download_path, resolution)
video_convertor= Video_convertor(download_path, audio_path)


#TODO Evaluate input methods
#link = input("Enter the YouTube video URL: ")
link = "https://www.youtube.com/watch?v=RVbkpVB4C-w"
download_file = youtuber.download_audio(link)
video_convertor.split_to_audio(download_file)