import logging
import ffmpeg
import os
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
from pydub.effects import speedup
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx

class Video_convertor:
    def __init__(self, download_path, audio_path, video_path, output_path):
        self.download_path = download_path
        self.audio_path = audio_path
        self.video_path = video_path
        self.output_path = output_path
    def split_to_audio(self, file_name):
        try:
            input_video_path = os.path.join(self.download_path, file_name)
            intermediate_audio_path = os.path.join(self.audio_path, file_name.replace('.mp4', '.mp3'))
            output_audio_path = os.path.join(self.audio_path, file_name.replace('.mp4', '.webm'))
            output_video_no_audio_path = os.path.join(self.video_path, file_name)

            logging.info(f"Processing file: {input_video_path}")

            if os.path.exists(input_video_path):
                video_clip = VideoFileClip(str(input_video_path))

                # Extract and save the audio to an intermediate MP3 file
                video_clip.audio.write_audiofile(intermediate_audio_path)
                logging.info(f"Audio extracted and saved to: {intermediate_audio_path}")

                # Convert MP3 to WEBM OPUS
                (
                    ffmpeg
                    .input(intermediate_audio_path)
                    .output(output_audio_path, acodec='libopus')
                    .run(overwrite_output=True)
                )
                logging.info(f"Converted audio to WEBM OPUS and saved to: {output_audio_path}")

                # Save a copy of the video without audio
                video_clip.write_videofile(output_video_no_audio_path, audio=False)
                logging.info(f"Video without audio saved to: {output_video_no_audio_path}")

                # Close the video clip
                video_clip.close()

                return {"audio_file": file_name.replace('.mp4', '.webm'), "video_file": file_name}
            else:
                logging.error(f"The file '{input_video_path}' does not exist.")
        except Exception as e:
            logging.critical(f"Failed to process the file '{file_name}': {str(e)}")

    def join_video_audio(self, video_name, input_audio_path):
        input_video_path = os.path.join(self.video_path, video_name)
        # Load the video and audio clips
        video_clip = VideoFileClip(input_video_path)
        audio_clip = AudioFileClip(input_audio_path)
        speed_corelation = video_clip.duration/audio_clip.duration
        logging.info(f"Speed of video increased for: {speed_corelation}")
        adjusted_video_clip = video_clip.speedx(speed_corelation)
        adjusted_video_clip = adjusted_video_clip.set_audio(audio_clip)
        output_file_path = os.path.join(self.output_path, video_name)

        # Write the combined video to the specified output file
        adjusted_video_clip.write_videofile(output_file_path, codec='libx264')

        print(f'Combined video with audio saved to {output_file_path}')