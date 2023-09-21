# project_nakky

## Translate any youtube video to any language  and dictate it back via speech to text.

## Pass youtube video link and receive back translate video

# Needed apis: speech.googleapis.com,  texttospeech.googleapis.com, translate.googleapis.com

# How to start:

Authenticate to your GCP account

`gcloud init`

`gcloud auth application-default login`

Enable apis: speech.googleapis.com,  texttospeech.googleapis.com, translate.googleapis.com

Create GCP bucket for temporary files

Pass your project VIDEO_LINK value in tha main file: video_link

Pass your project ID value in tha main file: project_id

Pass your BUCKET_NAME value in tha main file: BUCKET_NAME

Create all folder listed in main folder

Install all necessary libraries

Run main.py
