import os
import logging
from google.cloud import storage
from google.cloud import speech

class ToText():
    def __init__(self, project_id, bucket_name):
        self.project_id =project_id
        self.bucket_name = bucket_name
        self.full_translation = []
        self.audio_file = ""
        self.file_path = ""
    def put_in_to_bucket(self):
        client = storage.Client()
        bucket = client.get_bucket(self.bucket_name)
        blob = bucket.blob(self.audio_file)
        blob.upload_from_filename(self.file_path)
    def speech_to_text(self, audio_path: str,download_file: str, language_code: str) -> speech.RecognizeResponse:
        # Instantiates a client
        client = speech.SpeechClient()
        self.audio_file = download_file
        self.file_path = os.path.join(audio_path, self.audio_file)
        self.put_in_to_bucket()

        # The name of the audio file to transcribe
        gcs_uri = f"gs://{self.bucket_name}/{self.audio_file}"

        audio = speech.RecognitionAudio(uri=gcs_uri)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            language_code=language_code,
            audio_channel_count = 2,
        )

        # Detects speech in the audio file
        operation = client.long_running_recognize(config=config, audio=audio)
        logging.info('Waiting for operation to complete...')
        response = operation.result()
        translation = []
        for result in response.results:
            alternative = result.alternatives[0]
            translation.append(alternative.transcript)
        self.full_translation = str(' '.join(translation))
        return self.full_translation
    def write_translation_text_file(self):
        text_file_name = f"{self.audio_file.split('.')[0]}.txt"
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        # Create a blob (file) in the bucket
        blob = bucket.blob(text_file_name)
        # Write the string to the blob as text
        blob.upload_from_string(self.full_translation, content_type='text/plain;charset=utf-8')
        logging.info(f'String has been written to gs://{self.bucket_name}/{text_file_name}')