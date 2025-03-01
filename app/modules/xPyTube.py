import os
import random
import httpx
import time
from dotenv import load_dotenv
load_dotenv("../.env")

from pytubefix import YouTube
from moviepy import AudioFileClip

SERVER = os.getenv("SERVER")
PROXY_LIST_URL = "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.txt"

def get_random_proxy():
    try:
        response = httpx.get(PROXY_LIST_URL, timeout=10)
        response.raise_for_status()
        # Split the response text by lines to get a list of proxies
        proxies = response.text.splitlines()
        if not proxies:
            raise Exception("No proxies found in the list")
        # Select a random proxy from the list
        selected_proxy = random.choice(proxies).strip()
        # Build the proxy dictionary for httpx/pytubefix usage
        proxy = {
            "http": f"socks5://{selected_proxy}",
            "https": f"socks5://{selected_proxy}"
        }
        return proxy
    except Exception as e:
        print(f"Error fetching proxy list: {e}")
        raise

def test_proxy(proxy, timeout=5):
    """Test if proxy is working by making a request to a test URL"""
    try:
        with httpx.Client(proxies=proxy, timeout=timeout) as client:
            response = client.get("https://www.google.com")
            return response.status_code == 200
    except Exception:
        return False

def convert_to_mp3(video_url):
    max_retries = 8  # Increased from 5
    used_proxies = set()  # Keep track of already used proxies
    
    for attempt in range(max_retries):
        try:
            # Add exponential backoff between attempts
            if attempt > 0:
                backoff_time = min(2 ** attempt, 30)  # Cap at 30 seconds
                print(f"Waiting {backoff_time} seconds before next attempt...")
                time.sleep(backoff_time)
            
            print(f"Attempt {attempt+1}/{max_retries}: Step 1 - Getting free proxy...")
            
            # Get and test proxy
            proxy = None
            for _ in range(3):  # Try up to 3 proxies per attempt
                proxy = get_random_proxy()
                proxy_id = str(proxy)
                if proxy_id in used_proxies:
                    print("Skipping already used proxy...")
                    continue
                
                print(f"Testing proxy: {proxy}")
                if test_proxy(proxy):
                    used_proxies.add(proxy_id)
                    print("Using proxy:", proxy)
                    break
                else:
                    print("Proxy test failed, trying another...")
            
            if proxy is None:
                print("Failed to find working proxy, trying without proxy...")
                proxy = {}  # Try with no proxy as last resort
            
            print("Step 2 - Downloading YouTube video...")
            if SERVER == "0":
                yt = YouTube(video_url, 'WEB', proxies=proxy)
                mp3_output_dir = os.getcwd()
            else:
                yt = YouTube(video_url, 'WEB', proxies=proxy)
                mp3_output_dir = "/tmp"
                
            # Add a small delay to avoid hitting rate limits
            time.sleep(1)
            
            # Get video information first to verify connection works
            print("Fetching video info...")
            title = yt.title
            print(f"Video title: {title}")
            
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
            error_str = str(e).lower()
            rate_limit_indicators = ["429", "too many requests", "rate limit", "quota exceeded"]
            
            if any(indicator in error_str for indicator in rate_limit_indicators):
                print(f"Rate limiting detected: {e}")
                continue
            elif "video unavailable" in error_str:
                raise Exception(f"Video unavailable. Please check the URL: {str(e)}")
            else:
                print(f"An error occurred: {e}")
                # Only retry for network or proxy related errors
                if "connection" in error_str or "timeout" in error_str or "proxy" in error_str:
                    continue
                else:
                    raise Exception("Fail on Pytube: " + str(e))
    
    raise Exception("Failed to convert video after multiple attempts due to rate limiting.")

if __name__ == '__main__':
    video_url = input("Youtube video URL'si girin: ")
    result = convert_to_mp3(video_url)
    if result:
        mp3_path, name = result
        print(f"MP3 dosyası oluşturuldu: {mp3_path}")
        print(f"MP3 dosyası adı: {name}")