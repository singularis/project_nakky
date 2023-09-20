from youtuber import Youtuber
from video_convertor import Video_convertor
from translator import Translator
from speech import ToText
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
download_path = "video_download"
audio_path = "audio"
resolution = "480p"
project_id = os.getenv("PROJECT_ID")
video_link = os.getenv("VIDEO_LINK")
bucket_name = os.getenv("BUCKET_NAME")

youtuber = Youtuber(resolution)
video_convertor= Video_convertor(download_path, audio_path)
speech_to_text = ToText(project_id, bucket_name)
translator = Translator(project_id, bucket_name, "en")



#TODO Evaluate input methods
#link = input("Enter the YouTube video URL: ")

# download_file = youtuber.download_audio(video_link, audio_path)
# text_payload = speech_to_text.speech_to_text(audio_path=audio_path, download_file=download_file, language_code="ru-RU") # en-US ru-RU
# speech_to_text.write_translation_text_file()
translate_file = "audio_input_translate.txt"
# translator.read_original_text(download_file)
# translator.translate()
# translate_file = translator.write_translation_to_bucket()
speech_to_text.read_translated_text(translate_file)
speech_to_text.text_to_speech()

# video_convertor.split_to_audio(download_file)