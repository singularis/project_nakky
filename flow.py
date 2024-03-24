from youtuber import Youtuber
from video_convertor import Video_convertor
from translator import Translator
from speech import ToText
import os


class Flow:
    def __init__(self, resolution, download_path, audio_path, video_path,
                 output_path, project_id, bucket_name, voice_type, source_language):
        self.youtuber = None
        self.resolution = resolution
        self.download_path = download_path
        self.audio_path = audio_path
        self.video_path = video_path
        self.output_path = output_path
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.voice_type = voice_type
        self.source_language = source_language
        self.ensure_directories_exist()
        self.video_convertor = Video_convertor(download_path, audio_path, video_path, output_path)
        self.speech_to_text = ToText(project_id, bucket_name, voice_type)
        self.translator = Translator(project_id, bucket_name, "en")

    def ensure_directories_exist(self):
        for path in [self.download_path, self.audio_path, self.video_path, self.output_path]:
            os.makedirs(path, exist_ok=True)

    def youtube(self, video_link):
        self.youtuber = Youtuber(self.resolution)
        download_audio = self.youtuber.download_audio(video_link, self.audio_path)
        download_video = self.youtuber.download_video(video_link, self.video_path)
        self.common(audio_file=download_audio, video_file=download_video)

    def local(self, video_file):
        # separated_audio_and_video = self.video_convertor.split_to_audio(video_file)
        separated_audio_and_video = {"audio_file": "continuity.webm", "vide_file": "continuity.mp4"}
        self.common(audio_file=separated_audio_and_video["audio_file"],
                    video_file=separated_audio_and_video["vide_file"])

    def common(self, audio_file, video_file):
        self.speech_to_text.speech_to_text(audio_path=self.audio_path,
                                           download_file=audio_file,
                                           language_code=self.source_language)
        self.speech_to_text.write_translation_text_file()
        self.translator.read_original_text(audio_file)
        self.translator.translate()
        translate_file = self.translator.write_translation_to_bucket()
        self.speech_to_text.read_translated_text(translate_file)
        self.speech_to_text.text_to_speech()
        translated_audio = self.speech_to_text.download_converted_file()
        self.video_convertor.join_video_audio(video_name=video_file, input_audio_path=translated_audio)
        self.speech_to_text.download_all_files_from_bucket("./bucket_full_backup")
        self.speech_to_text.cleanup_bucket()
