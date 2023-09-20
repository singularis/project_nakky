from youtuber import Youtuber
from video_convertor import Video_convertor
from translator import Translator
from speech import ToText
from dotenv import load_dotenv
import os
import logging
import time

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
download_path = "video_download"
audio_path = "audio"
video_path = "video_input"
output_path = "done"
resolution = "1080p"
project_id = os.getenv("PROJECT_ID")
video_link = os.getenv("VIDEO_LINK")
bucket_name = os.getenv("BUCKET_NAME")

youtuber = Youtuber(resolution)
video_convertor= Video_convertor(download_path, audio_path, video_path, output_path)
speech_to_text = ToText(project_id, bucket_name)
translator = Translator(project_id, bucket_name, "en")



#TODO Evaluate input methods
#link = input("Enter the YouTube video URL: ")

start_time = time.time()
download_audio = youtuber.download_audio(video_link, audio_path)
text_payload = speech_to_text.speech_to_text(audio_path=audio_path, download_file=download_audio, language_code="ru-RU") # en-US ru-RU
speech_to_text.write_translation_text_file()
translator.read_original_text(download_audio)
translator.translate()
translate_file = translator.write_translation_to_bucket()
speech_to_text.read_translated_text(translate_file)
speech_to_text.text_to_speech()
translated_audio = speech_to_text.download_converted_file()
download_video = youtuber.download_video(video_link, video_path)
# download_video = "video_input.mp4"
# translated_audio = "./translated_audio/audio_input.mp3"
video_convertor.join_video_audio(video_name=download_video, input_audio_path=translated_audio)
end_time = time.time()
execution_time = end_time - start_time
logging.info(f"Execution time {execution_time}")
logging.info("Video processed successfully.")