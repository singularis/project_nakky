import logging
import os
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
from pydub.effects import speedup
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx

class Video_convertor:
    def __init__(self, download_path ,audio_path, video_path, output_path):
        self.download_path = download_path
        self.audio_path = audio_path
        self.video_path = video_path
        self.output_path = output_path
    def split_to_audio(self, file_name):
        try:
            # Replace 'output_audio.mp3' with the desired output audio file path
            input_video_path = os.path.join("./",self.download_path, file_name)
            output_audio_path = os.path.join("./",self.audio_path, file_name)
            logging.info(f"Converting file: {input_video_path}")
            try: 
                if os.path.exists(input_video_path):
                    video_clip = VideoFileClip(str(input_video_path))
                    # Extract the audio
                    video_clip.audio.write_audiofile(output_audio_path)
                    # Close the video and audio clips
                    video_clip.close()
                    logging.info(f"Converted in to audio file: {output_audio_path}")
                else:
                    print(f"The file '{input_video_path}' does not exist.")
            except:
                logging.critical(f"Failed to parse in to audion: {output_audio_path}")
        except:
            logging.critical(f"Failed to parse in to audion: {output_audio_path}")
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