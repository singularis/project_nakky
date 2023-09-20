from google.cloud import storage, translate_v2

class Translator():
    def __init__(self, project_id, bucket_name, target_language ):
        self.project_id =project_id
        self.bucket_name = bucket_name
        self.input_tex_file_name = ""
        self.target_language = target_language
        self.source_content = ""
        self.translated_content = ""
    def read_original_text(self, input_file_name):
        self.input_file_name = input_file_name
        self.input_tex_file_name = f"{input_file_name.split('.')[0]}.txt"
        storage_client = storage.Client()
        source_bucket = storage_client.bucket(self.bucket_name)
        source_blob = source_bucket.blob(self.input_tex_file_name)
        # Read the content of the source file
        self.source_content = source_blob.download_as_text()
    def translate(self):
        translate_client = translate_v2.Client()
        self.translated_content = translate_client.translate(self.source_content, target_language=self.target_language)
    def write_translation_to_bucket(self):
        storage_client = storage.Client()
        target_bucket = storage_client.bucket(self.bucket_name)
        target_blob = target_bucket.blob(f"{self.input_file_name}_translate.txt")
        # Upload the translated content to Google Cloud Storage
        target_blob.upload_from_string(self.translated_content['translatedText'], content_type='text/plain;charset=utf-8')