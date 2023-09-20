import logging
import os
import moviepy.editor

class Video_convertor:
    def __init__(self, download_path ,audio_path):
        self.download_path = download_path
        self.audio_path = audio_path
    def split_to_audio(self, file_name):
        try:
            # Replace 'output_audio.mp3' with the desired output audio file path
            input_video_path = os.path.join("./",self.download_path, file_name)
            output_audio_path = os.path.join("./",self.audio_path, file_name)
            logging.info(f"Converting file: {input_video_path}")
            try: 
                if os.path.exists(input_video_path):
                    video_clip = moviepy.editor.VideoFileClip(str(input_video_path))
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