from dotenv import load_dotenv
load_dotenv("../.env")

from pytubefix import YouTube
from moviepy import AudioFileClip
import os

SERVER = os.getenv("SERVER")

def convert_to_mp3(video_url):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt+1}: Step 1 - Getting free proxy...")
            proxy = {
            "http": "149.86.159.4:8080",
            }
            
            print("Step 2 - Setting output directory...")
            if SERVER == "0":
                mp3_output_dir = os.getcwd()
            else:
                mp3_output_dir = "/tmp"
                
            print("Step 2 - Downloading video using Pytube...")
            yt = YouTube(video_url, 'WEB', proxies=proxy)
            
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_file_path = audio_stream.download()
            
            print("Step 3 - Ensuring output directory exists...")
            if mp3_output_dir and not os.path.exists(mp3_output_dir):
                try:
                    os.makedirs(mp3_output_dir)
                except Exception as e:
                    print(f"Error creating output dir: {e}")
                    mp3_output_dir = os.getcwd()
            
            base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
            print(f"Step 4 - Base name determined: {base_name}")
            mp3_path = os.path.join(mp3_output_dir, 'temp.mp3')
            
            print("Step 5 - Extracting audio using AudioFileClip...")
            with AudioFileClip(audio_file_path) as clip:
                clip.write_audiofile(mp3_path)
            
            print("Step 6 - Removing the original audio file...")
            os.remove(audio_file_path)
                    
            print("Step 7 - Conversion completed successfully, returning result.")
            return mp3_path, base_name + ".mp3"
        
        except Exception as e:
            if "HTTP Error 429" in str(e):
                print("HTTP Error 429: Too Many Requests. Trying a new proxy...")
                continue
            else:
                print(f"An error occurred: {e}")
                raise Exception("Fail on Pytube: " + str(e))

    raise Exception("Failed to convert video after multiple attempts due to rate limiting.")

if __name__ == '__main__':
    video_url = input("Youtube video URL'si girin: ")
    result = convert_to_mp3(video_url)
    if result:
        mp3_path, name = result
        print(f"MP3 dosyası oluşturuldu: {mp3_path}")
        print(f"MP3 dosyası adı: {name}")