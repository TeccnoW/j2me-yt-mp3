import os
import subprocess
import sys

def get_ffmpeg_path():
    try:
        # Use the Windows "where" command to locate ffmpeg.exe
        result = subprocess.check_output("where ffmpeg", shell=True)
        # Return the first matching path
        ffmpeg_path = result.decode().splitlines()[0]
        print(f"Found FFmpeg at {ffmpeg_path}")
        return ffmpeg_path
    except subprocess.CalledProcessError:
        print("FFmpeg not found in PATH. Please install it or add it to your PATH.")
        sys.exit(1)

# Dynamically determine the FFmpeg executable path
ffmpeg_path = get_ffmpeg_path()

# Define folders
video_folder = 'Video'
output_folder = 'Output'
os.makedirs(output_folder, exist_ok=True)
os.makedirs(video_folder, exist_ok=True)

def convert_file(input_path, output_path):
    command = [
        ffmpeg_path,
        '-hwaccel', 'cuda',
        '-i', input_path,
        '-vf', 'scale=288:216',
        '-c:v', 'h264_nvenc',
        '-profile:v', 'baseline',
        '-level', '2.1',
        '-qp', '25',
        '-threads', '0',
        '-ac', '1',
        output_path
    ]
    
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command, check=True)

def process_files():
    # Process each .mp4 file in the video folder
    for filename in os.listdir(video_folder):
        if filename.lower().endswith('.mp4'):
            input_path = os.path.join(video_folder, filename)
            # Change extension to .mp4 for output (could be altered if needed)
            output_filename = os.path.splitext(filename)[0] + '.mp4'
            output_path = os.path.join(output_folder, output_filename)
            print(f"Converting {input_path} to {output_path}...")
            try:
                convert_file(input_path, output_path)
            except subprocess.CalledProcessError as e:
                print(f"Error converting {input_path}: {e}")

if __name__ == "__main__":
    process_files()