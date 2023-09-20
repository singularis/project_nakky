from pytube import YouTube
import logging

class Youtuber:
    def __init__(self ,resolution):
        self.resolution = resolution
    def download_audio(self, link, download_path):
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.filter(only_audio=True, file_extension='webm').first()
        try:
            # TODO File name should be autogenerated 
            file_name = "audio_input.webm"
            youtubeObject.download(output_path=download_path, filename=file_name)
        except:
            logging.fatal("Failed to download")
        logging.info(f"Download is completed successfully {file_name}")
        return file_name
    def download_video(self, link, download_path):
        youtubeObject = YouTube(link)
        youtubeObject = youtubeObject.streams.filter(type="video", res=self.resolution, file_extension='mp4').first()
        try:
            # TODO File name should be autogenerated 
            file_name = "video_input.mp4"
            youtubeObject.download(output_path=download_path, filename=file_name)
        except:
            logging.fatal("Failed to download")
        logging.info(f"Download is completed successfully {file_name}")
        return file_name