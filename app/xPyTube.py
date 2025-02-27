from pytubefix import YouTube
from moviepy import AudioFileClip
import os

def convert_to_mp3(video_url):
    try:
        # Download the YouTube video
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream = audio_stream.download()
        
        # Set the output directory to /tmp and construct a new file path
        mp3_output_dir = "/tmp"
        base_name = os.path.splitext(os.path.basename(audio_stream))[0]
        mp3_path = os.path.join(mp3_output_dir, base_name + '.mp3')
        
        # Extract the audio using AudioFileClip
        with AudioFileClip(audio_stream) as clip:
            clip.write_audiofile(mp3_path)
        
        # Optionally, remove the original audio file
        os.remove(audio_stream)
                
        # Return the MP3 path and its filename as dynamic name
        return mp3_path, os.path.basename(mp3_path)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    video_url = input("Youtube video URL'si girin: ")
    result = convert_to_mp3(video_url)
    if result:
        mp3_path, name = result
        print(f"MP3 dosyası oluşturuldu: {mp3_path}")
        print(f"MP3 dosyası adı: {name}")