from dotenv import load_dotenv
load_dotenv("../.env")

from pytubefix import YouTube
from moviepy import AudioFileClip
import os

from fp.fp import FreeProxy

# Get a free proxy
SERVER = os.getenv("SERVER")

def convert_to_mp3(video_url):
    try:
        proxyhttp = FreeProxy(rand=True, timeout=1).get()
        
        print(f"HTTP Proxy: {proxyhttp}")
        
        proxy = {
            "http": proxyhttp
            }
        
        visitorData = "MnQkEuuYQCfvICQq0-Lb2Zz9-rbWIcap-xfVCR8VbG-7sd6mPE_Ch-badrNco1OvQYewrAx2kt0HjQco5xtx_9Mh_jGb6nMTydz5sdiYWw2tnvHAwvYe4pNoOlaxUKoRn4YmtpWEhfb_NtFMJmi79rHvqlo8Dg=="
        poToken = "CgtBUGtab2NxMXpycyiH7oa-BjIKCgJVUxIEGgAgRg%3D%3D"
    
        # Download the YouTube video
        if SERVER == 0:
            yt = YouTube(video_url)
            mp3_output_dir = os.getcwd()
        else:
            print(f"Using proxy: {proxy}")
            yt = YouTube(video_url, 'WEB', use_po_token=True, po_token_verifier=(visitorData, poToken))
            mp3_output_dir = "/tmp"
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream = audio_stream.download()
        
        # Set the output directory to /tmp and construct a new file path
        try:
            if mp3_output_dir and not os.path.exists(mp3_output_dir):
                os.makedirs(mp3_output_dir)
        except Exception as e:
            print(f"Error: {e}")
            mp3_output_dir = os.getcwd()
            pass
        
        base_name = os.path.splitext(os.path.basename(audio_stream))[0]
        print(f"Base name: {base_name}")
        mp3_path = os.path.join(mp3_output_dir, 'temp.mp3')
        
        # Extract the audio using AudioFileClip
        with AudioFileClip(audio_stream) as clip:
            clip.write_audiofile(mp3_path)
        
        # Optionally, remove the original audio file
        os.remove(audio_stream)
                
        # Return the MP3 path and its filename as dynamic name
        return mp3_path, base_name
    
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    video_url = input("Youtube video URL'si girin: ")
    result = convert_to_mp3(video_url)
    if result:
        mp3_path, name = result
        print(f"MP3 dosyası oluşturuldu: {mp3_path}")
        print(f"MP3 dosyası adı: {name}")