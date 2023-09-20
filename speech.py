import os
import logging
from google.cloud import storage
from google.cloud import speech
from google.cloud import texttospeech

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
    def read_translated_text(self, input_file_name):
        storage_client = storage.Client()
        source_bucket = storage_client.bucket(self.bucket_name)
        source_blob = source_bucket.blob(input_file_name)
        # Read the content of the source file
        self.translate_source_content = source_blob.download_as_text()
        print(self.translate_source_content)
    def text_to_speech(self):
        # client = texttospeech.TextToSpeechLongAudioSynthesizeClient()
        # synthesis_input = texttospeech.SynthesisInput(text=self.translate_source_content)
        # voice = texttospeech.VoiceSelectionParams(
        #     language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        # )

        # # Select the type of audio file you want returned
        # audio_config = texttospeech.AudioConfig(
        #     audio_encoding=texttospeech.AudioEncoding.MP3
        # )

        # # Perform the text-to-speech request on the text input with the selected
        # # voice parameters and audio file type
        # response = client.synthesize_speech(
        #     input=synthesis_input, voice=voice, audio_config=audio_config
        # )
        # # The response's audio_content is binary.
        # with open("output.mp3", "wb") as out:
        #     # Write the response to the output file.
        #     out.write(response.audio_content)
        #     print('Audio content written to file "output.mp3"')
        client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

        input = texttospeech.SynthesisInput(
            text=self.translate_source_content
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name="en-US-Standard-A"
        )

        parent = f"projects/{self.project_id}/locations/us-central1"

        request = texttospeech.SynthesizeLongAudioRequest(
            parent=parent,
            input=input,
            audio_config=audio_config,
            voice=voice,
            output_gcs_uri=f"gs://{self.bucket_name}/{self.audio_file.split('.')[0]}_translated.mp3",
        )

        operation = client.synthesize_long_audio(request=request)
        # Set a deadline for your LRO to finish. 300 seconds is reasonable, but can be adjusted depending on the length of the input.
        # If the operation times out, that likely means there was an error. In that case, inspect the error, and try again.
        result = operation.result(timeout=300)
        print(
            "\nFinished processing, check your GCS bucket to find your audio file! Printing what should be an empty result: ",
            result,
        )