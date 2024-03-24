import logging
import time
import yaml
from cli import cli
from flow import Flow

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
voice_type = "en-US-Standard-D"
source_language = "ru-RU"
# Currently not supported: en-US-Studio-M, to try: en-US-Standard-D, default en-US-Standard-A

args = cli()
start_time = time.time()
flow = Flow(resolution=resolution, download_path=download_path,
            audio_path=audio_path, video_path=video_path, output_path=output_path, project_id=project_id,
            bucket_name=bucket_name, voice_type=voice_type, source_language=source_language)

if args.youtube:
    flow.youtube(video_link=args.youtube)
elif args.local:
    flow.local(video_file=args.local)
else:
    logging.critical("Not provided auth method")
    exit()

end_time = time.time()
execution_time = end_time - start_time
logging.info(f"Execution time {execution_time}")
logging.info("Video processed successfully.")