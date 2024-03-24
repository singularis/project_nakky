import logging
import time
import yaml

from youtuber import Youtuber
from video_convertor import Video_convertor
from translator import Translator
from speech import ToText

# Load secrets.yaml
with open('secrets.yaml', 'r') as file:
    secrets = yaml.safe_load(file)

project_id = secrets['project_id']
video_link = secrets['video_link']
bucket_name = secrets['bucket_name']

logging.basicConfig(level=logging.DEBUG)
download_path = "video_download"
audio_path = "audio"
video_path = "video_input"
output_path = "done"
resolution = "1080p"
voice_type = "en-US-Standard-D"  # Currently not supported: en-US-Studio-M, to try: en-US-Standard-D, default
# en-US-Standard-A

youtuber = Youtuber(resolution)
video_convertor = Video_convertor(download_path, audio_path, video_path, output_path)
speech_to_text = ToText(project_id, bucket_name, voice_type)
translator = Translator(project_id, bucket_name, "en")

start_time = time.time()
download_audio = youtuber.download_audio(video_link, audio_path)
text_payload = speech_to_text.speech_to_text(audio_path=audio_path, download_file=download_audio,
                                             language_code="ru-RU")  # en-US ru-RU
speech_to_text.write_translation_text_file()
translator.read_original_text(download_audio)
translator.translate()
translate_file = translator.write_translation_to_bucket()
speech_to_text.read_translated_text(translate_file)
speech_to_text.text_to_speech()
translated_audio = speech_to_text.download_converted_file()
download_video = youtuber.download_video(video_link, video_path)
video_convertor.join_video_audio(video_name=download_video, input_audio_path=translated_audio)
end_time = time.time()
execution_time = end_time - start_time
logging.info(f"Execution time {execution_time}")
logging.info("Video processed successfully.")